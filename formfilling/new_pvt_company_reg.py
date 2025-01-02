from flask import Flask, request, jsonify
from pymongo import MongoClient
from fpdf import FPDF
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import openai
import requests

app = Flask(__name__)

# OpenAI API Key
openai.api_key = "YOUR_OPENAI_API_KEY"

# MongoDB Configuration
mongo_client = MongoClient("mongodb://localhost:27017/")
db = mongo_client["company_registration"]
users_collection = db["user_sessions"]

# QuadrantDB (Simulated In-Memory Session Storage)
sessions = {}

### Step Definitions ###
workflow_steps = [
    "basic_details", "registered_office", "directors",
    "shareholders", "dsc", "name_approval", "additional", "upload_documents"
]

mandatory_documents = [
    "PAN card (Director 1)", "PAN card (Director 2)", 
    "Aadhaar card (Director 1)", "Aadhaar card (Director 2)", 
    "Registered office address proof"
]

optional_documents = [
    "Trademark registration certificate", 
    "GST registration proof", 
    "Professional tax registration"
]

# Workflow Prompts
prompts = {
    "basic_details": "Please provide:\n1. Proposed Company Name(s):\n2. Business Description:\n3. Authorized Capital (INR):\n4. Paid-up Capital (INR):",
    "registered_office": "Please share the company's registered office address:\n1. Address Line 1:\n2. Address Line 2:\n3. City:\n4. State:\n5. PIN Code:\n6. Mobile Number:\n7. Email Address:",
    "directors": "Provide details for each director:\n1. Name\n2. Father's Name\n3. DOB (DD/MM/YYYY)\n4. PAN\n5. Aadhaar\n6. DIN (if available)\n7. Address\n8. Email\n9. Mobile:\nSend these details in the same format.",
    "shareholders": "Provide details for each shareholder:\n1. Name\n2. PAN\n3. Shareholding (%)\n4. Address:",
    "dsc": "Do all directors/shareholders have a Digital Signature Certificate (DSC)? If not, list the names for assistance.",
    "name_approval": "For company name approval:\n1. Is the name based on business/names/theme?\n2. Brief rationale for the name:",
    "additional": "Any additional requirements? e.g., MoA/AoA drafting or stamp duty assistance:",
    "upload_documents": f"Upload the following mandatory documents:\n{', '.join(mandatory_documents)}.\nYou may also upload optional documents:\n{', '.join(optional_documents)}."
}

### Helper Functions ###
def get_user_session(user_id):
    """Fetch the user session from QuadrantDB (simulated)."""
    if user_id not in sessions:
        sessions[user_id] = {"current_step": "basic_details", "data": {}, "documents": {}}
    return sessions[user_id]

def save_user_data(user_id, key, value):
    """Save user data into MongoDB."""
    user_data = users_collection.find_one({"user_id": user_id})
    if not user_data:
        users_collection.insert_one({"user_id": user_id, "data": {key: value}})
    else:
        user_data["data"][key] = value
        users_collection.update_one({"user_id": user_id}, {"$set": {"data": user_data["data"]}})

def save_document(user_id, doc_name, doc_url):
    """Save document upload details."""
    user_data = users_collection.find_one({"user_id": user_id})
    if not user_data:
        users_collection.insert_one({"user_id": user_id, "documents": {doc_name: doc_url}})
    else:
        documents = user_data.get("documents", {})
        documents[doc_name] = doc_url
        users_collection.update_one({"user_id": user_id}, {"$set": {"documents": documents}})

def move_to_next_step(session):
    """Advance the workflow step."""
    current_step = session["current_step"]
    next_step_index = workflow_steps.index(current_step) + 1
    if next_step_index < len(workflow_steps):
        session["current_step"] = workflow_steps[next_step_index]
    else:
        session["current_step"] = "completed"

def list_missing_documents(user_id):
    """Check and return missing documents."""
    user_data = users_collection.find_one({"user_id": user_id})
    uploaded_documents = user_data.get("documents", {})
    missing_mandatory = [doc for doc in mandatory_documents if doc not in uploaded_documents]
    return missing_mandatory

def send_message_via_whatsapp(recipient_id, message):
    """Send a message using WhatsApp Business API."""
    url = "https://graph.facebook.com/v15.0/your-whatsapp-business-id/messages"
    headers = {
        "Authorization": "Bearer YOUR_ACCESS_TOKEN",
        "Content-Type": "application/json",
    }
    payload = {
        "messaging_product": "whatsapp",
        "to": recipient_id,
        "type": "text",
        "text": {"body": message},
    }
    response = requests.post(url, headers=headers, json=payload)
    if response.status_code != 200:
        print(f"Failed to send message: {response.json()}")
    return response.json()

### Flask Routes ###
@app.route("/whatsapp-webhook", methods=["POST"])
def whatsapp_webhook():
    """Handle incoming WhatsApp messages."""
    data = request.json

    # Parse data received from WhatsApp API
    messages = data.get("entry", [])[0].get("changes", [])[0].get("value", {}).get("messages", [])
    if not messages:
        return jsonify({"status": "no_messages"})

    # Get message details
    message = messages[0]
    user_id = message["from"]
    message_type = message["type"]
    session = get_user_session(user_id)

    # Handle file uploads
    if message_type == "document":
        document_url = message["document"]["link"]
        document_name = message["document"]["filename"]
        save_document(user_id, document_name, document_url)
        send_message_via_whatsapp(user_id, f"Received your document: {document_name}.")
        return jsonify({"status": "document_received"})

    # Handle text messages
    user_input = message["text"]["body"]
    current_step = session["current_step"]

    # If session is completed
    if current_step == "completed":
        missing_docs = list_missing_documents(user_id)
        if missing_docs:
            send_message_via_whatsapp(user_id, f"Missing mandatory documents: {', '.join(missing_docs)}.\nPlease upload them.")
        else:
            send_message_via_whatsapp(user_id, "All details and documents have been collected. Thank you!")
        return jsonify({"status": "completed"})

    # Generate prompt and response
    prompt = prompts.get(current_step, "Invalid step.")
    response = user_input  # Directly use user input as response (for simplicity)
    save_user_data(user_id, current_step, response)

    # Move to the next step
    move_to_next_step(session)

    # Send the next step prompt
    next_prompt = prompts.get(session["current_step"], "Thank you! Workflow is completed.")
    send_message_via_whatsapp(user_id, next_prompt)

    return jsonify({"status": "success"})

### Entry Point ###
if __name__ == "__main__":
    app.run(port=5000)
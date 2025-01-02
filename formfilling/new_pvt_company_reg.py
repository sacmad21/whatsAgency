import logging
from pymongo import MongoClient
from fpdf import FPDF
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import requests
import azure.functions as func
import json

# MongoDB Configuration
mongo_client = MongoClient("mongodb://<MONGO_DB_CONNECTION_STRING>")
db = mongo_client["company_registration"]
users_collection = db["user_sessions"]

# In-Memory Session Storage
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
    "directors": "Provide details for each director:\n1. Name\n2. Father's Name\n3. DOB (DD/MM/YYYY)\n4. PAN\n5. Aadhaar\n6. Address\n7. Email\n8. Mobile:",
    "shareholders": "Provide details for each shareholder:\n1. Name\n2. PAN\n3. Shareholding (%)\n4. Address:",
    "dsc": "Do all directors/shareholders have a Digital Signature Certificate (DSC)? If not, list the names for assistance.",
    "name_approval": "For company name approval:\n1. Is the name based on business/names/theme?\n2. Brief rationale for the name:",
    "additional": "Any additional requirements? e.g., MoA/AoA drafting or stamp duty assistance:",
    "upload_documents": f"Upload the following mandatory documents:\n{', '.join(mandatory_documents)}.\nYou may also upload optional documents:\n{', '.join(optional_documents)}."
}

### Helper Functions ###
def get_user_session(user_id):
    """Fetch the user session."""
    if user_id not in sessions:
        sessions[user_id] = {"current_step": "basic_details", "data": {}, "documents": {}, "retry_count": 0}
    return sessions[user_id]

def save_user_data(user_id, key, value):
    """Save user data into MongoDB."""
    user_data = users_collection.find_one({"user_id": user_id})
    if not user_data:
        users_collection.insert_one({"user_id": user_id, "data": {key: value}, "documents": {}})
    else:
        user_data["data"][key] = value
        users_collection.update_one({"user_id": user_id}, {"$set": {"data": user_data["data"]}})

def save_document(user_id, doc_name, doc_url):
    """Save document upload details."""
    user_data = users_collection.find_one({"user_id": user_id})
    if not user_data:
        users_collection.insert_one({"user_id": user_id, "data": {}, "documents": {doc_name: doc_url}})
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

def validate_step_data(current_step, user_input):
    """Validate the data provided by the user for the current step."""
    validation_rules = {
        "basic_details": ["Proposed Company Name(s)", "Business Description", "Authorized Capital", "Paid-up Capital"],
        "registered_office": ["Address Line 1", "City", "State", "PIN Code", "Mobile Number", "Email Address"],
        "directors": ["Name", "Father's Name", "DOB", "PAN", "Aadhaar", "Address", "Email", "Mobile"],
    }
    
    required_fields = validation_rules.get(current_step, [])
    missing_fields = [field for field in required_fields if field not in user_input]

    if missing_fields:
        return False, f"Missing fields: {', '.join(missing_fields)}. Please provide them."
    return True, "Valid input."

def list_missing_documents(user_id):
    """Check and return missing documents."""
    user_data = users_collection.find_one({"user_id": user_id})
    uploaded_documents = user_data.get("documents", {})
    missing_mandatory = [doc for doc in mandatory_documents if doc not in uploaded_documents]
    return missing_mandatory

def check_retry_limit(session):
    """Check if the user has exceeded the retry limit for a step."""
    retry_count = session.get("retry_count", 0)

    if retry_count >= 3:
        return False, "You've exceeded the retry limit for this step. Please contact support for assistance."

    session["retry_count"] = retry_count + 1
    return True, "Retry allowed."

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
        logging.error(f"Failed to send message: {response.json()}")
    return response.json()

def main(req: func.HttpRequest) -> func.HttpResponse:
    """Handle incoming WhatsApp messages."""
    logging.info('Python HTTP trigger function processed a request.')

    try:
        data = req.get_json()

        # Parse data received from WhatsApp API
        messages = data.get("entry", [])[0].get("changes", [])[0].get("value", {}).get("messages", [])
        if not messages:
            return func.HttpResponse(body=json.dumps({"status": "no_messages"}), mimetype="application/json")

        # Get message details
        message = messages[0]
        user_id = message["from"]
        session = get_user_session(user_id)
        current_step = session["current_step"]

        # Handle document uploads
        if message.get("type") == "document":
            document_url = message["document"]["link"]
            document_name = message["document"]["filename"]
            save_document(user_id, document_name, document_url)
            send_message_via_whatsapp(user_id, f"Received your document: {document_name}.")
            return func.HttpResponse(body=json.dumps({"status": "document_received"}), mimetype="application/json")

        # Handle text messages
        user_input = message["text"]["body"]
        is_valid, validation_message = validate_step_data(current_step, user_input)

        if not is_valid:
            retry_allowed, retry_message = check_retry_limit(session)
            if not retry_allowed:
                send_message_via_whatsapp(user_id, retry_message)
                return func.HttpResponse(body=json.dumps({"status": "retry_limit_exceeded"}), mimetype="application/json")

            send_message_via_whatsapp(user_id, validation_message)
            return func.HttpResponse(body=json.dumps({"status": "incomplete_data"}), mimetype="application/json")

        # Save valid data and move to next step
        save_user_data(user_id, current_step, user_input)
        move_to_next_step(session)

        # Handle completion
        if session["current_step"] == "completed":
            missing_docs = list_missing_documents(user_id)
            if missing_docs:
                send_message_via_whatsapp(user_id, f"Missing mandatory documents: {', '.join(missing_docs)}. Please upload them.")
            else:
                send_message_via_whatsapp(user_id, "All details and documents have been collected. Thank you!")
            return func.HttpResponse(body=json.dumps({"status": "completed"}), mimetype="application/json")

        # Send next step prompt
        next_prompt = prompts.get(session["current_step"], "Thank you! Workflow is completed.")
        send_message_via_whatsapp(user_id, next_prompt)

        return func.HttpResponse(body=json.dumps({"status": "success"}), mimetype="application/json")

    except Exception as e:
        logging.error(f"Error processing request: {e}")
        return func.HttpResponse(body=json.dumps({"status": "error", "message": str(e)}), mimetype="application/json", status_code=500)

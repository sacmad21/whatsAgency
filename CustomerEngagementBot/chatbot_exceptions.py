from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Dict
import httpx
from config import WHATSAPP_API_URL, WHATSAPP_ACCESS_TOKEN, customer_segments, escalation_rules

app = FastAPI()

# Models
class ComplaintMessage(BaseModel):
    phone_number: str
    message: str

class CampaignStatus(BaseModel):
    campaign_name: str
    status: str  # e.g., "failed", "success"

class InquiryMessage(BaseModel):
    phone_number: str
    message: str
    priority: str  # e.g., "high", "medium", "low"

# Functions
@app.post("/log-complaint")
async def log_complaint(complaint: ComplaintMessage):
    """
    Log repeated complaints and escalate if necessary.

    **Scenario**:
    - Customers report repeated issues with a specific product or service.
    - After three complaints from the same customer, the system automatically escalates the issue to a human agent for immediate resolution.

    Parameters:
    - complaint: Contains the customer's phone number and complaint message.

    Returns:
    - Escalation status or a log confirmation.
    """
    phone_number = complaint.phone_number
    message = complaint.message

    # Increment complaint count
    escalation_rules[phone_number] = escalation_rules.get(phone_number, 0) + 1

    # Check for escalation
    if escalation_rules[phone_number] > 3:
        await escalate_issue(phone_number, message)
        return {"status": "escalated", "phone_number": phone_number, "message": message}

    return {"status": "logged", "phone_number": phone_number, "message": message}

@app.post("/check-campaign-status")
async def check_campaign_status(campaign: CampaignStatus):
    """
    Handle campaign glitches and suggest fallback options.

    **Scenario**:
    - A promotional campaign fails due to technical glitches.
    - The system triggers an alert and recommends fallback email campaigns to ensure continuity.

    Parameters:
    - campaign: Contains the campaign name and its status (e.g., "failed", "success").

    Returns:
    - Alert status and fallback suggestions if the campaign fails.
    """
    if campaign.status == "failed":
        # Trigger alert and suggest fallback
        alert_message = f"Campaign '{campaign.campaign_name}' failed. Suggesting fallback email campaigns."
        # Log alert (could integrate with a monitoring system)
        print(alert_message)
        return {"status": "alert triggered", "suggestion": "Use email campaigns as a fallback."}

    return {"status": "campaign successful", "campaign_name": campaign.campaign_name}

@app.post("/handle-inquiry")
async def handle_inquiry(inquiry: InquiryMessage):
    """
    Prioritize customer inquiries based on urgency and history.

    **Scenario**:
    - During high-demand periods, such as a festive sale, the system experiences a surge in customer inquiries.
    - Chatbots prioritize responses based on customer-provided urgency levels (high, medium, low) and customer history.

    Parameters:
    - inquiry: Contains the customer's phone number, message, and priority level.

    Returns:
    - Confirmation that the response has been sent, including the customer's priority level.
    """
    phone_number = inquiry.phone_number
    message = inquiry.message
    priority = inquiry.priority.lower()

    # Define response based on priority
    if priority == "high":
        response = "Your inquiry is being prioritized. Our team will respond shortly."
    elif priority == "medium":
        response = "Thank you for your inquiry. We will get back to you soon."
    else:
        response = "We have received your message. Please allow some time for a response."

    # Send response
    await send_whatsapp_message(phone_number, response)
    return {"status": "response sent", "phone_number": phone_number, "priority": priority}

# Utility functions
async def escalate_issue(phone_number: str, message: str):
    """
    Escalate an issue to a human agent.

    **Scenario**:
    - When a customer reports repeated issues (e.g., more than three complaints), the system notifies a human agent to intervene.

    Parameters:
    - phone_number: The customer's phone number.
    - message: The latest complaint message.

    Actions:
    - Sends an escalation alert to a monitoring system or a human agent.
    """
    escalation_message = f"Escalation alert! Customer {phone_number} has reported repeated issues: {message}"
    # Log or notify escalation (e.g., send to a monitoring system or Slack channel)
    print(escalation_message)

async def send_whatsapp_message(phone_number: str, message: str):
    """
    Send a message via WhatsApp Business API.

    **Scenario**:
    - Used to communicate directly with customers for inquiries, complaints, or campaign updates.

    Parameters:
    - phone_number: The recipient's phone number.
    - message: The message content to be sent.

    Returns:
    - Sends the message and handles errors if the API request fails.
    """
    headers = {
        "Authorization": f"Bearer {WHATSAPP_ACCESS_TOKEN}",
        "Content-Type": "application/json"
    }
    payload = {
        "messaging_product": "whatsapp",
        "to": phone_number,
        "text": {"body": message}
    }
    async with httpx.AsyncClient() as client:
        response = await client.post(WHATSAPP_API_URL, json=payload, headers=headers)
        if response.status_code != 200:
            raise HTTPException(status_code=response.status_code, detail=response.text)

# Azure Function entry point
def azure_function(req):
    import azure.functions as func
    return func.AsgiMiddleware(app).handle(req)

import httpx
from fastapi import HTTPException
from config import WHATSAPP_API_URL, WHATSAPP_ACCESS_TOKEN

async def send_whatsapp_message(phone_number: str, message: str):
    """
    Send a message via WhatsApp Business API.

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

async def escalate_issue(phone_number: str, message: str):
    """
    Escalate an issue to a human agent.

    Parameters:
    - phone_number: The customer's phone number.
    - message: The latest complaint message.

    Actions:
    - Sends an escalation alert to a monitoring system or a human agent.
    """
    escalation_message = f"Escalation alert! Customer {phone_number} has reported repeated issues: {message}"
    print(escalation_message)  # Replace with real escalation logic (e.g., Slack alert or email)

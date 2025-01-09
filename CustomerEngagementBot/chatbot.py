from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Dict
from config import WHATSAPP_API_URL, WHATSAPP_ACCESS_TOKEN, customer_segments, engagement_data, loyalty_points
from utils import send_whatsapp_message

app = FastAPI()

class PromotionalMessage(BaseModel):
    segment: str
    message: str

class UserMessage(BaseModel):
    phone_number: str
    message: str

@app.post("/send-promotion")
async def send_promotional_message(promotional_message: PromotionalMessage):
    """Send promotional messages to a segmented customer list"""
    segment = promotional_message.segment
    message = promotional_message.message

    if segment not in customer_segments:
        raise HTTPException(status_code=400, detail="Invalid segment")

    for phone_number in customer_segments[segment]:
        await send_whatsapp_message(phone_number, message)
        engagement_data[segment]["messages_sent"] += 1

    return {"status": "Promotional messages sent", "segment": segment, "message": message}

@app.post("/send-class-notification")
async def send_class_notification(class_name: str, class_time: str):
    """
    Notify gym members about an upcoming group class.
    
    This endpoint is particularly useful for gyms with loyalty programs to:
    1. Notify members about upcoming classes.
    2. Encourage participation by offering loyalty reward points.
    3. Build engagement and foster a sense of community among gym members.
    """
    message = f"Join our upcoming {class_name} class at {class_time}! Attend to earn loyalty points!"

    segment = "gym_members"
    if segment not in customer_segments:
        raise HTTPException(status_code=400, detail="Invalid segment")

    for phone_number in customer_segments[segment]:
        await send_whatsapp_message(phone_number, message)
        engagement_data[segment]["messages_sent"] += 1

    return {"status": "Class notifications sent", "class": class_name, "time": class_time}

@app.post("/webhook")
async def whatsapp_webhook(data: dict):
    """
    Handle incoming replies from WhatsApp.

    This endpoint processes different types of customer interactions:
    1. **General Feedback**: Replies are acknowledged with a thank-you message, and engagement is tracked.
    2. **Complaints**: Can be identified using keywords (e.g., "complaint", "issue") and routed for further action.
    3. **Loyalty Rewards**: Gym members' participation is rewarded with additional loyalty points.

    The webhook dynamically determines the response and updates engagement statistics accordingly.
    """
    try:
        # Parse the incoming WhatsApp message
        phone_number = data['messages'][0]['from']
        message = data['messages'][0]['text']['body'].lower()

        # Default response
        response = "Thank you for your feedback! Keep participating to earn more rewards!"

        # Track engagement (reply counts)
        for segment, customers in customer_segments.items():
            if phone_number in customers:
                engagement_data[segment]["replies"] += 1

                # Handle complaints or specific issues
                if "complaint" in message or "issue" in message:
                    response = "We have received your complaint. Our team will get back to you shortly."
                
                # Add loyalty points for gym members
                if segment == "gym_members":
                    loyalty_points[phone_number] = loyalty_points.get(phone_number, 0) + 10

                break

        await send_whatsapp_message(phone_number, response)
        return {"status": "success"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/engagement")
async def get_engagement():
    """Retrieve engagement statistics"""
    return {"engagement": engagement_data, "loyalty_points": loyalty_points}

# Azure Function entry point
def azure_function(req):
    import azure.functions as func
    return func.AsgiMiddleware(app).handle(req)

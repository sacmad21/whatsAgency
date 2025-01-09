from fastapi import FastAPI, HTTPException, Request
from property_availability_query import handle_property_availability_query
from automated_greetings import handle_automated_greetings
from error_handling_queries import handle_query_error
from dynamic_suggestions import handle_dynamic_suggestions
from multilingual_Interaction import handle_multilingual_interaction
from datetime import datetime
import requests  # For making GROQ API calls
from db_config import CosmosDBConfig  # Importing from db-config.py

# Configure Cosmos DB connection using db-config.py
COSMOS_DB_CONFIG = CosmosDBConfig(
    endpoint="<COSMOS_DB_ENDPOINT>",
    key="<COSMOS_DB_KEY>",
    database_name="<COSMOS_DB_NAME>"
)
contact_info_container = COSMOS_DB_CONFIG.create_container(
    container_name="Contact_Info",
    partition_key={"path": "/businessId"}
)

# Implementing GROQ-like API functions
def map_user_id(phone_number, business_id):
    """
    Map phone_number to a user_id in the given business context using the Contact_Info table.
    """
    try:
        # Query the Contact_Info container
        query = "SELECT c.userId FROM c WHERE c.phone = @phone AND c.businessId = @businessId"
        parameters = [
            {"name": "@phone", "value": phone_number},
            {"name": "@businessId", "value": business_id}
        ]
        result = list(contact_info_container.query_items(query=query, parameters=parameters, enable_cross_partition_query=True))

        if result:
            return result[0].get("userId")  # Return the userId from the result
        else:
            return None
    except Exception as e:
        raise ValueError(f"Database query failed: {str(e)}")

def infer_intent(message_text):
    """
    Use GROQ API to infer the intent of the message_text.
    """
    try:
        # GROQ API endpoint for intent detection
        groq_api_url = "https://api.groq.com/intent-detection"
        headers = {"Content-Type": "application/json"}
        payload = {"text": message_text}

        # Make the API call to GROQ
        response = requests.post(groq_api_url, json=payload, headers=headers)

        if response.status_code == 200:
            data = response.json()
            return data.get("intent")  # Assume API returns {"intent": "greeting"}
        else:
            raise ValueError(f"GROQ API error: {response.status_code} - {response.text}")
    except Exception as e:
        raise ValueError(f"Intent inference using GROQ API failed: {str(e)}")

def decode_whatsapp_payload(payload):
    """
    Decode WhatsApp messaging raw payload and convert it into the required request object.
    """
    try:
        # Extract primary message details
        messages = payload.get("messages", [])
        if not messages:
            raise ValueError("No messages found in payload")

        message = messages[0]
        message_text = message.get("text", {}).get("body", "")
        phone_number = message.get("from", "")

        # Extract metadata
        metadata = payload.get("metadata", {})
        phone_number_id = metadata.get("phone_number_id")

        # Derive business_id
        business_id_mapping = {
            "WHATSAPP_BUSINESS_PHONE_NUMBER_ID": "B001"  # Example mapping
        }
        business_id = business_id_mapping.get(phone_number_id, "default_business")

        # Map user_id using Cosmos DB Contact_Info table
        user_id = map_user_id(phone_number, business_id)
        if not user_id:
            raise ValueError(f"User ID mapping failed for phone number: {phone_number}")

        # Infer event type using GROQ API
        event_type = infer_intent(message_text)
        if not event_type:
            raise ValueError(f"Intent inference failed for message: {message_text}")

        return {
            "event_type": event_type,
            "session_id": phone_number,  # Use phone number as session ID
            "business_id": business_id,
            "user_id": user_id,
            "message": message_text,
            "phone_number": phone_number
        }
    except Exception as e:
        raise ValueError(f"Failed to decode payload: {str(e)}")

app = FastAPI()

@app.post("/customer-webhook")
async def customer_communication_webhook(request: Request):
    """
    Webhook to handle all customer communication scenarios with WhatsApp Business API standards.
    """
    try:
        # Parse incoming request
        raw_payload = await request.json()
        payload = decode_whatsapp_payload(raw_payload)

        event_type = payload.get("event_type")
        session_id = payload.get("session_id")
        business_id = payload.get("business_id")
        user_id = payload.get("user_id")
        message = payload.get("message")
        phone_number = payload.get("phone_number")

        # Response template for WhatsApp
        def whatsapp_response(to, response_text, buttons=None):
            response = {
                "to": to,
                "type": "text",
                "text": {"body": response_text}
            }
            if buttons:
                response = {
                    "to": to,
                    "type": "interactive",
                    "interactive": {
                        "type": "button",
                        "body": {"text": response_text},
                        "action": {"buttons": buttons}
                    }
                }
            return response

        # Handle different event types
        if event_type == "greeting":
            result = handle_automated_greetings(
                session_id=session_id,
                business_id=business_id,
                user_id=user_id
            )
            return whatsapp_response(phone_number, result["response"])

        elif event_type == "property_query":
            query_id = payload.get("query_id", f"Q-{datetime.utcnow().strftime('%Y%m%d%H%M%S')}")
            result = handle_property_availability_query(
                query_id=query_id,
                business_id=business_id,
                user_id=user_id,
                query_text=message,
                session_id=session_id
            )
            if result["status"] == "success":
                buttons = [
                    {"type": "reply", "reply": {"id": "adjust_budget", "title": "Adjust Budget"}},
                    {"type": "reply", "reply": {"id": "search_area", "title": "Search Other Areas"}}
                ]
                return whatsapp_response(phone_number, result["response"], buttons=buttons)
            else:
                return whatsapp_response(phone_number, "Sorry, no properties found.")

        elif event_type == "error":
            error_message = payload.get("error_message", "An unknown error occurred.")
            result = handle_query_error(
                session_id=session_id,
                business_id=business_id,
                user_id=user_id,
                error_message=error_message
            )
            buttons = [
                {"type": "reply", "reply": {"id": "try_again", "title": "Try Again"}},
                {"type": "reply", "reply": {"id": "view_trending", "title": "View Trending Properties"}}
            ]
            return whatsapp_response(phone_number, result["response"], buttons=buttons)

        elif event_type == "dynamic_suggestions":
            result = handle_dynamic_suggestions(
                session_id=session_id,
                business_id=business_id,
                user_id=user_id
            )
            return whatsapp_response(phone_number, result["response"])

        elif event_type == "multilingual_interaction":
            target_language = payload.get("target_language", "en")
            result = handle_multilingual_interaction(
                session_id=session_id,
                business_id=business_id,
                user_id=user_id,
                input_text=message,
                target_language=target_language
            )
            return whatsapp_response(phone_number, result["response"])

        else:
            return whatsapp_response(phone_number, "Unsupported event type.")

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Example to test the webhook locally
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

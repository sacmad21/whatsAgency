from fastapi import APIRouter, HTTPException
from db_config import (
    categories_container,
    products_container,
    customers_container,
    promotions_container,
    feedback_container,
)
from feedback_config import FEEDBACK_RULES
from utils import send_whatsapp_message
import httpx
from datetime import datetime
import uuid

webhook_router = APIRouter()

async def identify_message_category(message: str) -> str:
    """
    Use GROQ APIs to identify the category of a message (e.g., complaint, feedback, inquiry).
    """
    try:
        async with httpx.AsyncClient() as client:
            response = await client.post("https://groqapi.com/classify", json={"text": message})
            response.raise_for_status()
            return response.json().get("category", "unknown")
    except Exception as e:
        print(f"Error identifying message category: {e}")
        return "unknown"

@webhook_router.post("/webhook")
async def whatsapp_webhook(data: dict):
    """
    Handle incoming replies from WhatsApp with enhanced functionality.

    **Enhancements**:
    - Intelligent query understanding with Generative AI.
    - Multi-criteria recommendations.
    - Interactive WhatsApp templates.
    - Proactive suggestions and sentiment analysis.
    """
    try:
        # Parse the incoming WhatsApp message
        phone_number = data['messages'][0]['from']
        message = data['messages'][0]['text']['body']

        # Identify the category of the message using GROQ API
        category = await identify_message_category(message)

        # Fetch rules for the identified category
        rules = FEEDBACK_RULES.get(category, FEEDBACK_RULES["unknown"])

        # Default response based on rules
        response = rules["response"]

        # Retrieve customer details from Cosmos DB
        customer_query = f"SELECT * FROM c WHERE c.id = '{phone_number}'"
        customer = list(customers_container.query_items(query=customer_query, enable_cross_partition_query=True))

        if customer:
            customer_name = customer[0].get("name", "Customer")
            preferences = customer[0].get("preferences", {})
            print(f"Customer found: {customer_name}")
        else:
            customer_name = "Customer"
            preferences = {}
            print(f"No customer record found for {phone_number}")

        # Proactive assistance with personalized suggestions
        proactive_suggestions = []
        if preferences:
            product_query = (
                f"SELECT * FROM c WHERE c.category_id IN ({','.join(preferences.get('categories', []))}) AND c.availability = true"
            )
            proactive_suggestions = list(products_container.query_items(query=product_query, enable_cross_partition_query=True))
            if proactive_suggestions:
                response += f"\nHere are some items based on your preferences: {[item['name'] for item in proactive_suggestions]}"

        # Log the message into `feedback` container
        feedback_container.upsert_item({
            "id": str(uuid.uuid4()),
            "customer_id": phone_number,
            "message_body": message,
            "timestamp": datetime.utcnow().isoformat(),
            "sentiment_score": rules.get("sentiment_score", "neutral"),
            "category": category,
        })

        # Use interactive WhatsApp templates
        response_template = {
            "type": "interactive",
            "header": {"type": "text", "text": "Product Recommendations"},
            "body": {"text": response},
            "footer": {"text": "Thank you for shopping with us!"}
        }

        # Send response and log outcome
        try:
            await send_whatsapp_message(phone_number, response_template)
            print(f"Response sent to {phone_number}: {response}")
        except Exception as send_error:
            print(f"Failed to send response to {phone_number}: {send_error}")

        return {"status": "success"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

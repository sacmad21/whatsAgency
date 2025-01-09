from custInteractionBot.utils.query_management_utils import save_customer_query, fetch_queries_by_user
from custInteractionBot.utils.user_preferences_utils import search_properties
from custInteractionBot.utils.session_management_utils import create_chat_session
from datetime import datetime

def handle_property_availability_query(query_id, business_id, user_id, query_text, session_id):
    """
    Handle a user query for property availability.
    """
    # Save the customer query
    timestamp = str(datetime.utcnow())
    save_result = save_customer_query(
        query_id=query_id,
        business_id=business_id,
        user_id=user_id,
        query_text=query_text,
        timestamp=timestamp
    )
    if save_result["status"] != "success":
        return {"status": "error", "message": "Failed to save customer query."}

    # Extract search criteria from the query (Placeholder: implement NLP for real scenarios)
    search_filters = {
        "type": "Apartment",
        "price": 50000  # Example filter; adapt based on query text parsing
    }

    # Search for properties matching the criteria
    search_result = search_properties(business_id=business_id, filters=search_filters)
    if search_result["status"] != "success":
        return {"status": "error", "message": "Failed to search properties."}

    properties = search_result["data"]

    # Prepare chatbot response based on search results
    if properties:
        response_text = f"Found {len(properties)} matching properties. Here are the details: "
        response_text += "\n".join([f"- {prop['address']} priced at {prop['price']}" for prop in properties])
    else:
        response_text = "No matching properties found. Would you like to adjust your search criteria?"

    # Log the session
    create_chat_session(
        session_id=session_id,
        business_id=business_id,
        user_id=user_id,
        messages=[
            {"messageId": "M1", "content": query_text, "timestamp": timestamp},
            {"messageId": "M2", "content": response_text, "timestamp": str(datetime.utcnow())}
        ]
    )

    return {"status": "success", "response": response_text}

# Example usage
if __name__ == "__main__":
    result = handle_property_availability_query(
        query_id="Q123",
        business_id="B001",
        user_id="U001",
        query_text="Is there a 2-bedroom apartment available?",
        session_id="S001"
    )
    print(result)

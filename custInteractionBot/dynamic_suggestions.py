from custInteractionBot.utils.query_management_utils import fetch_queries_by_user
from custInteractionBot.utils.user_preferences_utils import search_properties
from custInteractionBot.utils.session_management_utils import create_chat_session
from datetime import datetime

def handle_dynamic_suggestions(session_id, business_id, user_id):
    """
    Analyze user query patterns and suggest trending properties dynamically.
    """
    # Fetch recent queries from the user
    query_result = fetch_queries_by_user(user_id=user_id, business_id=business_id)
    if query_result["status"] != "success":
        return {"status": "error", "message": "Failed to fetch user queries."}

    user_queries = query_result["data"]

    # Analyze user preferences from recent queries (Placeholder for advanced NLP)
    filters = {"location": "Downtown", "price": 50000}  # Example filters based on query analysis

    # Search for trending properties based on analyzed preferences
    search_result = search_properties(business_id=business_id, filters=filters)
    if search_result["status"] != "success":
        return {"status": "error", "message": "Failed to fetch property suggestions."}

    properties = search_result["data"]

    # Prepare chatbot response based on search results
    if properties:
        response_text = "We noticed you're looking for properties in Downtown. Here are some trending options:\n"
        response_text += "\n".join([f"- {prop['address']} priced at {prop['price']}" for prop in properties])
    else:
        response_text = "We couldn't find any trending properties matching your preferences. Would you like to explore other areas?"

    # Log the suggestions in a chat session
    timestamp = str(datetime.utcnow())
    session_result = create_chat_session(
        session_id=session_id,
        business_id=business_id,
        user_id=user_id,
        messages=[
            {"messageId": "M1", "content": "Analyzing recent activity...", "timestamp": timestamp},
            {"messageId": "M2", "content": response_text, "timestamp": str(datetime.utcnow())}
        ]
    )

    if session_result["status"] != "success":
        return {"status": "error", "message": "Failed to log dynamic suggestions session."}

    # Return response
    return {
        "status": "success",
        "response": response_text
    }

# Example usage
if __name__ == "__main__":
    result = handle_dynamic_suggestions(
        session_id="S004",
        business_id="B001",
        user_id="U004"
    )
    print(result)

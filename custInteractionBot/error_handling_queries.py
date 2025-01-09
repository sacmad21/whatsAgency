from custInteractionBot.utils.session_management_utils import create_chat_session
from datetime import datetime

def handle_query_error(session_id, business_id, user_id, error_message):
    """
    Handle errors encountered during query processing by suggesting alternative options.
    """
    # Prepare error response
    apology_message = (
        "We're sorry, but we couldn't process your request due to an error."
    )

    # Provide alternative options
    suggestion_message = (
        "Here are some things you can try:\n"
        "- 'Find properties under $100,000'\n"
        "- 'Show me apartments in Uptown'\n"
        "- 'List properties with 3 bedrooms'"
    )

    # Log the error and suggestions in a chat session
    timestamp = str(datetime.utcnow())
    session_result = create_chat_session(
        session_id=session_id,
        business_id=business_id,
        user_id=user_id,
        messages=[
            {"messageId": "M1", "content": error_message, "timestamp": timestamp},
            {"messageId": "M2", "content": apology_message, "timestamp": str(datetime.utcnow())},
            {"messageId": "M3", "content": suggestion_message, "timestamp": str(datetime.utcnow())}
        ]
    )

    if session_result["status"] != "success":
        return {"status": "error", "message": "Failed to log error handling session."}

    # Return response
    return {
        "status": "success",
        "response": apology_message + "\n" + suggestion_message
    }

# Example usage
if __name__ == "__main__":
    result = handle_query_error(
        session_id="S003",
        business_id="B001",
        user_id="U003",
        error_message="System encountered a timeout error while fetching properties."
    )
    print(result)

from custInteractionBot.utils.session_management_utils import create_chat_session
from datetime import datetime

def handle_automated_greetings(session_id, business_id, user_id):
    """
    Send an automated greeting and suggest initial property search options.
    """
    # Prepare the greeting message
    greeting_message = "Hello! Welcome to Real Estate Assistant. How can I assist you today?"

    # Prepare suggestions for initial search
    suggestion_message = (
        "You can start by searching for properties. Here are some options:\n"
        "- 'Show me properties under $50,000'\n"
        "- 'Find 2-bedroom apartments in Downtown'\n"
        "- 'What properties are available in my area?'"
    )

    # Log the greeting and suggestions in a chat session
    timestamp = str(datetime.utcnow())
    session_result = create_chat_session(
        session_id=session_id,
        business_id=business_id,
        user_id=user_id,
        messages=[
            {"messageId": "M1", "content": greeting_message, "timestamp": timestamp},
            {"messageId": "M2", "content": suggestion_message, "timestamp": str(datetime.utcnow())}
        ]
    )

    if session_result["status"] != "success":
        return {"status": "error", "message": "Failed to log greeting session."}

    # Return response
    return {
        "status": "success",
        "response": greeting_message + "\n" + suggestion_message
    }

# Example usage
if __name__ == "__main__":
    result = handle_automated_greetings(
        session_id="S002",
        business_id="B001",
        user_id="U002"
    )
    print(result)

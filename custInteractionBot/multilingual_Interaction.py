from custInteractionBot.utils.language_tools_utils import translate_text, detect_language
from custInteractionBot.utils.session_management_utils import create_chat_session
from datetime import datetime

def handle_multilingual_interaction(session_id, business_id, user_id, input_text, target_language):
    """
    Handle a multilingual interaction by translating user input and responding accordingly.
    """
    # Detect the language of the user input
    detected_language = detect_language(input_text)

    # Translate the user input to the target language (if necessary)
    if detected_language != target_language:
        translated_text = translate_text(input_text, target_language)
    else:
        translated_text = input_text

    # Prepare the chatbot response (Example: hardcoded response for simplicity)
    chatbot_response = "Thank you for reaching out! How can I assist you further?"

    # Translate the chatbot response back to the user's language (if necessary)
    if detected_language != target_language:
        translated_response = translate_text(chatbot_response, detected_language)
    else:
        translated_response = chatbot_response

    # Log the conversation in a chat session
    timestamp = str(datetime.utcnow())
    session_result = create_chat_session(
        session_id=session_id,
        business_id=business_id,
        user_id=user_id,
        messages=[
            {"messageId": "M1", "content": input_text, "timestamp": timestamp},
            {"messageId": "M2", "content": translated_response, "timestamp": str(datetime.utcnow())}
        ]
    )

    if session_result["status"] != "success":
        return {"status": "error", "message": "Failed to log multilingual session."}

    # Return response
    return {
        "status": "success",
        "response": translated_response
    }

# Example usage
if __name__ == "__main__":
    result = handle_multilingual_interaction(
        session_id="S005",
        business_id="B001",
        user_id="U006",
        input_text="Hola, ¿puedes ayudarme con opciones de apartamentos?",
        target_language="en"
    )
    print(result)

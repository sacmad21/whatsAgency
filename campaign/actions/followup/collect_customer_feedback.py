from ai import generate_choices_with_prompt
from util import save_user_selection_to_db
from session import session
from datetime import datetime

def build_feedback_prompt(session):
    campaign_name = session.get("campaign_name", "Unnamed Campaign")
    goal = session.get("campaign_goal", "Drive QR redemptions and first purchases")
    main_channels = session.get("main_channels", ["WhatsApp"])
    offer_details = session.get("offer_details", "₹500 off first purchase")
    target_audience = session.get("customer_segments", [{"segment": "All Customers"}])

    return f"""
        You are a customer experience strategist creating a feedback collection system after a major product launch.

        Campaign Context:
        - Name: {campaign_name}
        - Goal: {goal}
        - Main Channels: {', '.join(main_channels)}
        - Offer Details: {offer_details}
        - Target Audience: {', '.join([seg['segment'] for seg in target_audience])}

        Objectives:
        - Collect actionable feedback post-campaign, focusing on QR code redemption experience, satisfaction, and brand impression.
        - Use WhatsApp-first communication (friendly, short-form).
        - Provide rating collection (1–5) and allow optional free-text comments.

        Design:
        - Feedback collection Message Template (for WhatsApp and Email)
        - Three Specific Feedback Questions (aligned with campaign context)
        - Rating Mechanism (WhatsApp tap options)
        - Target Segment Selection Strategy

        Output Structure:
        - WhatsAppMessageTemplate
        - EmailTemplate
        - FeedbackQuestions
        - RatingMechanism
        - TargetSegments
            """



def collect_customer_feedback(campaign_id: str):
    global session

    prompt = build_feedback_prompt(session)
    feedback_plan = generate_choices_with_prompt(prompt)

    print("\nGenerated Customer Feedback Collection Plan:\n")
    for i, plan in enumerate(feedback_plan):
        print(f"Option {i+1}:\n{plan}\n")

    selected_index = int(input("Select your preferred feedback plan (1-3): ")) - 1
    selected_block = feedback_plan[selected_index]
    parsed_feedback_plan = parse_feedback_plan_block(parsed_block)

    save_user_selection_to_db(
        model_name="CustomerFeedback",
        data={
            "campaignId": campaign_id,
            "userId": "SYSTEM_SETUP",
            "interactionId": None,
            "feedbackText": parsed_feedback_plan["whatsapp_message_template"],
            "rating": 0,
            "collectedVia": "Setup",
            "createdAt": datetime.now()
        }
    )

    session["feedback_collection_plan"] = parsed_feedback_plan
    print("\nFeedback collection plan setup saved successfully.")
    return parsed_feedback_plan


def parse_feedback_plan_block(block: str) -> dict:
    """
    Parses feedback plan block from GenAI response
    """
    # Assume block includes WhatsApp message template and questions separated properly
    lines = block.strip().split("\n")
    plan = {
        "whatsapp_message_template": "",
        "email_template": "",
        "feedback_questions": [],
        "rating_mechanism": "",
        "target_segments": []
    }

    current_key = None
    for line in lines:
        if line.startswith("WhatsAppMessageTemplate:"):
            current_key = "whatsapp_message_template"
            plan[current_key] = line.split(":", 1)[1].strip()
        elif line.startswith("EmailTemplate:"):
            current_key = "email_template"
            plan[current_key] = line.split(":", 1)[1].strip()
        elif line.startswith("FeedbackQuestions:"):
            current_key = "feedback_questions"
            plan[current_key] = []
        elif line.startswith("RatingMechanism:"):
            current_key = "rating_mechanism"
            plan[current_key] = line.split(":", 1)[1].strip()
        elif line.startswith("TargetSegments:"):
            current_key = "target_segments"
            plan[current_key] = []
        elif current_key == "feedback_questions" and line.strip():
            plan[current_key].append(line.strip())
        elif current_key == "target_segments" and line.strip():
            plan[current_key].append(line.strip())

    return plan

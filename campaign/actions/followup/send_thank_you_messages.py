from ai import generate_choices_with_prompt
from util import save_user_selection_to_db
from session import session
from datetime import datetime

def send_thank_you_messages(campaign_id: str):
    global session

    campaign_context = f"""
    Campaign Name: {session['campaign_name']}
    Product: {session['product_name']}
    Goal: {session['campaign_goal']}
    Offer: {session['offer_details']}
    Launch Date: {session['launch_date']}
    Target Audience: {', '.join(session['target_segments'])}
    Primary Channels: {', '.join(session['channels'])}
    """

    prompt = f"""
    You are a customer engagement specialist designing post-campaign thank-you messaging.

    {campaign_context}

    Objectives:
    - Thank all participants warmly
    - Personalize differently for:
    1. Buyers: Gratitude + hint about loyalty offers + VIP sneak peek
    2. Non-converters: Thank + nudge with gentle limited-time bonus (e.g., ₹300 extra coupon for 5 days)
    - WhatsApp messages: short, casual
    - Email messages: slightly richer, emotional, relational

    Instructions:
    - WhatsApp max 3 lines, easy to read
    - Email max 6 lines with strong CTA
    - Ensure re-engagement without looking desperate

    Output Needed:
    - WhatsAppMessageBuyer
    - WhatsAppMessageNonConverter
    - EmailTemplateBuyer
    - EmailTemplateNonConverter

    """


    thank_you_plan = generate_choices_with_prompt(prompt)
    print("\nGenerated Thank You Message Plan:\n")
    for i, plan in enumerate(thank_you_plan):
        print(f"Option {i+1}:\n{plan}\n")

    selected_index = int(input("Select your preferred thank you message plan (1-3): ")) - 1
    selected_block = thank_you_plan[selected_index]
    parsed_thank_you_plan = parse_thank_you_plan_block(parsed_block)

    # Save sample setup entries
    for segment, message in parsed_thank_you_plan.items():
        save_user_selection_to_db(
            model_name="ThankYouMessage",
            data={
                "campaignId": campaign_id,
                "userId": "SYSTEM_SETUP",
                "messageBody": message,
                "sentVia": "Setup",
                "segment": segment,
                "sentAt": datetime.now()
            }
        )

    session["thank_you_message_plan"] = parsed_thank_you_plan
    print("\nThank You message plan setup saved successfully.")
    return parsed_thank_you_plan


def parse_thank_you_plan_block(block: str) -> dict:
    """
    Parses thank you message plan structure
    """
    parsed = {
        "Buyer": "",
        "NonConverter": ""
    }
    lines = block.strip().split("\n")
    for line in lines:
        if "WhatsAppMessageBuyer" in line:
            parsed["Buyer"] += line.split(":", 1)[1].strip() + " "
        elif "WhatsAppMessageNonConverter" in line:
            parsed["NonConverter"] += line.split(":", 1)[1].strip() + " "
    return parsed

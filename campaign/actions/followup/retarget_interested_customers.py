from ai import generate_choices_with_prompt
from util import save_user_selection_to_db
from session import session
from datetime import datetime


def build_retargeting_prompt(session):
    campaign_name = session.get("campaign_name", "UrbanNest Campaign")
    main_offer = session.get("main_offer", "₹500 off first purchase above ₹4999")
    feedback_highlights = session.get("feedback_collection_plan", {}).get("summary", "positive feedback from buyers and visitors")
    
    return f"""
        You are a customer retargeting strategist.

        Campaign Context:
        - Campaign Name: {campaign_name}
        - Campaign Offer: {main_offer}
        - Key Observations: {feedback_highlights}

        User Segments:
        - Users who scanned QR but did not checkout
        - Users who interacted with chatbot but did not buy
        - Users who partially added products to cart but did not pay

        Objective:
        - Build a powerful retargeting plan to convert high-intent users.
        - Channels to consider: WhatsApp, Instagram Ads, Facebook Retargeting, Email
        - Offer Options: Continue ₹500 offer OR ₹300 bonus for quick action within 5 days
        - Personalize based on past interaction (if they scanned QR, visited site, abandoned cart).

        Tasks:
        - Identify audience segments and messaging nuances.
        - Create WhatsApp Message Template (for retargeting nudge)
        - Create Instagram Ad Copy Sample
        - Create Facebook Ad Copy Sample
        - Create Reminder Email Template
        - Create UTM tracking recommendations.

        Output Format:
        - AudienceSegments
        - WhatsAppTemplate
        - InstagramAdCopy
        - FacebookAdCopy
        - EmailTemplate
        - UTMRecommendations
        """



def retarget_interested_customers(campaign_id: str):
    global session

    # Build prompt dynamically using session data
    prompt = build_retargeting_prompt(session)

    retargeting_plan = generate_choices_with_prompt(prompt)
    print("\nGenerated Retargeting Plan:\n")
    for i, plan in enumerate(retargeting_plan):
        print(f"Option {i+1}:\n{plan}\n")

    selected_index = int(input("Select your preferred retargeting plan (1-3): ")) - 1
    selected_block = retargeting_plan[selected_index]
    parsed_retargeting_plan = parse_retargeting_block(parsed_block)

    save_user_selection_to_db(
        model_name="RetargetingPlan",
        data={
            "campaignId": campaign_id,
            "audienceSegment": parsed_retargeting_plan["audienceSegment"],
            "retargetingChannel": parsed_retargeting_plan["retargetingChannel"],
            "offerMessage": parsed_retargeting_plan["offerMessage"],
            "scheduledAt": datetime.now()
        }
    )

    session["retargeting_plan"] = parsed_retargeting_plan
    print("\nRetargeting plan setup saved successfully.")
    return parsed_retargeting_plan


def parse_retargeting_block(block: str) -> dict:
    """
    Parses retargeting plan structure
    """
    return {
        "audienceSegment": "Engaged Non-Converters and Partial Checkouts",
        "retargetingChannel": "WhatsApp, Facebook Retargeting Ads, Instagram Stories",
        "offerMessage": block.strip()
    }

from ai import generate_choices_with_prompt
from util import save_user_selection_to_db
from session import session

def enable_real_time_support(campaign_id: str):
    global session

    campaign_product = session.get("campaign_product_name", "UrbanNest Furniture QR Code Promotion")
    campaign_offer = session.get("campaign_offer", "₹500 off on first purchase")
    launch_date = session.get("go_live_date", "10-May-2025")
    target_segments = session.get("target_segments", "Tier-2 City Shoppers")
    campaign_goal = session.get("campaign_goal", "Drive QR redemptions and new customer acquisitions")

    prompt = f"""
    You are a customer experience strategist designing real-time support for a live digital campaign.

    Campaign Context:
    - Product: {campaign_product}
    - Offer: {campaign_offer}
    - Launch Date: {launch_date}
    - Primary Channel: WhatsApp (chatbot + live human escalation)
    - Target Audience: {target_segments}
    - Campaign Objective: {campaign_goal}

    Support Objectives:
    - Ensure instant resolution of basic queries via chatbot (under 3 seconds)
    - Escalate complex issues to human agents within 2 minutes
    - Escalations triggered if chatbot fails to understand after 2 replies, or if user sends keywords like "Help", "Problem", "Agent"
    - Capture Customer Satisfaction (CSAT) score post-resolution
    - Daily monitoring report for unresolved or delayed chats

    Build a structured real-time support plan:
    - Define Interaction Types
    - Define Escalation Triggers
    - Define SLA Monitoring Rules
    - Define CSAT Collection Mechanism
    - Define Daily Support Monitoring Report Structure
    """

    support_plan = generate_choices_with_prompt(prompt)
    print("\nGenerated Real-Time Customer Support Plan:\n")
    for i, plan in enumerate(support_plan):
        print(f"Option {i+1}:\n{plan}\n")

    selected_index = int(input("Select your preferred support plan (1-3): ")) - 1
    selected_block = support_plan[selected_index]
    parsed_support = parse_support_block(selected_block)

    # Save system plan into session
    save_user_selection_to_db(
        model_name="CustomerEngagementLog",
        data={
            "campaignId": campaign_id,
            "userId": "SYSTEM",
            "sessionId": "SUPPORT_SETUP",
            "interactionType": "SupportPlanSetup",
            "message": parsed_support["summary"],
            "resolutionStatus": "Pending",
            "responseTime": 0,
            "csatScore": None
        }
    )

    session["real_time_support_plan"] = parsed_support
    print("\nReal-Time Support System plan saved successfully.")
    return parsed_support


def parse_support_block(block: str) -> dict:
    """
    Parses real-time support plan from AI response.
    """
    return {
        "summary": block.strip()
    }

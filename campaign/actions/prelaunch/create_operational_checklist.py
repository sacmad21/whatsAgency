from ai import generate_choices_with_prompt
from util import get_enterprise_context, save_user_selection_to_db
from session import session
from datetime import datetime, timedelta



def create_operational_checklist(campaign_id: str):
    global session

    # Fetch real campaign context
    primary_channel = session.get("primary_channel", "WhatsApp")
    channels = session.get("channels", [])
    promotion_type = session.get("promotion_type", "")
    creative_assets = session.get("creatives", [])
    media_assets = session.get("media_assets", [])
    integrations = session.get("integrations", {
        "payment_gateway": True,
        "chatbot": True,
        "landing_pages": True,
        "analytics": True,
        "crm": True
    })

    # Create a clean system list for GenAI prompt
    active_systems = []
    if integrations.get("payment_gateway"):
        active_systems.append("Payment Gateway")
    if integrations.get("chatbot"):
        active_systems.append("WhatsApp Chatbot")
    if integrations.get("landing_pages"):
        active_systems.append("Landing Pages")
    if integrations.get("analytics"):
        active_systems.append("Analytics (GA4)")
    if integrations.get("crm"):
        active_systems.append("CRM Integration")
    if "WhatsApp" in channels:
        active_systems.append("WhatsApp Messaging / QR Flow")
    if "Instagram" in channels:
        active_systems.append("Instagram Story Ads")
    if "Facebook Ads" in channels:
        active_systems.append("Facebook Ads Retargeting")

    # Prepare dynamic GenAI prompt
    prompt = f"""
    You are a QA Lead preparing a professional pre-launch operational checklist for a digital campaign.

    Campaign Overview:
    - Promotion Type: {promotion_type}
    - Primary Channel: {primary_channel}
    - Platforms Used: {", ".join(channels)}
    - Active Systems: {", ".join(active_systems)}
    - Campaign Uses QR code redemption on WhatsApp.

    Checklist Quality Requirements:
    - For each checklist item, provide:
        1. System: (specific system like WhatsApp QR Flow, Payment Gateway, Instagram Story Ads)
        2. Checklist Item: (specific verification step)
        3. Expected Outcome: (clearly define success)
        4. Responsibility: (Tech Team, QA Team, Campaign Manager, etc.)
        5. Status: Pending

    Guidelines:
    - Checklist must match actual campaign setup.
    - Allow clear auditing for each item.
    - Include content validation, system responsiveness, user journey smoothness, failure fallback, analytics correctness.

    Output Format:
    System: ...
    Checklist Item: ...
    Expected Outcome: ...
    Responsibility: ...
    Status: Pending
    """

    checklist_items = generate_choices_with_prompt(prompt)
    parsed_items = parse_operational_checklist_block(checklist_items)

    for item in parsed_items:
        save_user_selection_to_db(
            model_name="OperationalChecklist",
            data={
                "campaignId": campaign_id,
                "item": f"{item['system']} - {item['checklist_item']} (Expected: {item['expected_outcome']})",
                "status": item['status']
            }
        )

    session["operational_checklist"] = parsed_items
    print("\nOperational checklist saved successfully.")
    return parsed_items


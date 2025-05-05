from ai import generate_choices_with_prompt
from util import save_user_selection_to_db
from session import session
from datetime import datetime

def build_content_calendar(campaign_id: str):
    global session

    timeline = session.get("timeline", [])
    promo_messages = session.get("promo_messages", {})
    creatives = session.get("creatives", [])
    media_assets = session.get("media_assets", [])

    prompt = f"""
    You are a campaign scheduler.

    Here are the campaign milestones:
    {timeline}

    Available Assets:
    - WhatsApp Promotional Message
    - Instagram Story Ad
    - Facebook Carousel Ad
    - WhatsApp Flyer
    - Animated Instagram Story
    - QR Code Scan GIF (under 5 seconds)

    Build a publishing calendar:
    - Assign each asset to an appropriate date near milestones
    - Suggest WhatsApp broadcasts 1-2 days before and on go-live
    - Retargeting creatives after mid-campaign review
    - End campaign with Thank You + Retarget push

    Format:
    Platform: ...
    AssetType: ...
    AssetReference: ...
    ScheduledAt: ...
    """

    calendar_suggestions = generate_choices_with_prompt(prompt)
    print("\nGenerated Content Calendar Suggestions:\n")
    for i, cal in enumerate(calendar_suggestions):
        print(f"Option {i+1}:\n{cal}\n")

    selected_index = int(input("Select your preferred calendar (1-3): ")) - 1
    selected_block = calendar_suggestions[selected_index]
    parsed_calendar = parse_calendar_block(selected_block)

    for item in parsed_calendar:
        save_user_selection_to_db(
            model_name="ContentCalendar",
            data={
                "campaignId": campaign_id,
                "platform": item["platform"],
                "assetType": item["asset_type"],
                "assetRef": item["asset_reference"],
                "scheduledAt": item["scheduled_at"]
            }
        )

    session["content_calendar"] = parsed_calendar
    print("\nContent Calendar saved successfully.")
    return parsed_calendar


def parse_calendar_block(block: str) -> list:
    """
    Parses AI response structured as platform, asset type, reference, date
    """
    events = []
    lines = block.strip().split("\n")
    current = {}
    for line in lines:
        if line.startswith("Platform:"):
            if current:
                events.append(current)
                current = {}
            current["platform"] = line.split(":", 1)[1].strip()
        elif line.startswith("AssetType:"):
            current["asset_type"] = line.split(":", 1)[1].strip()
        elif line.startswith("AssetReference:"):
            current["asset_reference"] = line.split(":", 1)[1].strip()
        elif line.startswith("ScheduledAt:"):
            date_str = line.split(":", 1)[1].strip()
            current["scheduled_at"] = datetime.strptime(date_str, "%d-%m-%Y")
    if current:
        events.append(current)
    return events

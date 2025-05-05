from ai import generate_choices_with_prompt
from util import get_enterprise_context, get_all_campaign_data, save_user_selection_to_db
from session import session

def prepare_multimedia_assets(campaign_id: str):
    global session

    # Fetch all previously created context
    context = get_enterprise_context(campaign_id)
    full_campaign_data = get_all_campaign_data(campaign_id)  # aggregates from all tables

    business_model = context.get("businessModel")
    audience = full_campaign_data.get("audience_segment", "general audience")
    promotion_type = full_campaign_data.get("promotion_type", "discount")
    offer = full_campaign_data.get("offer_description", "great savings")
    primary_channel = full_campaign_data.get("primary_channel", "WhatsApp")
    promo_messages = full_campaign_data.get("promo_messages", {})
    creative_directions = full_campaign_data.get("creatives", [])

    # Generate extremely thoughtful prompt
    prompt = f"""
    You are a top multimedia creative director building assets for a mobile-first digital campaign.

    Company Model: {business_model}
    Target Audience: {audience}
    Promotion Type: {promotion_type}
    Offer: {offer}
    Primary Channel: {primary_channel}
    Messaging Tone: Friendly and Aspirational with Urgency

    Previously selected creative directions:
    {creative_directions}

    Promotional messages by platform:
    {promo_messages}

    Build 3 multimedia content ideas that:
    - Are highly visual and mobile-friendly
    - Reinforce QR code redemption flow naturally
    - Maximize emotional engagement and easy sharing
    - Fit the attention span of Tier-2 city customers
    - Are optimized under 500 KB file size (or explain if bigger is needed)
    - Match the urgency and excitement tone

    For each idea, structure as:
    - Type: [GIF / Infographic / Animated Video]
    - Title: [Short catchy title]
    - Concept: [Storyline / How it will visually guide users]
    - Engagement Tip: [How it will boost sharing / redemption / excitement]
    - Mobile Optimization Tip: [Frame rate, file size, orientation etc.]
    """

    multimedia_ideas = generate_choices_with_prompt(prompt)
    print("\nGenerated Multimedia Asset Ideas:\n")
    for i, idea in enumerate(multimedia_ideas):
        print(f"Option {i+1}:\n{idea}\n")

    selected_index = int(input("Select your preferred multimedia idea (1-3): ")) - 1
    selected_block = multimedia_ideas[selected_index]
    parsed_assets = parse_multimedia_block(selected_block)

    for asset in parsed_assets:
        save_user_selection_to_db(
            model_name="MediaAsset",
            data={
                "campaignId": campaign_id,
                "type": asset["type"],
                "title": asset["title"],
                "concept": asset["concept"],
                "engagementTip": asset["engagement_tip"],
                "mobileOptimizationTip": asset["mobile_tip"],
                "url": None  # Placeholder, real asset comes later
            }
        )

    session["media_assets"] = parsed_assets
    print("\nMultimedia assets saved successfully.")
    return parsed_assets


def parse_multimedia_block(block: str) -> list:
    """
    Parses OpenAI response to structured MediaAsset list.
    """
    assets = []
    current = {}
    lines = block.strip().split("\n")
    for line in lines:
        if line.startswith("Type:"):
            if current:
                assets.append(current)
                current = {}
            current["type"] = line.split(":", 1)[1].strip()
        elif line.startswith("Title:"):
            current["title"] = line.split(":", 1)[1].strip()
        elif line.startswith("Concept:"):
            current["concept"] = line.split(":", 1)[1].strip()
        elif line.startswith("Engagement Tip:"):
            current["engagement_tip"] = line.split(":", 1)[1].strip()
        elif line.startswith("Mobile Optimization Tip:"):
            current["mobile_tip"] = line.split(":", 1)[1].strip()
    if current:
        assets.append(current)
    return assets

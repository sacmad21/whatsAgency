from ai import generate_choices_with_prompt
from util import get_enterprise_context, save_user_selection_to_db
from session import session

def design_campaign_creatives(campaign_id: str):
    global session

    # Step 1: Fetch all necessary data
    context = get_enterprise_context(campaign_id)
    goal = session.get("campaign_goal")
    promotion_type = session.get("promotion_type")
    offer = session.get("offer_description")
    audience = session.get("audience_segment")
    channels = session.get("channels")
    tone = "Friendly and Aspirational with urgency"
    primary_channel = session.get("primary_channel")

    # Step 2: Generate Dynamic Prompt (Insightful)
    prompt = f"""
    You are a creative director designing visual assets for a sales promotion campaign.

    Context:
    - Company: {context['companyName']} ({context['domain']})
    - Campaign Goal: {goal}
    - Offer: {offer}
    - Promotion Type: {promotion_type}
    - Primary Platform: {primary_channel}
    - Additional Channels: {", ".join(channels)}
    - Audience: {audience}
    - Tone: {tone}

    Generate 3 platform-specific creative plans, one each for:
    - WhatsApp Broadcast Flyer
    - Instagram Story Ad
    - Facebook Carousel Ad

    For each creative, specify:
    - Platform
    - Creative Title
    - Headline Text (hook in 6–8 words)
    - Visual Theme (colors, imagery style)
    - CTA (short action phrase)
    - Mobile Optimization Tip (optimize for Tier-2 city mobile users)

    Focus on practical, emotional triggers (trust, value, urgency).
    Reference all available campaign context.
    """

    creative_ideas = generate_choices_with_prompt(prompt)
    print("\nGenerated Strategic Creative Plans:\n")
    for i, idea in enumerate(creative_ideas):
        print(f"Option {i+1}:\n{idea}\n")

    selected_index = int(input("Select the preferred creative design plan (1-3): ")) - 1
    selected_block = creative_ideas[selected_index]
    parsed_assets = parse_creative_block(selected_block)

    for asset in parsed_assets:
        save_user_selection_to_db(
            model_name="CreativeDesignPlan",
            data={
                "campaignId": campaign_id,
                "platform": asset["platform"],
                "creativeTitle": asset["creative_title"],
                "headline": asset["headline"],
                "visualTheme": asset["visual_theme"],
                "cta": asset["cta"],
                "mobileOptimizationTip": asset["mobile_tip"]
            }
        )

    session["creative_plans"] = parsed_assets
    print("\nCreative design plans saved successfully.")
    return parsed_assets


def parse_creative_block(block: str) -> list:
    """
    Parses LLM output expecting:
    Platform
    Creative Title
    Headline
    Visual Theme
    CTA
    Mobile Tip
    """
    assets = []
    current = {}
    lines = block.strip().split("\n")
    for line in lines:
        if line.startswith("Platform:"):
            if current:
                assets.append(current)
                current = {}
            current["platform"] = line.split(":", 1)[1].strip()
        elif line.startswith("Creative Title:"):
            current["creative_title"] = line.split(":", 1)[1].strip()
        elif line.startswith("Headline:"):
            current["headline"] = line.split(":", 1)[1].strip()
        elif line.startswith("Visual Theme:"):
            current["visual_theme"] = line.split(":", 1)[1].strip()
        elif line.startswith("CTA:"):
            current["cta"] = line.split(":", 1)[1].strip()
        elif line.startswith("Mobile Tip:"):
            current["mobile_tip"] = line.split(":", 1)[1].strip()
    if current:
        assets.append(current)
    return assets

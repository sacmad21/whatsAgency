from ai import generate_choices_with_prompt
from util import get_campaign_full_context, save_user_selection_to_db
from session import session

def write_promotional_messaging(campaign_id: str):
    global session

    # Step 1: Fetch all relevant campaign context
    context = get_campaign_full_context(campaign_id)
    offer = context["offer"]
    audience = context["audience"]
    goal = context["goal"]
    promotion_type = context["promotion_type"]
    primary_channel = context["primary_channel"]
    tone = derive_messaging_tone(audience)

    # Step 2: Create a solid intelligent prompt
    prompt = f"""
    You are a campaign messaging expert.

    Campaign Details:
    - Campaign Goal: {goal}
    - Promotion Type: {promotion_type}
    - Offer: {offer}
    - Target Audience: {audience}
    - Primary Platform: {primary_channel}
    - Tone: {tone}

    Based on this, write 3 highly compelling promotional messages optimized for:
    1. WhatsApp Broadcast (friendly, direct, mobile-optimized)
    2. Instagram Story Ad (aspirational, urgent, swipe-up CTA)
    3. Facebook Carousel Ad (value-focused, community-driven)

    Each message should include:
    - 1 core message (up to 25 words)
    - 1 motivating call-to-action (up to 10 words)

    Ensure emotional hooks, sense of urgency, and trust building.
    """

    message_variants = generate_choices_with_prompt(prompt)
    print("\nGenerated Messaging Options:\n")
    for idx, variant in enumerate(message_variants, 1):
        print(f"Option {idx}:\n{variant}\n")

    selected_index = int(input("Select the preferred messaging option (1-3): ")) - 1
    selected_variant = message_variants[selected_index]
    parsed = parse_promotional_message_variant(selected_variant)

    # Step 3: Save all platform-specific messages to DB
    for platform, content in parsed.items():
        save_user_selection_to_db(
            model_name="PromotionalMessage",
            data={
                "campaignId": campaign_id,
                "platform": platform,
                "tone": tone,
                "message": content["message"],
                "callToAction": content["cta"]
            }
        )

    session["promotional_messages"] = parsed
    print("\nPromotional Messages saved successfully.")
    return parsed

def derive_messaging_tone(audience_segment: str) -> str:
    """
    Simple tone derivation based on audience persona.
    """
    if "young" in audience_segment.lower() or "aspirational" in audience_segment.lower():
        return "Friendly and Aspirational with Urgency"
    else:
        return "Trustworthy and Value-focused"

def parse_promotional_message_variant(block: str) -> dict:
    """
    Parse LLM output expecting:
    WhatsApp Message: ...
    Instagram Message: ...
    Facebook Message: ...
    """
    parsed = {}
    lines = block.strip().split("\n")
    current_platform = None

    for line in lines:
        if "WhatsApp Message:" in line:
            current_platform = "WhatsApp"
            parsed[current_platform] = {"message": line.split(":", 1)[1].strip(), "cta": ""}
        elif "Instagram Message:" in line:
            current_platform = "Instagram"
            parsed[current_platform] = {"message": line.split(":", 1)[1].strip(), "cta": ""}
        elif "Facebook Message:" in line:
            current_platform = "Facebook"
            parsed[current_platform] = {"message": line.split(":", 1)[1].strip(), "cta": ""}
        elif "Call to Action:" in line and current_platform:
            parsed[current_platform]["cta"] = line.split(":", 1)[1].strip()

    return parsed

from ai import generate_choices_with_prompt
from util import prisma_client, save_user_selection_to_db
from session import session

def select_platforms(campaign_id: str):
    global session

    # Step 1: Fetch everything needed DIRECTLY from Prisma tables
    context = prisma_client.enterprisecontext.find_first(where={"campaignId": campaign_id})
    audience = prisma_client.audiencesegment.find_first(where={"campaignId": campaign_id})
    goal = prisma_client.campaignobjective.find_first(where={"campaignId": campaign_id})
    offer = prisma_client.campaignoffer.find_first(where={"campaignId": campaign_id})
    budget = prisma_client.campaignbudget.find_first(where={"campaignId": campaign_id})

    # Defensive defaults in case any is missing
    business_model = context.businessModel if context else "D2C"
    company_name = context.companyName if context else "Brand"
    domain = context.domain if context else "Consumer Goods"

    audience_segment = audience.label if audience else "Urban Youth"
    campaign_goal = goal.goal if goal else "Increase Sales"
    offer_description = offer.description if offer else "₹500 Off QR Coupon"
    total_budget = budget.totalBudget if budget else 1000000  # fallback ₹10 lakh

    # Step 2: Intelligent, Insight-Rich Prompt
    prompt = f"""
    You are a digital sales campaign strategist.

    Company: {company_name}
    Domain: {domain}
    Business Model: {business_model}
    Target Audience: {audience_segment}
    Campaign Goal: {campaign_goal}
    Promotion Type: {session.get('promotion_type')}
    Offer: {offer_description}
    Budget: Approx ₹{total_budget} overall

    Recommend the top 3 digital platforms with:
    - Platform Name (e.g., WhatsApp, Instagram, Facebook)
    - Purpose (Lead Gen, Engagement, Conversion, Retargeting)
    - Message Style (e.g., Story Ad, Broadcast, Carousel Ads)
    - Primary (Yes/No)
    - If Primary, explain WHY this platform should be the main driver.

    Ensure platforms:
    - Are mobile-first
    - Are cost-effective
    - Suit buyers in Tier-2 cities
    - Emphasize WhatsApp if fitting
    """

    options = generate_choices_with_prompt(prompt)
    print("\nSuggested Platform Strategies:\n")
    for i, plan in enumerate(options):
        print(f"Option {i+1}:\n{plan}\n")

    selected_index = int(input("Select your preferred channel plan (1-3): ")) - 1
    selected_block = options[selected_index]
    parsed = parse_channel_block(selected_block)

    # Step 3: Save to Prisma DB
    save_user_selection_to_db(
        model_name="ChannelPlan",
        data={
            "campaignId": campaign_id,
            "channels": parsed["channels"],
            "primary": parsed["primary"],
            "primaryReason": parsed["primary_reason"],
            "messageStyles": parsed["message_styles"]
        }
    )

    # Step 4: Save into global session
    session["channels"] = parsed["channels"]
    session["primary_channel"] = parsed["primary"]
    session["primary_reason"] = parsed["primary_reason"]
    session["message_styles"] = parsed["message_styles"]

    print(f"\nChannel plan saved successfully! Primary platform: {parsed['primary']}")
    return parsed


def parse_channel_block(block: str) -> dict:
    """
    Parser to convert OpenAI structured response into DB fields.
    """
    lines = block.strip().split("\n")
    channels = []
    message_styles = []
    primary = ""
    primary_reason = ""

    for i in range(0, len(lines), 5):
        platform = lines[i].split(":", 1)[1].strip()
        purpose = lines[i+1].split(":", 1)[1].strip()
        message = lines[i+2].split(":", 1)[1].strip()
        is_primary = lines[i+3].split(":", 1)[1].strip().lower() == "yes"
        reason = lines[i+4].split(":", 1)[1].strip() if "Why" in lines[i+4] else ""

        channels.append(platform)
        message_styles.append(message)

        if is_primary:
            primary = platform
            primary_reason = reason

    return {
        "channels": channels,
        "message_styles": message_styles,
        "primary": primary,
        "primary_reason": primary_reason
    }

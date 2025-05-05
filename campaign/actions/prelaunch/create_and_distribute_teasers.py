from ai import generate_choices_with_prompt
from util import get_enterprise_context, save_user_selection_to_db
from session import session
from datetime import datetime, timedelta

def create_and_distribute_teasers(campaign_id: str):
    global session

    # Fetch necessary data
    context = get_enterprise_context(campaign_id)
    offer = session.get("offer_description")
    launch_date = next(
        (item["date"] for item in session.get("timeline", []) if "Go-Live" in item["milestone"]),
        datetime.now() + timedelta(days=15)
    )
    primary_channel = session.get("primary_channel")
    target_segment = session.get("audience_segment")
    promotion_type = session.get("promotion_type")
    teaser_launch_date = launch_date - timedelta(days=2)

    prompt = f"""
    You are a creative strategist for a Tier-2 city-focused D2C campaign.

    Campaign Context:
    - Company Domain: {context['domain']}
    - Business Model: {context['businessModel']}
    - Offer: {offer}
    - Primary Channel: {primary_channel}
    - Target Audience: {target_segment}
    - Promotion Type: {promotion_type}
    - Launch Date: {launch_date.strftime('%d-%m-%Y')}

    Your task:
    - Generate 3 teaser ideas optimized for WhatsApp, Instagram Story, and Facebook Ads.
    - Create different teaser types: 1 Mystery, 1 Countdown, 1 Influencer Hint (optional).
    - Each teaser must include a teaserTheme, a short Message (<150 characters), and clear CTA like "Stay Tuned" or "Unlock the Mystery."
    - Make sure teasers are mobile-first, quick-read friendly for Tier-2 audiences.

    Format your output as:
    1. Platform: ...
       TeaserTheme: ...
       Message: ...
       Recommended Launch Date: {teaser_launch_date.strftime('%d-%m-%Y')}
    """

    teaser_suggestions = generate_choices_with_prompt(prompt)
    print("\nGenerated Teaser Suggestions:\n")
    for i, teaser in enumerate(teaser_suggestions):
        print(f"Option {i+1}:\n{teaser}\n")

    selected_index = int(input("Select your preferred teaser plan (1-3): ")) - 1
    selected_block = teaser_suggestions[selected_index]
    parsed_teasers = parse_teaser_block(selected_block)

    for teaser in parsed_teasers:
        save_user_selection_to_db(
            model_name="TeaserContent",
            data={
                "campaignId": campaign_id,
                "message": teaser["message"],
                "platform": teaser["platform"],
                "teaserTheme": teaser["teaser_theme"],
                "scheduledAt": teaser_launch_date
            }
        )

    session["teasers"] = parsed_teasers
    print("\n✅ Teaser content saved successfully to DB.")
    return parsed_teasers


def parse_teaser_block(block: str) -> list:
    """
    Parses AI teaser block expecting structure:
    Platform: ...
    TeaserTheme: ...
    Message: ...
    Recommended Launch Date: ...
    """
    teasers = []
    current = {}
    lines = block.strip().split("\n")
    for line in lines:
        if line.startswith("Platform:"):
            if current:
                teasers.append(current)
                current = {}
            current["platform"] = line.split(":", 1)[1].strip()
        elif line.startswith("TeaserTheme:"):
            current["teaser_theme"] = line.split(":", 1)[1].strip()
        elif line.startswith("Message:"):
            current["message"] = line.split(":", 1)[1].strip()
    if current:
        teasers.append(current)
    return teasers

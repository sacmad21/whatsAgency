from ai import generate_choices_with_prompt
from util import save_user_selection_to_db, get_enterprise_context
from session import session
from datetime import datetime, timedelta

def engage_influencers(campaign_id: str):
    global session

    # Fetch campaign context
    context = get_enterprise_context(campaign_id)
    audience = session.get("audience_segment", "General Audience")
    promotion_type = session.get("promotion_type")
    offer = session.get("offer_description")
    primary_channel = session.get("primary_channel", "WhatsApp")
    launch_date = next(
        (item["date"] for item in session.get("timeline", []) if "Go-Live" in item["milestone"]),
        datetime.now() + timedelta(days=15)
    )
    teaser_launch_date = launch_date - timedelta(days=2)

    # Highly Thoughtful Dynamic Prompt
    prompt = f"""
    You are an influencer marketing strategist for a digital furniture brand campaign.

    Campaign Details:
    - Business Model: {context.get('businessModel')}
    - Audience: {audience}
    - Promotion Type: {promotion_type}
    - Offer: {offer}
    - Primary Channel: {primary_channel}
    - Launch Date: {launch_date.strftime('%d-%m-%Y')}
    - Teaser Phase: Start teasing 2 days before launch.

    Objective:
    - Build strong excitement before the launch
    - Drive QR-code scans and ₹500 offer redemptions
    - Focus on Tier-2 city audiences (Indore, Nashik, Bhopal)

    Requirements:
    - Suggest 3 influencer collaboration plans.
    - Each plan should include:
      - Influencer Name (conceptual; example names)
      - Platform (Instagram, YouTube, WhatsApp Community)
      - Post Type (Story, Reel, Static Post, Group Post)
      - Expected Impact (eg: Build Curiosity, Drive Swipes, Initiate Conversations)
      - Suggested Post Date (during teaser or launch)

    Be creative, practical, and specific. Tie influencer activity closely to the QR code offer and campaign urgency.

    Format:
    1. Influencer Name: ...
       Platform: ...
       Post Type: ...
       Expected Impact: ...
       Suggested Post Date: ...
    """

    influencer_ideas = generate_choices_with_prompt(prompt)
    print("\nGenerated Influencer Collaboration Ideas:\n")
    for i, idea in enumerate(influencer_ideas):
        print(f"Option {i+1}:\n{idea}\n")

    selected_index = int(input("Select your preferred influencer plan (1-3): ")) - 1
    selected_block = influencer_ideas[selected_index]
    parsed_influencers = parse_influencer_block(selected_block)

    for infl in parsed_influencers:
        save_user_selection_to_db(
            model_name="InfluencerPlan",
            data={
                "campaignId": campaign_id,
                "influencerName": infl["influencer_name"],
                "platform": infl["platform"],
                "postType": infl["post_type"],
                "expectedImpact": infl["expected_impact"],
                "scheduledAt": infl["scheduled_at"]
            }
        )

    session["influencers"] = parsed_influencers
    print("\nInfluencer plans saved successfully.")
    return parsed_influencers


def parse_influencer_block(block: str) -> list:
    """
    Parses AI-generated structured influencer plans
    """
    influencers = []
    current = {}
    lines = block.strip().split("\n")
    for line in lines:
        if "Influencer Name:" in line:
            if current:
                influencers.append(current)
                current = {}
            current["influencer_name"] = line.split(":", 1)[1].strip()
        elif "Platform:" in line:
            current["platform"] = line.split(":", 1)[1].strip()
        elif "Post Type:" in line:
            current["post_type"] = line.split(":", 1)[1].strip()
        elif "Expected Impact:" in line:
            current["expected_impact"] = line.split(":", 1)[1].strip()
        elif "Suggested Post Date:" in line:
            date_str = line.split(":", 1)[1].strip()
            current["scheduled_at"] = datetime.strptime(date_str, "%d-%m-%Y")
    if current:
        influencers.append(current)
    return influencers

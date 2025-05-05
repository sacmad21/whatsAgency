from ai import generate_choices_with_prompt
from util import get_full_campaign_context, save_user_selection_to_db
from session import session
from datetime import datetime, timedelta

def create_campaign_timeline(campaign_id: str):
    global session

    # Step 1: Fetch full campaign context intelligently
    context = get_full_campaign_context(campaign_id)
    today = datetime.now()
    default_launch_gap = 15  # Days from today
    expected_launch_date = today + timedelta(days=default_launch_gap)

    # Step 2: Highly Thoughtful Dynamic Prompt
    prompt = f"""
    You are a professional project manager designing a sales promotion campaign for {context['companyName']}.

    Business Model: {context['businessModel']}
    Campaign Goal: {context['campaignGoal']}
    Target Audience: {context['targetAudience']}
    Promotion Type: {context['promotionType']}
    Offer: {context['offerDescription']}
    Offer Limit: {context['offerLimit']} redemptions
    Budget: ₹{context['budget']['total']} total (Media, Creative, Incentives, Logistics)
    Primary Channel: {context['primaryChannel']}
    Secondary Channels: {", ".join(context['secondaryChannels'])}

    Today's Date: {today.strftime('%d-%m-%Y')}
    Target Launch Date: {expected_launch_date.strftime('%d-%m-%Y')}

    Build a project execution timeline for this campaign. 
    - Suggest 6-8 intelligent milestones.
    - Space them logically (consider creative production, system setup, QA, approvals, influencer collaboration).
    - Plan Mid-campaign review and Post-campaign learning phases also.

    For each milestone, clearly mention:
    - Milestone Name
    - Milestone Type (categorize it: Planning, Execution, QA, Launch, Monitoring, Closing)
    - Planned Date (realistic)
    """

    options = generate_choices_with_prompt(prompt)
    print("\nGenerated Campaign Timeline Options:\n")
    for i, plan in enumerate(options):
        print(f"Option {i+1}:\n{plan}\n")

    selected_index = int(input("Select your preferred timeline (1-3): ")) - 1
    selected_block = options[selected_index]
    parsed_milestones = parse_timeline_block(selected_block)

    # Save each milestone to Prisma DB
    for milestone in parsed_milestones:
        save_user_selection_to_db(
            model_name="CampaignTimeline",
            data={
                "campaignId": campaign_id,
                "milestoneName": milestone["name"],
                "milestoneType": milestone["type"],
                "plannedDate": milestone["date"]
            }
        )

    session["timeline"] = parsed_milestones
    print(f"\n✅ Campaign Timeline milestones saved successfully.")
    return parsed_milestones


def parse_timeline_block(block: str) -> list:
    """
    Parses AI structured output for timeline milestones.
    """
    lines = block.strip().split("\n")
    milestones = []
    current = {}

    for line in lines:
        if "Milestone Name:" in line:
            current["name"] = line.split(":", 1)[1].strip()
        elif "Milestone Type:" in line:
            current["type"] = line.split(":", 1)[1].strip()
        elif "Planned Date:" in line:
            date_str = line.split(":", 1)[1].strip()
            current["date"] = datetime.strptime(date_str, "%d-%m-%Y")
            milestones.append(current)
            current = {}

    return milestones

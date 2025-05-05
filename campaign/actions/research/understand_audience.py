from ai import generate_choices_with_prompt
from util import get_enterprise_context, save_user_selection_to_db
from session import session
import re
def understand_audience(campaign_id: str):
    global session

    # Step 1: Fetch campaign and context
    context = get_enterprise_context(campaign_id)
    goal = session.get("campaign_goal")


    # Step 2: AI Prompt to generate audience segments
    prompt = f"""
    You are a customer segmentation strategist for a sales promotion campaign.

    Company Name: {context['companyName']}
    Domain: {context['domain']}
    Business Model: {context['businessModel']}
    Key Challenge: {context['currentPain']}
    Campaign Goal: {goal}

    Based on this, generate 3 detailed audience segments that the campaign should target.
    Each of the 3 audience segments must include following data. Each key value pair seperated with : and pairs are seperated with comma.
        - Segment (e.g., 'Tier-2 Aspirational Buyers')
        - Demographics (e.g. '18 to 30 years old married house wifes')
        - OnlineBehavior (e.g. 'people who keep scrolling the amazon and flipkart but don't buy things')
        - PainPoints (e.g. 'confused wiht lot of choices available on the internet about essentials things'
    
    """


    audience_segments = generate_choices_with_prompt(prompt, "understand audience for sales promotion")
    session["audience_segments"] = audience_segments

    print("\nSuggested Target Audience Segments:\n")
    for i, seg in enumerate(audience_segments):
        print(f"{i+1}. {seg}")

    selected_index = int(input("\nSelect the best audience segment (1-3): ")) - 1
    selected_segment = audience_segments[selected_index]

    # Step 3: Store final structured segment in DB
    data = parse_audience_segment(selected_segment)

    save_user_selection_to_db(
        model_name="AudienceSegment",
        data={
            "campaignId": campaign_id,
            "label": data["segment"],
            "demographics": data["demographics"],
            "behavior": data["onlinebehavior"],
            "painPoints": data["painpoints"]
        }
    )

    print("\nAudience Segment Saved:", data )
    session["audience_segment"] = selected_segment
    return selected_segment


def parse_audience_segment(raw: str) -> tuple:
    """
    Dummy parser – in production, use LLM structured format.
    Expects each segment formatted like:
    'Label: ..., Demographics: ..., Behavior: ..., Pain Points: ...'
    """
    print("\n Parsed Output --------------------------------- ")
    fields = {}

    raw = re.sub(r"^\s*GROUP\s*\d+:\s*", "", raw.strip(), flags=re.IGNORECASE)
    
    for line in raw.strip().split(","):
        if ":" in line:
            key, val = line.split(":", 1)
            key = re.sub(r"^\d+[\.\)\-]*\s*", "", key) 
            fields[key.strip().lower().replace(" ", "_")] = val.strip()
            print(key,"-->",val)

    return fields

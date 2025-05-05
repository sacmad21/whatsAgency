from ai import generate_choices_with_prompt
from util import get_enterprise_context, save_user_selection_to_db
from session import session

def determine_offer(campaign_id: str):
    global session

    # Step 1: Fetch all needed context
    context = get_enterprise_context(campaign_id)
    goal = session.get("campaign_goal")
    audience = session.get("audience_segment")
    promotion_type = session.get("promotion_type")
    competitor = session.get("competitor_strategy", {}).get("promotion_type", "N/A")
    business_model = context.get("businessModel", "online business")

    # Step 2: Create intelligent prompt
    prompt = f"""
    You are a senior campaign strategist for a {business_model}.

    Context:
    - Campaign Goal: {goal}
    - Target Audience Segment: {audience}
    - Promotion Type Selected: {promotion_type}
    - Competitor's Strategy Observed: {competitor}

    Your task is to create 3 compelling offer ideas that:
    - Strongly support the campaign goal.
    - Emotionally connect with the target audience.
    - Differentiate clearly from competitor strategy.
    - Are executable within a {business_model} setup.
    - Contain clear offer limits (e.g., "first 500 customers", "valid for 7 days only").
    - Define measurable success criteria (KPIs).
    - Suggest a backup offer plan in case the main offer underperforms.

    Structure your response strictly like this:
    ---
    1. Offer Description:
       Offer Limit:
       Offer Type:
       Success Criteria:
       Backup Offer:
    """

    offer_options = generate_choices_with_prompt(prompt)
    session["offer_options"] = offer_options

    # Step 3: Display options
    print("\nGenerated Offer Options (with success criteria and backup plans):\n")
    for i, offer in enumerate(offer_options):
        print(f"Option {i+1}:\n{offer}\n")

    selected_index = int(input("Select the best offer (1-3): ")) - 1
    selected_offer = offer_options[selected_index]
    parsed = parse_offer_block(selected_offer)

    # Step 4: Save structured output to DB
    save_user_selection_to_db(
        model_name="CampaignOffer",
        data={
            "campaignId": campaign_id,
            "description": parsed["description"],
            "offerLimit": parsed["limit"],
            "offerType": parsed["type"],
            "successCriteria": parsed["success_criteria"],
            "backupOffer": parsed["backup_offer"]
        }
    )

    session["offer_description"] = parsed["description"]
    session["offer_limit"] = parsed["limit"]
    session["offer_type"] = parsed["type"]
    session["offer_success_criteria"] = parsed["success_criteria"]
    session["backup_offer"] = parsed["backup_offer"]

    print(f"\nSaved Offer: {parsed['description']} with Success Criteria: {parsed['success_criteria']}")
    return parsed


def parse_offer_block(block: str) -> dict:
    """
    Parses Offer block into structured dictionary.
    """
    lines = block.split("\n")
    parsed = {}
    for line in lines:
        if "Offer Description:" in line:
            parsed["description"] = line.split(":", 1)[1].strip()
        elif "Offer Limit:" in line:
            parsed["limit"] = int(''.join(filter(str.isdigit, line)))
        elif "Offer Type:" in line:
            parsed["type"] = line.split(":", 1)[1].strip()
        elif "Success Criteria:" in line:
            parsed["success_criteria"] = line.split(":", 1)[1].strip()
        elif "Backup Offer:" in line:
            parsed["backup_offer"] = line.split(":", 1)[1].strip()
    return parsed

from ai import generate_choices_with_prompt
from util import get_enterprise_context, get_audience_segment, save_user_selection_to_db
from session import session
import re

def choose_promotion_type(campaign_id: str):
    global session

    # Step 1: Context from DB and session
    context = get_enterprise_context(campaign_id)
    business_model = context.get("businessModel")
    geography = get_audience_segment(campaign_id).get("demographics", "target market")
    goal = session.get("campaign_goal")
    competitor_promo = session.get("competitor_strategy", {}).get("promotion_type", "N/A")

    # Step 2: Dynamic Prompt
    prompt = f"""
    You are a digital commerce strategist planning a sales promotion campaign.

    Campaign Goal: {goal}
    Business Model: {business_model}
    Target Geography: {geography}
    Competitor's Promotion Type: {competitor_promo}

    Based on this, generate 3 detailed promotion types that the campaign should include.
    Each of the 3 promotion types must include following data. Each key value pair seperated with : and pairs are seperated with comma.
        1. PromotionType: (name of the promotion type)
        2. Description: (brief explanation of the mechanism)
        3. Working: (What is it's working ? How it aligns with the customer segment, channel, and goal)
        4. SuccessCriteria: (Measurable outcome e.g., “Reduce cart abandonment by 25% within 2 weeks”]
    """


    response_blocks = generate_choices_with_prompt(prompt,"choose promotion type for campaign")
    session["promotion_type_options"] = response_blocks


    # Print options for selection
    print("\nGenerated Promotion Options with Success Criteria:\n")
    for i, block in enumerate(response_blocks):
        print(f"Option {i+1}-------------------\n{block}\n")


    selected_index = int(input("Select the best promotion type (1-3): ")) - 1
    selected_block = response_blocks[selected_index]
    parsed = parse_promotion_block(selected_block)

    # Save to DB
    save_user_selection_to_db(
        model_name="PromotionType",
        data={
            "campaignId": campaign_id,
            "type": parsed["promotiontype"]
        }
    )

    session["promotion_type"] = parsed["promotiontype"]
    session["promotion_success_criteria"] = parsed["successcriteria"]
    print(f"\nSaved Promotion Type: {parsed['promotiontype']}")
    print(f"Expected Success: {parsed['successcriteria']}")
    return parsed


def parse_promotion_block(raw: str) -> dict:
    """
    Parse AI response with expected keys:
    Promotion Type: ...
    Description: ...
    Why It Works: ...
    Success Criteria: ...
    """
    print("\n Parsed Output of :: " + raw)
    fields = {}

    raw = re.sub(r"^GROUP\s*\d+:\s*", "", raw.strip(), flags=re.IGNORECASE)
    
    for line in raw.strip().split(","):
        if ":" in line:
            key, val = line.split(":", 1)
            key = re.sub(r"^\d+[\.\)\-]*\s*", "", key)
            key = key.strip().lower().replace(" ", "_") 
            fields[key] = val.strip()
            print(key,"-->",val)
    return fields

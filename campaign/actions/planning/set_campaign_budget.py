from ai import generate_choices_with_prompt
from util import get_enterprise_context, get_audience_segment, save_user_selection_to_db
from session import session

def set_campaign_budget(campaign_id: str):
    global session

    # Step 1: Gather context
    context = get_enterprise_context(campaign_id)
    business_model = context.get("businessModel")
    geography = get_audience_segment(campaign_id).get("demographics", "Target market")
    goal = session.get("campaign_goal")
    promotion_type = session.get("promotion_type")
    offer = session.get("offer_description")
    offer_limit = session.get("offer_limit")
    competitor = session.get("competitor_strategy", {}).get("promotion_type", "N/A")

    # Step 2: Build thorough dynamic prompt
    prompt = f"""
    You are acting as a financial strategist for a sales promotion campaign.

    Campaign Overview:
    - Company Business Model: {business_model}
    - Target Geography and Audience: {geography}
    - Campaign Goal: {goal}
    - Chosen Promotion Type: {promotion_type}
    - Offer Details: {offer}
    - Offer Redemption Limit: {offer_limit}
    - Competitor's Observed Promotion Type: {competitor}

    Based on the above, provide 3 detailed budget breakdown options.

    Each option must include:
    - Media Spend (ads, influencers, WhatsApp marketing)
    - Creative Spend (visuals, landing page design, video content)
    - Incentive Spend (cost of offers, discounts, rewards)
    - Logistics Spend (delivery, fulfillment, support costs)
    - Total Budget

    Additionally, calculate and include:
    - Estimated Cost per Customer Acquired (Total Budget / Expected redemptions)
    - Expected ROI percentage if campaign achieves 80% of target redemptions

    Format response like:

    Option X:
    Media Spend: ₹xxx
    Creative Spend: ₹xxx
    Incentive Spend: ₹xxx
    Logistics Spend: ₹xxx
    Total Budget: ₹xxx
    Cost per Customer: ₹xxx
    Expected ROI: xx%

    Provide thoughtful and practical estimates based on Tier-2 economics in India.
    """

    budget_options = generate_choices_with_prompt(prompt)
    session["budget_options"] = budget_options

    # Step 3: Present to User
    print("\nGenerated Budget Options (Deeply Thoughtful):\n")
    for i, budget in enumerate(budget_options):
        print(f"Option {i+1}:\n{budget}\n")

    selected_index = int(input("Select the preferred budget option (1-3): ")) - 1
    selected_budget_block = budget_options[selected_index]
    parsed = parse_budget_block(selected_budget_block)

    save_user_selection_to_db(
        model_name="CampaignBudget",
        data={
            "campaignId": campaign_id,
            "mediaSpend": parsed["media_spend"],
            "creativeSpend": parsed["creative_spend"],
            "incentiveSpend": parsed["incentive_spend"],
            "logisticsSpend": parsed["logistics_spend"],
            "totalBudget": parsed["total_budget"],
            "costPerCustomer": parsed["cost_per_customer"],
            "expectedROI": parsed["expected_roi"],
            "notes": parsed["notes"]
        }
    )

    session["campaign_budget"] = parsed
    print(f"\nBudget saved successfully! Total Budget: ₹{parsed['total_budget']} (Expected ROI: {parsed['expected_roi']}%)")
    return parsed


def parse_budget_block(block: str) -> dict:
    """
    Parse structured AI budget response.
    """
    import re

    values = {}
    lines = block.strip().split("\n")
    for line in lines:
        if "Media Spend" in line:
            values["media_spend"] = float(re.sub(r"[^\d.]", "", line))
        elif "Creative Spend" in line:
            values["creative_spend"] = float(re.sub(r"[^\d.]", "", line))
        elif "Incentive Spend" in line:
            values["incentive_spend"] = float(re.sub(r"[^\d.]", "", line))
        elif "Logistics Spend" in line:
            values["logistics_spend"] = float(re.sub(r"[^\d.]", "", line))
        elif "Total Budget" in line:
            values["total_budget"] = float(re.sub(r"[^\d.]", "", line))
        elif "Cost per Customer" in line:
            values["cost_per_customer"] = float(re.sub(r"[^\d.]", "", line))
        elif "Expected ROI" in line:
            values["expected_roi"] = float(re.sub(r"[^\d.]", "", line))
    values["notes"] = "Generated via AI based on campaign context."
    return values

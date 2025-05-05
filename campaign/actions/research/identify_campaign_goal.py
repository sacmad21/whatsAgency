from ai import generate_choices_with_prompt
from util import get_enterprise_context, save_user_selection_to_db
from session import session
import asyncio


def identify_campaign_goal(campaign_id: str):
    global session
    print("Campaign Id :" + campaign_id)
    # Step 1: Fetch enterprise context
    
    context = get_enterprise_context(campaign_id)
    print("Enterprise context :", context)
    company = context.get("companyName")
    domain = context.get("domain")
    model = context.get("businessModel")
    background = context.get("background")
    problem = context.get("currentPain")
    strategic_goals = context.get("goals", "")

    # Step 2: Craft deeply insightful prompt
    prompt = f"""
    You are a growth strategist designing a Sales Promotion Campaign for a company named '{company}'.

    Company Domain: {domain}
    Business Model: {model}
    Background: {background}
    Key Challenge: {problem}
    Strategic Goals (if any): {strategic_goals}

    Based on this business context, generate 3 deeply strategic, measurable campaign goals that align with the company's business problem and objectives. 
    Each goal must be:
    - Specific to {domain}
    - Realistic for a sales promotion campaign
    - Aligned with either customer acquisition, conversion uplift, market expansion, or lead engagement.

    Format each goal clearly and succinctly.
    """


    goals =  generate_choices_with_prompt(prompt, topic="sales promotion campaign goals")
    session["goal_options"] = goals

    # Step 3: Present options to user
    print("\nBased on enterprise insights, here are 3 strategic campaign goal options:\n")
    for i, g in enumerate(goals):
        print(f"{i+1}. {g}")
    choice = int(input("\nSelect the most suitable goal (1-3): ")) - 1

    selected_goal = goals[choice]
    session["campaign_goal"] = selected_goal

    # Step 4: Persist selected goal
    save_user_selection_to_db(
        model_name="CampaignObjective",
        data={
            "campaignId": campaign_id,
            "goal": selected_goal
        }
    )

    print(f"\nSelected Goal Saved: {selected_goal}")
    return selected_goal

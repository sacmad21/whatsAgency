from ai import generate_choices_with_prompt
from util import save_user_selection_to_db
from session import session
from datetime import datetime

def document_key_learnings(campaign_id: str):
    global session

    prompt = f"""
    [INSERT FINALIZED DYNAMIC PROMPT ABOVE]
    """

    learnings_plan = generate_choices_with_prompt(prompt)
    print("\nGenerated Campaign Learnings Summary:\n")
    for i, plan in enumerate(learnings_plan):
        print(f"Option {i+1}:\n{plan}\n")

    selected_index = int(input("Select your preferred learning summary (1-3): ")) - 1
    selected_block = learnings_plan[selected_index]
    parsed_learnings = parse_learnings_block(selected_block)

    save_user_selection_to_db(
        model_name="CampaignLearnings",
        data={
            "campaignId": campaign_id,
            "whatWorked": parsed_learnings["whatWorked"],
            "whatDidNotWork": parsed_learnings["whatDidNotWork"],
            "bestPractices": parsed_learnings["bestPractices"],
            "improvementAreas": parsed_learnings["improvementAreas"],
            "createdAt": datetime.now()
        }
    )

    session["campaign_learnings"] = parsed_learnings
    print("\nCampaign Learnings saved successfully.")
    return parsed_learnings


def parse_learnings_block(block: str) -> dict:
    """
    Parses campaign learnings structure
    """
    return {
        "whatWorked": block.get("WhatWorked", "").strip(),
        "whatDidNotWork": block.get("WhatDidNotWork", "").strip(),
        "bestPractices": block.get("BestPractices", "").strip(),
        "improvementAreas": block.get("ImprovementAreas", "").strip(),
    }

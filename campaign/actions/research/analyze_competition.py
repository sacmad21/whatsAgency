from ai import generate_choices_with_prompt
from util import get_enterprise_context, save_user_selection_to_db
from session import session
import re


def analyze_competition(campaign_id: str):
    global session

    context = get_enterprise_context(campaign_id)
    company = context["companyName"]
    domain = context["domain"]
    goal = session.get("campaign_goal")
    segment = session.get("audience_segment")

    prompt = f"""
            You are a competitive strategy analyst. Generate 3 competitors of {company} as per the recent sales promotion campaigns 
            run by the domain '{domain}' that target segments similar to '{segment}'.

            Each the 3 competitors must include following data. Each key value pair seperated with : and pairs are seperated with comma.
                1. Competitor:
                2. Campaign:
                3. PromotionType: (e.g., Flash Sale, Coupon Code, Loyalty Cashback)
                4. Channels: (e.g., Instagram, WhatsApp, Website)
                5. Strength:(why the campaign worked well)
                6. Weakness: (what could be improved or gaps)

                
            Format the output clearly for storage and selection.

            Kindly ensure the names of all keys should be as at least one of following prisma model.            
            """

    competitors = generate_choices_with_prompt(prompt,"analyze competition in sales promotion campaign")
    session["competitor_strategies"] = competitors

    print("\nSuggested Competitor Campaign Snapshots:\n")
    for i, comp in enumerate(competitors):
        print(f"{i+1}. {comp}\n")

    selected_index = int(input("Select the most relevant competitor case (1-3): ")) - 1
    selected = competitors[selected_index]
    parsed = parse_competitor_strategy(selected)

    save_user_selection_to_db(
        model_name="CompetitorStrategy",
        data= {
            "campaignId": campaign_id,
            "competitor": parsed["competitor"],
            "promotionType": parsed["promotiontype"],
            "channels": parsed["channels"],
            "strength": parsed["strength"],
            "weakness": parsed["weakness"]
        }
    )

    print(f"\nCompetitor Strategy Saved: {parsed['competitor']}")
    session["competitor_strategy"] = parsed
    return parsed



def parse_competitor_strategy(raw: str) -> dict:
    """
    Dummy structured parser (for structured LLM response).
    Expected format:
    Competitor: ...
    Promotion Type: ...
    Channels: ...
    Strength: ...
    Weakness: ...
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


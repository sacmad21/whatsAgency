from ai import generate_choices_with_prompt
from util import get_enterprise_context, save_user_selection_to_db
from session import session
from datetime import datetime

def run_compliance_checklist(campaign_id: str):
    global session

    context = get_enterprise_context(campaign_id)

    # Gather all available session data
    business_model = context.get("businessModel")
    campaign_goal = session.get("campaign_goal")
    offer = session.get("offer_description")
    promotion_type = session.get("promotion_type")
    audience = session.get("audience_segment")
    platforms = session.get("channels")
    success_criteria = session.get("promotion_success_criteria", "Achieve sales lift / engagement growth")
    timeline_summary = ", ".join([item["milestone"] for item in session.get("timeline", [])])
    budget = session.get("budget", {}).get("total", 0)

    # Generate dynamic prompt
    prompt = f"""
    You are a Digital Campaign Compliance Officer for a sales promotion campaign.

    Campaign Details:
    - Company Business Model: {business_model}
    - Campaign Goal: {campaign_goal}
    - Offer Description: {offer}
    - Promotion Type: {promotion_type}
    - Target Geography and Audience: {audience}
    - Primary and Secondary Channels: {', '.join(platforms)}
    - Platform Usage: {', '.join(platforms)}
    - Success Criteria: {success_criteria}
    - Launch Timeline: {timeline_summary}
    - Total Budget: ₹{budget}

    Create a comprehensive compliance checklist that ensures:
    - Adherence to Indian Consumer Protection laws
    - Adherence to WhatsApp and Instagram Advertising Policies
    - Data Privacy Compliance for WhatsApp interactions
    - Clear disclosures (e.g., "Limited seats", "First 1000 customers only")
    - Financial disclaimers (if cashback/discounts involved)
    - Brand Guidelines compliance (tone of communication, logos)
    - Offer Validity and Redemption Terms

    Each checklist item must include:
    - Compliance Item (short and crisp)
    - Severity: Critical / Major / Minor
    - Responsible Department: Legal / Marketing / Product / Finance
    - Immediate Action Required: Yes / No

    Format strictly as:
    Compliance Item: ...
    Severity: ...
    Responsible Department: ...
    Immediate Action Required: ...
    """

    # Step 1: Generate checklist items
    checklist_blocks = generate_choices_with_prompt(prompt)

    print("\nGenerated Compliance Checklist:\n")
    for i, block in enumerate(checklist_blocks):
        print(f"Option {i+1}:\n{block}\n")

    # Step 2: User selects the compliance set
    selected_index = int(input("Select the compliance checklist to proceed with (1-3): ")) - 1
    selected_block = checklist_blocks[selected_index]

    parsed_items = parse_compliance_block(selected_block)

    # Step 3: Save each item to DB
    for item in parsed_items:
        save_user_selection_to_db(
            model_name="ComplianceChecklist",
            data={
                "campaignId": campaign_id,
                "item": item["item"],
                "severity": item["severity"],
                "responsibleDepartment": item["responsible"],
                "status": "Pending"
            }
        )

    session["compliance"] = parsed_items
    print("\nCompliance checklist saved successfully.")
    return parsed_items


def parse_compliance_block(block: str) -> list:
    """
    Parses block like:
    Compliance Item: ...
    Severity: ...
    Responsible Department: ...
    Immediate Action Required: ...
    """
    lines = block.strip().split("\n")
    items = []
    current_item = {}

    for line in lines:
        if "Compliance Item:" in line:
            current_item["item"] = line.split(":", 1)[1].strip()
        elif "Severity:" in line:
            current_item["severity"] = line.split(":", 1)[1].strip()
        elif "Responsible Department:" in line:
            current_item["responsible"] = line.split(":", 1)[1].strip()
        elif "Immediate Action Required:" in line:
            current_item["action_required"] = line.split(":", 1)[1].strip()
            items.append(current_item)
            current_item = {}

    return items

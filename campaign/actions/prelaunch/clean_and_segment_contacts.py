from ai import generate_choices_with_prompt
from util import get_enterprise_context, save_user_selection_to_db
from session import session

def clean_and_segment_contacts(campaign_id: str):
    global session

    context = get_enterprise_context(campaign_id)
    offer = session.get("offer_description")
    launch_date = next(
        (item["date"] for item in session.get("timeline", []) if "Go-Live" in item["milestone"]),
        None
    )
    primary_channel = session.get("primary_channel")
    audience = session.get("audience_segment", "Tier-2 City Young Professionals")

    prompt = f"""
    You are an advanced CRM strategist.

    Here are details of an upcoming campaign:
    - Offer: {offer}
    - Launch Date: {launch_date.strftime('%d-%m-%Y') if launch_date else 'TBD'}
    - Target Audience: {audience}
    - Primary Platform: {primary_channel}
    - Promotion Style: WhatsApp QR code discount
    - Tone: Friendly, Aspirational, Urgent

    Your task:
    - Segment customers based on behavioral readiness, purchase history, and location.
    - Clean the list by removing users inactive in the last 90 days.
    - Recommend 3 segments creatively named but highly actionable.

    For each segment, provide:
    - Segment Name
    - Criteria (short description of segmentation logic)
    - Approximate Count

    Format:
    1. Segment Name: ...
       Criteria: ...
       Approximate Count: ...
    """

    segments = generate_choices_with_prompt(prompt)
    print("\nGenerated Customer Segments:\n")
    for i, seg in enumerate(segments):
        print(f"Option {i+1}:\n{seg}\n")

    selected_index = int(input("Select your preferred segmentation plan (1-3): ")) - 1
    selected_block = segments[selected_index]
    parsed_segments = parse_segment_block(selected_block)

    for seg in parsed_segments:
        save_user_selection_to_db(
            model_name="CustomerSegmentList",
            data={
                "campaignId": campaign_id,
                "segment": seg["name"],
                "criteria": seg["criteria"],
                "count": seg["count"]
            }
        )

    session["customer_segments"] = parsed_segments
    print("\nCustomer segments saved successfully.")
    return parsed_segments


def parse_segment_block(block: str) -> list:
    """
    Parse advanced AI response into structured segments
    """
    segments = []
    current = {}
    lines = block.strip().split("\n")
    for line in lines:
        if "Segment Name:" in line:
            if current:
                segments.append(current)
                current = {}
            current["name"] = line.split(":", 1)[1].strip()
        elif "Criteria:" in line:
            current["criteria"] = line.split(":", 1)[1].strip()
        elif "Approximate Count:" in line:
            current["count"] = int(''.join(filter(str.isdigit, line)))
    if current:
        segments.append(current)
    return segments

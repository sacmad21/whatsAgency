from ai import generate_choices_with_prompt
from util import save_user_selection_to_db
from session import session
from datetime import datetime

def activate_campaign_on_all_platforms(campaign_id: str):
    global session

    campaign_goal = session.get("campaign_goal", "Drive QR code redemptions and new customer signups")
    campaign_offer = session.get("offer_description", "₹500 off via QR scan on first furniture purchase")
    target_audience = session.get("target_audience", "Tier-2 city young homeowners")
    launch_date = next(
        (item["date"] for item in session.get("timeline", []) if "Go-Live" in item["milestone"]), 
        datetime.now()
    ).strftime("%d-%m-%Y")
    customer_segments = ", ".join([seg["segment"] for seg in session.get("customer_segments", [])])

    prompt = f"""
        You are a digital marketing campaign launch specialist.

        You are activating the following campaign:

        Campaign Details:
        - Goal: {campaign_goal}
        - Offer: {campaign_offer}
        - Target Audience: {target_audience}
        - Launch Date: {launch_date}
        - Major Customer Segments: {customer_segments}
        - Platforms: WhatsApp, Instagram, Facebook (Content calendar available)

        Instructions:
        - For each platform and asset:
        - Define the asset to be activated
        - Confirm if correct UTM tracking is embedded
        - Define 3-point verification checklist after activation (e.g., link open check, analytics event firing, message delivery rate)
        - Define success criteria for the activation (e.g., message delivered to 95% of recipients, ad approved within 2 hours)

        Quality Expectations:
        - Activation must be traceable and measurable
        - Any missing parameters or verification gaps must be flagged
        - Recommendations for immediate corrective actions if activation fails

        Output Structure:
        Platform: ...
        AssetType: ...
        AssetReference: ...
        ActivationTime: ...
        TrackingParameters: ...
        VerificationChecklist: ...
        SuccessCriteria: ...

    """

    activation_plan = generate_choices_with_prompt(prompt)
    print("\nGenerated Activation Plans:\n")
    for i, plan in enumerate(activation_plan):
        print(f"Option {i+1}:\n{plan}\n")

    selected_index = int(input("Select your preferred activation plan (1-3): ")) - 1
    selected_block = activation_plan[selected_index]
    parsed_activations = parse_activation_block(selected_block)

    for act in parsed_activations:
        save_user_selection_to_db(
            model_name="CampaignActivation",
            data={
                "campaignId": campaign_id,
                "platform": act["platform"],
                "assetType": act["asset_type"],
                "assetReference": act["asset_reference"],
                "activationTime": act["activation_time"],
                "trackingParameters": act["tracking_parameters"],
                "verificationChecklist": act["verification_checklist"],
                "successCriteria": act["success_criteria"],
                "status": "Scheduled",
                "activationResult": ""
            }
        )

    session["campaign_activation"] = parsed_activations
    print("\nCampaign activation entries saved successfully.")
    return parsed_activations


def parse_activation_block(block: str) -> list:
    """
    Parses detailed activation block with tracking and verification
    """
    activations = []
    current = {}
    lines = block.strip().split("\n")
    for line in lines:
        if line.startswith("Platform:"):
            if current:
                activations.append(current)
                current = {}
            current["platform"] = line.split(":", 1)[1].strip()
        elif line.startswith("AssetType:"):
            current["asset_type"] = line.split(":", 1)[1].strip()
        elif line.startswith("AssetReference:"):
            current["asset_reference"] = line.split(":", 1)[1].strip()
        elif line.startswith("ActivationTime:"):
            ts = line.split(":", 1)[1].strip()
            current["activation_time"] = datetime.strptime(ts, "%d-%m-%Y %H:%M")
        elif line.startswith("TrackingParameters:"):
            current["tracking_parameters"] = line.split(":", 1)[1].strip()
        elif line.startswith("VerificationChecklist:"):
            current["verification_checklist"] = line.split(":", 1)[1].strip()
        elif line.startswith("SuccessCriteria:"):
            current["success_criteria"] = line.split(":", 1)[1].strip()
    if current:
        activations.append(current)
    return activations

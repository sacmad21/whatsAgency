from ai import generate_choices_with_prompt
from util import save_user_selection_to_db
from session import session
from datetime import datetime

def analyze_campaign_metrics(campaign_id: str):
    global session

    # Fetch aggregated metrics from session or DB
    total_impressions = session["performance_summary"]["impressions"]
    total_clicks = session["performance_summary"]["clicks"]
    total_qr_scans = session["performance_summary"]["qr_scans"]
    total_conversions = session["performance_summary"]["conversions"]
    avg_csat = session["performance_summary"]["csat_score_average"]
    escalation_rate = session["performance_summary"]["escalation_rate"]

    prompt = f"""
    [INSERT FINALIZED PROMPT ABOVE dynamically with actual values]
    """

    analysis_plan = generate_choices_with_prompt(prompt)
    print("\nGenerated Campaign Analysis Plan:\n")
    for i, plan in enumerate(analysis_plan):
        print(f"Option {i+1}:\n{plan}\n")

    selected_index = int(input("Select your preferred analysis summary (1-3): ")) - 1
    selected_block = analysis_plan[selected_index]
    parsed_analysis = parse_analysis_block(selected_block)

    revenue_generated = total_conversions * 6000  # Assume avg order ₹6000
    campaign_spend = 200000  # Assume ₹2 lakh
    roi = round(((revenue_generated - campaign_spend) / campaign_spend) * 100, 2)
    conversion_rate = round((total_conversions / total_clicks) * 100, 2)
    engagement_rate = round((total_clicks / total_impressions) * 100, 2)

    save_user_selection_to_db(
        model_name="CampaignAnalysisReport",
        data={
            "campaignId": campaign_id,
            "totalImpressions": total_impressions,
            "totalClicks": total_clicks,
            "totalQrScans": total_qr_scans,
            "totalConversions": total_conversions,
            "conversionRate": conversion_rate,
            "revenueGenerated": revenue_generated,
            "campaignSpend": campaign_spend,
            "roi": roi,
            "engagementRate": engagement_rate,
            "csatAverage": avg_csat,
            "escalationRate": escalation_rate,
            "learningsSummary": parsed_analysis["summary"],
            "createdAt": datetime.now()
        }
    )

    session["campaign_analysis_report"] = parsed_analysis
    print("\nCampaign Analysis Report saved successfully.")
    return parsed_analysis


def parse_analysis_block(block: str) -> dict:
    """
    Parses campaign analysis block structure
    """
    return {
        "summary": block.strip()
    }

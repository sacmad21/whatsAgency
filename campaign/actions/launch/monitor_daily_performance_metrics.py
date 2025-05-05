from ai import generate_choices_with_prompt
from util import save_user_selection_to_db
from session import session
from datetime import datetime

def monitor_daily_performance_metrics(campaign_id: str):
    global session

    campaign_name = session.get("campaign_name", "Unknown Brand")
    offer_description = session.get("offer_description", "Special Offer")
    timeline = session.get("timeline", [])
    primary_channels = session.get("primary_channels", [])
    customer_segments = session.get("customer_segments", [])
    support_plan = session.get("real_time_support_plan", {}).get("summary", "No support plan found")

    prompt = f"""
        You are a Campaign Performance Analyst for a live product promotion campaign.

        Campaign Details (dynamic context):
        - Brand: {campaign_name}
        - Offer: {offer_description}
        - Launch Date: {timeline}
        - Primary Channels: {primary_channels}
        - Customer Segments Targeted: {customer_segments}
        - Support Setup: {support_plan}
        - Goal: Maximize QR scans and first-time purchases

        Objectives:
        - Daily auto-track KPIs across WhatsApp, Instagram, Facebook, Support system.
        - Identify any anomalies using smart thresholds.
        - Flag risk areas early (SLA breaches, low conversions, poor CSAT).

        Build the following:
        - List of Daily KPIs to track
        - Suggested thresholds for anomaly detection
        - CSAT and SLA Monitoring strategy
        - Daily reporting format (for dashboard and export)

        **Examples of anomalies:**
        - >20% drop in conversions day-over-day
        - Escalation rate >25%
        - Bot SLA response failures >5%
        - CSAT average score falls below 3.5

        Output Structure:
        - KPIs
        - Anomaly Detection Rules
        - Daily Reporting Format
        - SLA Monitoring Recommendations
    """

    monitoring_plan = generate_choices_with_prompt(prompt)
    print("\nGenerated Daily Monitoring and Anomaly Detection Plan:\n")
    for i, plan in enumerate(monitoring_plan):
        print(f"Option {i+1}:\n{plan}\n")

    selected_index = int(input("Select your preferred monitoring plan (1-3): ")) - 1
    selected_block = monitoring_plan[selected_index]
    parsed_monitoring = parse_monitoring_block(selected_block)

    save_user_selection_to_db(
        model_name="PerformanceReport",
        data={
            "campaignId": campaign_id,
            "date": datetime.now(),
            "impressions": 0,
            "clicks": 0,
            "qrScans": 0,
            "conversions": 0,
            "chatbotSessions": 0,
            "escalations": 0,
            "escalationRate": 0.0,
            "avgBotResponseTime": 0,
            "avgHumanResponseTime": 0,
            "csatScoreAverage": 0.0,
            "anomalies": "Monitoring Initialized"
        }
    )

    session["performance_monitoring_plan"] = parsed_monitoring
    print("\nDaily Monitoring Setup Completed Successfully.")
    return parsed_monitoring


def parse_monitoring_block(block: str) -> dict:
    """
    Parses the monitoring plan text into dictionary
    """
    return {
        "summary": block.strip()
    }

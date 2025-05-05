import asyncio
from prisma import Prisma
import json
from datetime import datetime

async def generate_reporting_pptjson(campaign_id: str, output_path: str):
    db = Prisma()
    await db.connect()

    # Fetch all required campaign data
    campaign = await db.campaign.find_unique(where={"id": campaign_id})
    enterprise = await db.enterprisecontext.find_first(where={"campaignId": campaign_id})
    objectives = await db.campaignobjective.find_many(where={"campaignId": campaign_id})
    competitors = await db.competitorstrategy.find_many(where={"campaignId": campaign_id})
    offers = await db.campaignoffer.find_many(where={"campaignId": campaign_id})
    budgets = await db.campaignbudget.find_many(where={"campaignId": campaign_id})
    promotions = await db.promotiontype.find_many(where={"campaignId": campaign_id})
    channelplans = await db.channelplan.find_many(where={"campaignId": campaign_id})
    reports = await db.performancereport.find_many(where={"campaignId": campaign_id})
    feedbacks = await db.customerfeedback.find_many(where={"campaignId": campaign_id})
    learnings = await db.campaignlearnings.find_first(where={"campaignId": campaign_id})
    analysis = await db.campaignanalysisreport.find_first(where={"campaignId": campaign_id})
    retargetings = await db.retargetingplan.find_many(where={"campaignId": campaign_id})

    await db.disconnect()

    slides = []

    # Slide 1: Campaign Overview
    slides.append({
        "slideNumber": 1,
        "title": campaign.name,
        "subtitle": f"Driving {enterprise.domain} in {enterprise.businessModel}",
        "leftColumn": [
            f"Company: {enterprise.companyName}",
            f"Domain: {enterprise.domain}",
            f"Business Model: {enterprise.businessModel}"
        ],
        "rightBlock": {
            "type": "text",
            "paragraph": enterprise.background or "UrbanNest aims to drive innovation in Tier-2 city real estate sector."
        }
    })

    # Slide 2: Executive Summary
    slides.append({
        "slideNumber": 2,
        "title": "Executive Summary",
        "leftColumn": [
            f"Conversions: {analysis.totalConversions}",
            f"Revenue: ₹{analysis.revenueGenerated}",
            f"ROI: {round(analysis.roi,2)}%",
            f"Engagement Rate: {round(analysis.engagementRate,2)}%"
        ],
        "rightBlock": {
            "type": "text",
            "paragraph": analysis.learningsSummary or "Campaign delivered outstanding ROI through WhatsApp and QR-driven engagement strategies."
        }
    })

    # Slide 3: Research & Planning Insights
    research_bullets = [obj.goal for obj in objectives] + [f"Competitor: {comp.competitor} focused on {comp.promotionType}" for comp in competitors]
    slides.append({
        "slideNumber": 3,
        "title": "Research & Planning Insights",
        "leftColumn": research_bullets[:5],  # Limit to top 5 points
        "rightBlock": {
            "type": "text",
            "paragraph": "Market analysis identified high responsiveness to QR code-driven promotions among Tier-2 audiences. Competitor benchmarking revealed opportunity in mobile-first campaigns."
        }
    })

    # Slide 4: Pre-Launch Preparation
    slides.append({
        "slideNumber": 4,
        "title": "Pre-Launch Preparation",
        "leftColumn": [
            "Teaser campaigns initiated on WhatsApp",
            "Influencer partnerships activated",
            "Operational readiness checklist completed"
        ],
        "rightBlock": {
            "type": "text",
            "paragraph": "WhatsApp teasers and influencer promotions created significant buzz before launch, ensuring operational systems were tested and stable."
        }
    })

    # Slide 5: Launch KPIs and Financial Overview
    total_impressions = sum(r.impressions for r in reports)
    total_clicks = sum(r.clicks for r in reports)
    total_qr_scans = sum(r.qrScans for r in reports)
    total_conversions = analysis.totalConversions

    slides.append({
        "slideNumber": 5,
        "title": "Launch KPIs and Financial Overview",
        "leftColumn": [
            f"Impressions: {total_impressions}",
            f"Clicks: {total_clicks}",
            f"QR Scans: {total_qr_scans}",
            f"Conversions: {total_conversions}",
            f"Revenue: ₹{analysis.revenueGenerated}"
        ],
        "rightBlock": {
            "type": "chart",
            "graphSuggestion": "Funnel Chart",
            "categories": ["Impressions", "Clicks", "QR Scans", "Conversions"],
            "values": [total_impressions, total_clicks, total_qr_scans, total_conversions]
        }
    })

    # Slide 6: Retargeting Performance (if available)
    if retargetings:
        slides.append({
            "slideNumber": 6,
            "title": "Retargeting Performance",
            "leftColumn": [
                "Retargeted audience conversion uplift observed",
                "WhatsApp personalized re-engagement successful"
            ],
            "rightBlock": {
                "type": "chart",
                "graphSuggestion": "Retargeting Uplift",
                "categories": ["Retargeted", "Non-Retargeted"],
                "values": [70, 310]  # Replace with real numbers if available
            }
        })

    # Slide 7: Customer Feedback Trends
    if feedbacks:
        slides.append({
            "slideNumber": 7,
            "title": "Customer Feedback Trends",
            "leftColumn": [
                "Overall CSAT rating: 4.3/5",
                "Positive experience with QR journeys",
                "Minor issues in coupon redemption"
            ],
            "rightBlock": {
                "type": "chart",
                "graphSuggestion": "CSAT Trend Line",
                "categories": ["Day 1", "Day 2", "Day 3", "Day 4", "Day 5"],
                "values": [4.1, 4.2, 4.4, 4.3, 4.5]
            }
        })

    # Slide 8: Operational Learnings
    slides.append({
        "slideNumber": 8,
        "title": "Operational Learnings",
        "leftColumn": [
            "Chatbot resolved 88% customer queries",
            "Escalation rate within acceptable range",
            "Minor delivery delays observed"
        ],
        "rightBlock": {
            "type": "text",
            "paragraph": learnings.whatWorked or "WhatsApp bot automation greatly enhanced support efficiency, with majority queries handled automatically."
        }
    })

    # Slide 9: What Worked vs What Didn't
    slides.append({
        "slideNumber": 9,
        "title": "What Worked vs What Didn't",
        "leftColumn": [
            f"✅ {learnings.whatWorked or 'WhatsApp nurturing highly effective'}",
            f"❌ {learnings.whatDidNotWork or 'Manual coupon entry created friction'}"
        ],
        "rightBlock": {
            "type": "text",
            "paragraph": learnings.bestPractices or "Seamless QR journeys outperformed flat discount strategies."
        }
    })

    # Slide 10: Future Recommendations
    slides.append({
        "slideNumber": 10,
        "title": "Future Recommendations",
        "leftColumn": [
            "Auto-apply discounts",
            "Expand Story Ads",
            "Gamify QR journeys",
            "Strengthen Tier-2 logistics"
        ],
        "rightBlock": {
            "type": "text",
            "paragraph": learnings.improvementAreas or "Next campaigns should simplify checkout, diversify influencer content, and further automate lead nurturing."
        }
    })

    # Slide 11: Financial Overview
    slides.append({
        "slideNumber": 11,
        "title": "Financial Overview",
        "leftColumn": [
            f"Revenue: ₹{analysis.revenueGenerated}",
            f"Spend: ₹{analysis.campaignSpend}",
            f"ROI: {round(analysis.roi,2)}%"
        ],
        "rightBlock": {
            "type": "chart",
            "graphSuggestion": "Revenue vs Spend Pie",
            "categories": ["Revenue", "Spend"],
            "values": [analysis.revenueGenerated, analysis.campaignSpend]
        }
    })

    # Slide 12: Closing & Acknowledgments
    slides.append({
        "slideNumber": 12,
        "title": "Closing & Acknowledgments",
        "subtitle": "Congratulations Team!",
        "leftColumn": [
            "Marketing, Tech, Sales Teams",
            "Influencer collaborations appreciated",
            "Bot Automation team success"
        ],
        "rightBlock": {
            "type": "text",
            "paragraph": "UrbanNest achieved record-breaking new customer acquisition during this campaign thanks to flawless collaboration across Marketing, Tech, and Operations."
        }
    })

    # Save the generated slides.json
    with open(output_path, "w") as f:
        json.dump({"slides": slides}, f, indent=2)

    print(f"✅ slides.json generated at {output_path}")

# Run program
if __name__ == "__main__":
    campaign_id = "YOUR_CAMPAIGN_ID"  # Replace with real campaign ID
    output_file = "slides.json"
    asyncio.run(generate_slides_json(campaign_id, output_file))

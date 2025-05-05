from ai import generate_single_choice_with_prompt
from util import save_user_selection_to_db
from prisma import Prisma
from datetime import datetime


def build_dynamic_prompt(campaign, objectives, offers, budget, channels, performance_reports, feedbacks, analysis, learnings, retargeting, extension):
    # Summarize key inputs
    objective_summary = ", ".join([obj.goal for obj in objectives])
    offer_summary = ", ".join([off.description for off in offers])
    performance_summary = f"""
    Total Impressions: {sum(r.impressions for r in performance_reports)}
    Total Clicks: {sum(r.clicks for r in performance_reports)}
    Total Conversions: {sum(r.conversions for r in performance_reports)}
    Average CSAT: {round(sum(r.csatScoreAverage for r in performance_reports) / len(performance_reports), 2)}
    """

    feedback_summary = f"Sample feedback: {feedbacks[0].feedbackText}" if feedbacks else "No feedback collected."

    retargeting_summary = f"{len(retargeting)} retargeting programs executed." if retargeting else "No retargeting performed."

    extension_summary = f"Stock clearance extended to {extension.extendedTo.date()}" if extension else "No extension."

    # Create powerful executive dynamic prompt
    return f"""
        You are an enterprise campaign analyst and presentation specialist.

        Create a 12-slide professional internal campaign report for:
        - Brand: UrbanNest Furniture
        - Campaign Name: {campaign.name}
        - Duration: {campaign.startDate.date()} to {campaign.endDate.date()}

        Campaign Objectives:
        - {objective_summary}

        Offer Highlights:
        - {offer_summary}

        Channel Strategy:
        - Primary Channel: {channels.primary}
        - Channels used: {", ".join(channels.channels)}

        Budget:
        - Total Budget Allocated: ₹{budget.totalBudget}
        - Cost per Customer: ₹{budget.costPerCustomer}

        Performance Summary:
        {performance_summary}

        Customer Feedback:
        {feedback_summary}

        Learnings Summary:
        - What Worked: {learnings.whatWorked}
        - What Didn't Work: {learnings.whatDidNotWork}

        Retargeting Summary:
        - {retargeting_summary}

        Extension Summary:
        - {extension_summary}

        Requirements:
        - Executive Summary
        - Research Stage Learnings
        - Campaign Planning Highlights
        - Offer Strategy
        - Channel Strategy
        - Launch Phase KPIs
        - Retargeting Performance
        - Customer Feedback Insights
        - Operational Learnings
        - Recommendations
        - Graphs: Impressions Trend, Conversions Funnel, CSAT Trend, ROI Pie Chart
        - Be visually creative: use infographics, clean diagrams, data-driven storytelling.

        Output JSON structure:
        - executiveSummary
        - kpiHighlights
        - learningHighlights
        - improvementAreas
        - graphsReference (describe recommended graphs)

        Language should be professional, crisp, visionary.

        """


async def prepare_creative_internal_report_dynamic(campaign_id: str):
    client = Prisma()
    await client.connect()

    # Fetch all dynamic data
    campaign = await client.campaign.find_unique(where={"id": campaign_id})
    objectives = await client.campaignobjective.find_many(where={"campaignId": campaign_id})
    offers = await client.campaignoffer.find_many(where={"campaignId": campaign_id})
    budget = await client.campaignbudget.find_first(where={"campaignId": campaign_id})
    channels = await client.channelplan.find_first(where={"campaignId": campaign_id})
    performance_reports = await client.performancereport.find_many(where={"campaignId": campaign_id})
    feedbacks = await client.customerfeedback.find_many(where={"campaignId": campaign_id})
    analysis = await client.campaignanalysisreport.find_first(where={"campaignId": campaign_id})
    learnings = await client.campaignlearnings.find_first(where={"campaignId": campaign_id})
    retargeting = await client.retargetingplan.find_many(where={"campaignId": campaign_id})
    extension = await client.campaignextensionplan.find_first(where={"campaignId": campaign_id})

    await client.disconnect()

    # Dynamically construct prompt
    prompt = build_dynamic_prompt(campaign, objectives, offers, budget, channels, performance_reports, feedbacks, analysis, learnings, retargeting, extension)

    # Generate creative internal report
    slides = generate_single_choice_with_prompt(prompt)

    # Save into DB
    save_user_selection_to_db(
        model_name="InternalCampaignReport",
        data={
            "campaignId": campaign_id,
            "reportTitle": f"{campaign.name} - Internal Campaign Report",
            "executiveSummary": slides["executiveSummary"],
            "kpiHighlights": slides["kpiHighlights"],
            "learningHighlights": slides["learningHighlights"],
            "improvementAreas": slides["improvementAreas"],
            "graphsReference": slides.get("graphsReference", None),
            "createdAt": datetime.now()
        }
    )

    return slides

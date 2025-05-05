import json
import os
import sys

# Automatically add the project root to sys.path
current_file = os.path.abspath(__file__)
print("Current file :: " , current_file)
project_root = os.path.abspath(os.path.join(current_file, "../../"))  # Adjust depth as needed
if project_root not in sys.path:
    sys.path.insert(0, project_root)


from datetime import datetime
from db import client
import asyncio

# ======= GENERAL UTILITIES =======

def safe_json_dump(data: dict, file_path: str):
    """
    Dumps Python dict safely to JSON file with proper formatting.
    """
    try:
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        print(f"✅ JSON saved successfully at: {file_path}")
    except Exception as e:
        print(f"⚠️ Failed to save JSON: {e}")

def safe_json_load(file_path: str) -> dict:
    """
    Loads JSON safely from file.
    """
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        print(f"✅ JSON loaded successfully from: {file_path}")
        return data
    except Exception as e:
        print(f"⚠️ Failed to load JSON: {e}")
        return {}

def format_currency(amount: float) -> str:
    """
    Formats a float into Indian currency format ₹.
    Example: 2280000.00 -> ₹22,80,000.00
    """
    return f"₹{amount:,.2f}"

def format_date(date_obj: datetime) -> str:
    """
    Formats a datetime object into a standard readable date.
    Example: 2025-05-01 -> 01-May-2025
    """
    return date_obj.strftime("%d-%b-%Y")

def fallback_paragraph(topic: str) -> str:
    """
    Provides a basic fallback paragraph if GenAI API call fails.
    """
    return f"This section summarizes the {topic} based on campaign activities and results."

# ======= PRISMA DB UTILITIES =======

def get_enterprise_context(campaign_id: str):
    context = asyncio.run(_get_enterprise_context(campaign_id))
    return context.dict() 

def get_audience_segment(campaign_id: str):
    context = asyncio.run(_get_audience_segment(campaign_id))
    return context.dict() 

async def _get_audience_segment(campaign_id: str):
    """
    Fetches EnterpriseContext object for a campaign.
    """
    await  client.connect()

    context =  await client.audiencesegment.find_first(where={"campaignId": campaign_id})

    await client.disconnect()
    
    return context


async def _get_enterprise_context(campaign_id: str):
    """
    Fetches EnterpriseContext object for a campaign.
    """
    await  client.connect()

    context =  await client.enterprisecontext.find_first(where={"campaignId": campaign_id})

    await client.disconnect()
    
    return context

async def get_all_campaign_data(campaign_id: str):
    """
    Fetches all key campaign data models at once.
    Returns dictionary with all needed entities.
    """
    client.connect()
    db = client 

    campaign = await db.campaign.find_unique(where={"id": campaign_id})
    enterprise = await db.enterprisecontext.find_first(where={"campaignId": campaign_id})
    objectives = await db.campaignobjective.find_many(where={"campaignId": campaign_id})
    competitors = await db.competitorstrategy.find_many(where={"campaignId": campaign_id})
    offers = await db.campaignoffer.find_many(where={"campaignId": campaign_id})
    budgets = await db.campaignbudget.find_many(where={"campaignId": campaign_id})
    promotions = await db.promotiontype.find_many(where={"campaignId": campaign_id})
    channels = await db.channelplan.find_many(where={"campaignId": campaign_id})
    timelines = await db.campaigntimeline.find_many(where={"campaignId": campaign_id})
    compliances = await db.compliancechecklist.find_many(where={"campaignId": campaign_id})
    creatives = await db.creativeasset.find_many(where={"campaignId": campaign_id})
    reports = await db.performancereport.find_many(where={"campaignId": campaign_id})
    feedbacks = await db.customerfeedback.find_many(where={"campaignId": campaign_id})
    learnings = await db.campaignlearnings.find_first(where={"campaignId": campaign_id})
    analysis = await db.campaignanalysisreport.find_first(where={"campaignId": campaign_id})
    retargetings = await db.retargetingplan.find_many(where={"campaignId": campaign_id})
    extensions = await db.campaignextensionplan.find_many(where={"campaignId": campaign_id})
    activations = await db.campaignactivation.find_many(where={"campaignId": campaign_id})
    thankyou = await db.thankyoumessage.find_many(where={"campaignId": campaign_id})

    db.disconnect()



    return {
        "campaign": campaign,
        "enterprise": enterprise,
        "objectives": objectives,
        "competitors": competitors,
        "offers": offers,
        "budgets": budgets,
        "promotions": promotions,
        "channels": channels,
        "timelines": timelines,
        "compliances": compliances,
        "creatives": creatives,
        "reports": reports,
        "feedbacks": feedbacks,
        "learnings": learnings,
        "analysis": analysis,
        "retargetings": retargetings,
        "extensions": extensions,
        "activations": activations,
        "thankyou": thankyou
    }


def save_user_selection_to_db(model_name: str, data: dict):
    asyncio.run(_save_user_selection_to_db(model_name, data))


async def _save_user_selection_to_db(model_name: str, data: dict):
    """
    Saves user selection to Prisma database dynamically based on model_name.
    """
    await client.connect()
    db = client

    try:
        if model_name == "CompetitorStrategy":
            await db.competitorstrategy.create(data=data)
        elif model_name == "EnterpriseContext":
            await db.enterprisecontext.create(data=data)
        elif model_name == "AudienceSegment":
            await db.audiencesegment.create(data=data)
        elif model_name == "CampaignObjective":
            await db.campaignobjective.create(data=data)
        elif model_name == "TargetAudienceSegment":
            await db.targetaudiencesegment.create(data=data)
        elif model_name == "PromotionType":
            await db.promotiontype.create(data=data)
        elif model_name == "CampaignOffer":
            await db.campaignoffer.create(data=data)
        elif model_name == "CampaignBudget":
            await db.campaignbudget.create(data=data)
        elif model_name == "ChannelPlan":
            await db.channelplan.create(data=data)
        elif model_name == "CampaignTimeline":
            await db.campaigntimeline.create(data=data)
        elif model_name == "ComplianceChecklist":
            await db.compliancechecklist.create(data=data)
        elif model_name == "PromotionalMessage":
            await db.promotionalmessage.create(data=data)
        elif model_name == "CreativeDesignPlan":
            await db.creativedesignplan.create(data=data)
        elif model_name == "CreativeAsset":
            await db.creativeasset.create(data=data)
        elif model_name == "MediaAsset":
            await db.mediaasset.create(data=data)
        elif model_name == "ContentCalendar":
            await db.contentcalendar.create(data=data)
        elif model_name == "TeaserContent":
            await db.teasercontent.create(data=data)
        elif model_name == "CustomerSegmentList":
            await db.customersegmentlist.create(data=data)
        elif model_name == "InfluencerPlan":
            await db.influencerplan.create(data=data)
        elif model_name == "OperationalChecklist":
            await db.operationalchecklist.create(data=data)
        elif model_name == "CampaignActivation":
            await db.campaignactivation.create(data=data)
        elif model_name == "CustomerEngagementLog":
            await db.customerengagementlog.create(data=data)
        elif model_name == "PerformanceReport":
            await db.performancereport.create(data=data)
        elif model_name == "CustomerFeedback":
            await db.customerfeedback.create(data=data)
        elif model_name == "ThankYouMessage":
            await db.thankyoumessage.create(data=data)
        elif model_name == "RetargetingPlan":
            await db.retargetingplan.create(data=data)
        elif model_name == "CampaignExtensionPlan":
            await db.campaignextensionplan.create(data=data)
        elif model_name == "CampaignAnalysisReport":
            await db.campaignanalysisreport.create(data=data)
        elif model_name == "CampaignLearnings":
            await db.campaignlearnings.create(data=data)
        elif model_name == "InternalCampaignReport":
            await db.internalcampaignreport.create(data=data)
        else:
            raise Exception(f"Unknown model name: {model_name}")

        print(f"✅ User selection saved to {model_name}")

    except Exception as e:
        print(f"⚠️ Failed to save user selection to DB: {e}")
    finally:
        await db.disconnect()





# Stage to model mapping based on user-provided JSON
stage_model_mapping = {
    "Research and Objective Setting": [
        "CampaignObjective", "TargetAudienceSegment", "CompetitorStrategy", "PromotionType"
    ],
    "Campaign Planning": [
        "CampaignOffer", "CampaignBudget", "ChannelPlan", "CampaignTimeline", "ComplianceChecklist"
    ],
    "Content Creation and Design": [
        "PromotionalMessage", "CreativeAsset", "MediaAsset", "ContentCalendar"
    ],
    "Pre-Launch Phase": [
        "TeaserContent", "CustomerSegmentList", "InfluencerPlan", "OperationalChecklist"
    ],
    "Campaign Launch": [
        "CampaignActivation", "CustomerEngagementLog", "PerformanceReport"
    ],
    "Post-Launch Follow-Up": [
        "CustomerFeedback", "ThankYouMessage", "RetargetingPlan", "CampaignExtensionPlan"
    ],
    "Campaign Analysis": [
        "CampaignAnalysisReport", "CampaignLearnings", "InternalCampaignReport"
    ]
}


def generate_db_fetch_function(stage_name: str, model_names: list) -> str:
    func_name = f"get_{stage_name.lower().replace(' ', '_')}_data"
    lines = [f"async def {func_name}(campaign_id: str):",
             f'    """',
             f"    Fetches data for stage: {stage_name}",
             f'    """',
             f"    await client.connect()",
             f"    db = client", ""]

    for model in model_names:
        instance_name = model.lower()
        if model in ["CampaignAnalysisReport", "CampaignLearnings", "InternalCampaignReport"]:
            lines.append(f"    {instance_name} = await db.{instance_name}.find_first(where={{\"campaignId\": campaign_id}})")
        else:
            lines.append(f"    {instance_name} = await db.{instance_name}.find_many(where={{\"campaignId\": campaign_id}})")
    lines.append("\n    await db.disconnect()\n")
    lines.append("    return {")
    for model in model_names:
        instance_name = model.lower()
        lines.append(f"        \"{instance_name}\": {instance_name},")
    lines.append("    }")
    return "\n".join(lines)



async def get_research_and_objective_setting_data(campaign_id: str):
    """
    Fetches data for stage: Research and Objective Setting
    """
    await client.connect()
    db = client

    campaignobjective = await db.campaignobjective.find_many(where={"campaignId": campaign_id})
    audiencesegment = await db.audiencesegment.find_many(where={"campaignId": campaign_id})
    competitorstrategy = await db.competitorstrategy.find_many(where={"campaignId": campaign_id})
    promotiontype = await db.promotiontype.find_many(where={"campaignId": campaign_id})

    await db.disconnect()

    return {
        "campaignobjective": campaignobjective,
        "audiencesegment": audiencesegment,
        "competitorstrategy": competitorstrategy,
        "promotiontype": promotiontype,
    }



async def get_campaign_planning_data(campaign_id: str):
    """
    Fetches data for stage: Campaign Planning
    """
    await client.connect()
    db = client

    campaignoffer = await db.campaignoffer.find_many(where={"campaignId": campaign_id})
    campaignbudget = await db.campaignbudget.find_many(where={"campaignId": campaign_id})
    channelplan = await db.channelplan.find_many(where={"campaignId": campaign_id})
    campaigntimeline = await db.campaigntimeline.find_many(where={"campaignId": campaign_id})
    compliancechecklist = await db.compliancechecklist.find_many(where={"campaignId": campaign_id})

    await db.disconnect()

    return {
        "campaignoffer": campaignoffer,
        "campaignbudget": campaignbudget,
        "channelplan": channelplan,
        "campaigntimeline": campaigntimeline,
        "compliancechecklist": compliancechecklist,
    }




async def get_content_creation_and_design_data(campaign_id: str):
    """
    Fetches data for stage: Content Creation and Design
    """
    await client.connect()
    db = client

    promotionalmessage = await db.promotionalmessage.find_many(where={"campaignId": campaign_id})
    creativeasset = await db.creativeasset.find_many(where={"campaignId": campaign_id})
    mediaasset = await db.mediaasset.find_many(where={"campaignId": campaign_id})
    contentcalendar = await db.contentcalendar.find_many(where={"campaignId": campaign_id})

    await db.disconnect()

    return {
        "promotionalmessage": promotionalmessage,
        "creativeasset": creativeasset,
        "mediaasset": mediaasset,
        "contentcalendar": contentcalendar,
    }




async def get_pre_launch_phase_data(campaign_id: str):
    """
    Fetches data for stage: Pre-Launch Phase
    """
    await client.connect()
    db = client

    teasercontent = await db.teasercontent.find_many(where={"campaignId": campaign_id})
    customersegmentlist = await db.customersegmentlist.find_many(where={"campaignId": campaign_id})
    influencerplan = await db.influencerplan.find_many(where={"campaignId": campaign_id})
    operationalchecklist = await db.operationalchecklist.find_many(where={"campaignId": campaign_id})

    await db.disconnect()

    return {
        "teasercontent": teasercontent,
        "customersegmentlist": customersegmentlist,
        "influencerplan": influencerplan,
        "operationalchecklist": operationalchecklist,
    }



async def get_campaign_launch_data(campaign_id: str):
    """
    Fetches data for stage: Campaign Launch
    """
    await client.connect()
    db = client

    campaignactivation = await db.campaignactivation.find_many(where={"campaignId": campaign_id})
    customerengagementlog = await db.customerengagementlog.find_many(where={"campaignId": campaign_id})
    performancereport = await db.performancereport.find_many(where={"campaignId": campaign_id})

    await db.disconnect()

    return {
        "campaignactivation": campaignactivation,
        "customerengagementlog": customerengagementlog,
        "performancereport": performancereport,
    }




async def get_post_launch_follow_up_data(campaign_id: str):
    """
    Fetches data for stage: Post-Launch Follow-Up
    """
    await client.connect()
    db = client

    customerfeedback = await db.customerfeedback.find_many(where={"campaignId": campaign_id})
    thankyoumessage = await db.thankyoumessage.find_many(where={"campaignId": campaign_id})
    retargetingplan = await db.retargetingplan.find_many(where={"campaignId": campaign_id})
    campaignextensionplan = await db.campaignextensionplan.find_many(where={"campaignId": campaign_id})

    await db.disconnect()

    return {
        "customerfeedback": customerfeedback,
        "thankyoumessage": thankyoumessage,
        "retargetingplan": retargetingplan,
        "campaignextensionplan": campaignextensionplan,
    }




async def get_campaign_analysis_data(campaign_id: str):
    """
    Fetches data for stage: Campaign Analysis
    """
    await client.connect()
    db = client

    campaignanalysisreport = await db.campaignanalysisreport.find_first(where={"campaignId": campaign_id})
    campaignlearnings = await db.campaignlearnings.find_first(where={"campaignId": campaign_id})
    internalcampaignreport = await db.internalcampaignreport.find_first(where={"campaignId": campaign_id})

    await db.disconnect()

    return {
        "campaignanalysisreport": campaignanalysisreport,
        "campaignlearnings": campaignlearnings,
        "internalcampaignreport": internalcampaignreport,
    }





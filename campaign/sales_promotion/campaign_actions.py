import json

# Define the campaign name
campaign_name = "sales_promotion"

# Define the campaign plan
campaign_plan = [
    {
        "stage": "Research and Objective Setting",
        "goal": "Define the purpose and scope of the campaign.",
        "actions": [
            {
                "task": "Identify the Goal",
                "implementation_guidelines": "Determine the main reason for the campaign such as increasing short-term sales, clearing inventory, or customer acquisition/retention.",
                "output": "CampaignObjective",
                "raci": {
                    "responsible": ["marketing_manager"],
                    "accountable": "campaign_director",
                    "consulted": ["sales_head"],
                    "informed": ["CEO"]
                }
            },
            {
                "task": "Understand the Audience",
                "implementation_guidelines": "Segment the audience based on demographics, interests, and purchase history to create targeted messages.",
                "output": "TargetAudienceSegment",
                "raci": {
                    "responsible": ["data_analyst"],
                    "accountable": "marketing_manager",
                    "consulted": ["crm_team"],
                    "informed": ["campaign_director"]
                }
            },
            {
                "task": "Analyze Competition",
                "implementation_guidelines": "Study competitor promotions and positioning strategies to find differentiators.",
                "output": "CompetitorStrategy",
                "raci": {
                    "responsible": ["market_researcher"],
                    "accountable": "marketing_manager",
                    "consulted": ["brand_team"],
                    "informed": ["product_head"]
                }
            },
            {
                "task": "Choose the Promotion Type",
                "implementation_guidelines": "Decide from discount types, flash deals, gifts, or loyalty rewards based on product fit and margin.",
                "output": "PromotionType",
                "raci": {
                    "responsible": ["campaign_planner"],
                    "accountable": "sales_head",
                    "consulted": ["finance_team"],
                    "informed": ["marketing_team"]
                }
            }
        ]
    },
    {
        "stage": "Campaign Planning",
        "goal": "Design the mechanics and structure of the campaign.",
        "actions": [
            {
                "task": "Determine the Offer",
                "implementation_guidelines": "Craft compelling offers with clear limits (e.g. first 500 customers, limited time only).",
                "output": "CampaignOffer",
                "raci": {
                    "responsible": ["sales_team"],
                    "accountable": "sales_head",
                    "consulted": ["marketing_manager"],
                    "informed": ["customer_support"]
                }
            },
            {
                "task": "Set a Budget",
                "implementation_guidelines": "Estimate the spend for media, creatives, incentives and logistics.",
                "output": "CampaignBudget",
                "raci": {
                    "responsible": ["finance_team"],
                    "accountable": "CFO",
                    "consulted": ["campaign_planner"],
                    "informed": ["CEO"]
                }
            },
            {
                "task": "Select Platforms",
                "implementation_guidelines": "Choose channels like WhatsApp, social media, email and offline locations based on audience behavior.",
                "output": "ChannelPlan",
                "raci": {
                    "responsible": ["media_buyer"],
                    "accountable": "marketing_manager",
                    "consulted": ["creative_team"],
                    "informed": ["sales_team"]
                }
            },
            {
                "task": "Create a Timeline",
                "implementation_guidelines": "Outline every major milestone and deadlines including content creation and testing.",
                "output": "CampaignTimeline",
                "raci": {
                    "responsible": ["project_manager"],
                    "accountable": "campaign_director",
                    "consulted": ["team_leads"],
                    "informed": ["marketing_team"]
                }
            },
            {
                "task": "Compliance Check",
                "implementation_guidelines": "Ensure promotion adheres to all consumer protection laws and internal brand guidelines.",
                "output": "ComplianceChecklist",
                "raci": {
                    "responsible": ["legal_team"],
                    "accountable": "compliance_head",
                    "consulted": ["marketing_manager"],
                    "informed": ["campaign_director"]
                }
            }
        ]
    }
]

# Save to file
filename = f"{campaign_name}_campaign_actions.json"
with open(filename, "w") as f:
    json.dump(campaign_plan, f, indent=2)

filename

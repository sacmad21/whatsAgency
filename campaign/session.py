
session= { }

class CampaignSession:
    """
    Global session object to hold campaign context across slides.
    """

    def __init__(self):
        self.campaign_id = None
        self.company_name = None
        self.domain = None
        self.business_model = None
        self.background = None
        self.current_pain = None
        self.start_date = None
        self.end_date = None
        self.primary_channel = None
        self.objectives = []
        self.competitor_summary = []
        self.total_impressions = 0
        self.total_clicks = 0
        self.total_conversions = 0
        self.revenue_generated = 0.0
        self.campaign_spend = 0.0
        self.roi = 0.0
        self.customer_feedback_summary = ""
        self.learnings_summary = ""

    def __repr__(self):
        return f"CampaignSession({self.company_name} - {self.domain} - {self.business_model})"

# Singleton Pattern (Single Session per Run)
campaign_session = CampaignSession()

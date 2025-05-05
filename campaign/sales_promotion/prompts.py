identify_campaing_goal = """
You are a growth strategist designing a Sales Promotion Campaign for a company named 'UrbanNest Furniture'.

Company Domain: E-commerce - Home & Living  
Business Model: Direct-to-Consumer (D2C) model with online-only storefront, no retail presence  
Background: UrbanNest Furniture is a fast-growing online brand offering modern furniture targeted at urban millennials. Over the last two years, they've expanded their product range and invested heavily in influencer partnerships and Instagram shopping integrations.  
Key Challenge: Despite strong traffic from paid social, their conversion rates remain stagnant. Tier-2 city penetration is poor, and repeat purchase rate is lower than industry benchmarks. There is also rising pressure from local aggregator platforms offering deep discounts.  
Strategic Goals: Increase conversion rates by 15%, boost first-time purchase volume, and expand brand reach in Tier-2 geographies via limited-time offers and loyalty programs.

Based on this business context, generate 3 deeply strategic, measurable campaign goals that align with the company's business problem and objectives.  
Each goal must be:  
- Specific to E-commerce - Home & Living  
- Realistic for a sales promotion campaign  
- Aligned with either customer acquisition, conversion uplift, market expansion, or lead engagement.

Format each goal clearly and succinctly.

"""



understand_audience = """
You are a customer segmentation strategist for a sales promotion campaign.

Company Name: UrbanNest Furniture  
Domain: E-commerce – Home & Living  
Business Model: Direct-to-Consumer (D2C) model with online-only storefront  
Key Challenge: Poor Tier-2 city conversion, low repeat purchases, stagnant conversion rates  
Campaign Goal: Drive 10,000 purchases from Tier-2 cities through regional influencer marketing and free shipping offers.

Based on this, generate 3 detailed audience segments that the campaign should target.
Each segment should include:
- A label (e.g., 'Tier-2 Aspirational Buyers')
- Demographic profile
- Online behavior
- Pain points or unmet needs
"""


analyze_competition = """
You are a competitive strategy analyst. Generate 3 examples of recent sales promotion campaigns 
run by other competitors in the domain 'E-commerce – Home & Living' that target segments similar to 'Tier-2 Aspirational Buyers'.

For each competitor, describe:
- Competitor name
- Promotion type (e.g., Flash Sale, Coupon Code, Loyalty Cashback)
- Channel mix (e.g., Instagram, WhatsApp, Website)
- Strategic strength (why the campaign worked well)
- Weakness or gap (what could be improved)

Format the output clearly for storage and selection.

"""



choose_promotion_type = """
You are a digital commerce strategist planning a sales promotion campaign.

Campaign Goal: Drive 10,000 purchases from Tier-2 cities through regional influencer marketing and free shipping offers.  
Business Model: Direct-to-Consumer (D2C) model with online-only storefront  
Target Geography: Age 24–40, young professionals and homemakers in cities like Indore, Nashik, Bhopal  
Competitor's Promotion Type: Flat 25% off + Cashback

Suggest 3 innovative promotion types that:
- Fit a D2C or digital-first business
- Will appeal to buyers in Age 24–40, young professionals and homemakers in cities like Indore, Nashik, Bhopal
- Are financially feasible and easy to launch via WhatsApp, Instagram, or mobile app
- Are differentiated from the competitor’s approach

For each option, structure your answer like this:

1. Promotion Type: [Name]  
   Description: [Brief explanation of the mechanism]  
   Why It Works: [How it aligns with the customer segment, channel, and goal]  
   Success Criteria: [Measurable outcome e.g., “Reduce cart abandonment by 25% within 2 weeks”]

"""


determine_offer = """
You are a senior campaign strategist for a Direct-to-Consumer (D2C) Online Storefront.

Context:
- Campaign Goal: Drive 10,000 purchases from Tier-2 cities through regional influencer marketing and free shipping offers.
- Target Audience Segment: Tier-2 Aspirational Buyers (Age 24–40, mobile-first shoppers)
- Promotion Type Selected: WhatsApp-Exclusive QR Code Coupon
- Competitor's Strategy Observed: Flat 25% off + Cashback

Your task is to create 3 compelling offer ideas that:
- Strongly support the campaign goal.
- Emotionally connect with the target audience.
- Differentiate clearly from competitor strategy.
- Are executable within a Direct-to-Consumer (D2C) setup.
- Contain clear offer limits (e.g., "first 500 customers", "valid for 7 days only").
- Define measurable success criteria (KPIs).
- Suggest a backup offer plan in case the main offer underperforms.

Structure your response strictly like this:
---
1. Offer Description:
   Offer Limit:
   Offer Type:
   Success Criteria:
   Backup Offer:
"""



set_campaign_budget = """You are acting as a financial strategist for a sales promotion campaign.

Campaign Overview:
- Company Business Model: Direct-to-Consumer (D2C) online storefront
- Target Geography and Audience: Age 24–40, young professionals and homemakers in cities like Indore, Nashik, Bhopal
- Campaign Goal: Drive 10,000 purchases from Tier-2 cities through regional influencer marketing and free shipping offers
- Chosen Promotion Type: WhatsApp-Exclusive QR Code Coupon
- Offer Details: Unlock ₹500 off with your personal QR code — valid only on your first furniture order above ₹4,999
- Offer Redemption Limit: 1000 redemptions
- Competitor's Observed Promotion Type: Flat 25% off + Cashback

Based on the above, provide 3 detailed budget breakdown options.

Each option must include:
- Media Spend
- Creative Spend
- Incentive Spend
- Logistics Spend
- Total Budget
- Cost per Customer
- Expected ROI (based on 80% redemption rate)

Provide thoughtful and practical estimates based on Tier-2 economics in India.

"""


select_platforms= """
You are a digital sales campaign strategist.

Company: UrbanNest Furniture
Domain: E-commerce – Home & Living
Business Model: Direct-to-Consumer (D2C) model with online-only storefront
Target Audience: Tier-2 Aspirational Buyers
Campaign Goal: Drive 10,000 purchases from Tier-2 cities via regional influencer marketing and free shipping offers
Promotion Type: WhatsApp-Exclusive QR Code Coupon
Offer: Unlock ₹500 off with your personal QR code — valid only on your first furniture order above ₹4,999.
Budget: Approx ₹1450000 overall

Recommend the top 3 digital platforms with:
- Platform Name
- Purpose (Lead Gen, Engagement, Conversion, Retargeting)
- Message Style (Story Ad, Broadcast, Carousel Ads, Chatbot)
- Primary (Yes/No)
- If Primary, explain WHY this platform should be the main driver.

Ensure platforms:
- Are mobile-first
- Are cost-effective
- Suit buyers in Tier-2 cities
- Emphasize WhatsApp if fitting

"""


create_campaign_timeline="""You are a professional project manager designing a sales promotion campaign for UrbanNest Furniture.

Business Model: Direct-to-Consumer (D2C) model with online-only storefront
Campaign Goal: Drive 10,000 purchases from Tier-2 cities
Target Audience: Tier-2 Aspirational Buyers (Age 24–40, urban professionals)
Promotion Type: WhatsApp-Exclusive QR Code Coupon
Offer: ₹500 off on first furniture purchase above ₹4,999
Offer Limit: 1000 redemptions
Budget: ₹14,50,000 total (Media, Creative, Incentives, Logistics)
Primary Channel: WhatsApp
Secondary Channels: Instagram, Facebook Ads

Today's Date: 28-04-2025
Target Launch Date: 13-05-2025

Build a project execution timeline for this campaign.
- Suggest 6-8 intelligent milestones.
- Space them logically (creative production, system setup, QA, approvals, influencer collaboration).
- Plan Mid-campaign review and Post-campaign learning phases also.

For each milestone, clearly mention:
- Milestone Name
- Milestone Type (Planning, Execution, QA, Launch, Monitoring, Closing)
- Planned Date

"""


run_compliance_checklist="""You are a Digital Campaign Compliance Officer for a sales promotion campaign.

Campaign Details:
- Company Business Model: Direct-to-Consumer (D2C) model with online-only storefront
- Campaign Goal: Drive 10,000 purchases from Tier-2 cities via WhatsApp QR Code Coupon
- Offer Description: ₹500 off with personal QR code for orders above ₹4,999
- Promotion Type: WhatsApp-Exclusive QR Code Coupon
- Target Geography and Audience: Age 24–40, young professionals and homemakers in cities like Indore, Nashik, Bhopal
- Primary and Secondary Channels: WhatsApp, Instagram, Facebook Ads
- Platform Usage: WhatsApp, Instagram, Facebook Ads
- Success Criteria: Achieve 5,000 redemptions of QR codes within 14 days of launch
- Launch Timeline: Offer Finalization, Creative Approval, Platform Setup, Pre-launch Testing, Launch, Mid-Campaign Review, Post-Campaign Data Collection
- Total Budget: ₹1450000

Create a comprehensive compliance checklist that ensures:
- Indian Consumer Protection compliance
- WhatsApp and Instagram Ads Policy compliance
- Data Privacy for WhatsApp interactions
- Offer disclosure, expiry clarity, cashback conditions
- Financial disclaimer compliance
- Brand tone and design consistency

Each checklist item must include:
- Compliance Item
- Severity
- Responsible Department
- Immediate Action Required
"""




################### Stage 4 
write_promotional_messaging="""You are a campaign messaging expert.

Campaign Details:
- Campaign Goal: Drive 10,000 purchases from Tier-2 cities via WhatsApp QR Coupons
- Promotion Type: WhatsApp-Exclusive QR Code Coupon
- Offer: Unlock ₹500 off with your personal QR code — valid only on your first furniture order above ₹4,999.
- Target Audience: Age 24–40, Tier-2 city professionals and homemakers
- Primary Platform: WhatsApp
- Tone: Friendly and Aspirational with Urgency

Based on this, write 3 highly compelling promotional messages optimized for:
1. WhatsApp Broadcast (friendly, direct, mobile-optimized)
2. Instagram Story Ad (aspirational, urgent, swipe-up CTA)
3. Facebook Carousel Ad (value-focused, community-driven)

Each message should include:
- 1 core message (up to 25 words)
- 1 motivating call-to-action (up to 10 words)

Ensure emotional hooks, sense of urgency, and trust building.

"""


design_campaign_creatives="""You are a creative director designing visual assets for a sales promotion campaign.

Context:
- Company: UrbanNest Furniture (E-commerce – Home & Living)
- Campaign Goal: Drive 10,000 purchases from Tier-2 cities via QR-based coupons
- Offer: Unlock ₹500 off with your personal QR code — valid only on your first furniture order above ₹4,999
- Promotion Type: WhatsApp-Exclusive QR Code Coupon
- Primary Platform: WhatsApp
- Additional Channels: Instagram, Facebook Ads
- Audience: Tier-2 city, Age 24–40, young professionals and homemakers
- Tone: Friendly and Aspirational with urgency

Generate 3 platform-specific creative plans:
- WhatsApp Broadcast Flyer
- Instagram Story Ad
- Facebook Carousel Ad

For each creative, specify:
- Platform
- Creative Title
- Headline Text (hook in 6–8 words)
- Visual Theme (colors, imagery style)
- CTA (short action phrase)
- Mobile Optimization Tip (optimize for Tier-2 city mobile users)

Focus on practical, emotional triggers (trust, value, urgency).
Reference all available campaign context.

"""



prepare_multimedia_assets="""You are a top multimedia creative director building assets for a mobile-first digital campaign.

Company Model: Direct-to-Consumer (D2C) model with online-only storefront  
Target Audience: Tier-2 city young professionals and homemakers (24–40 years)  
Promotion Type: WhatsApp-Exclusive QR Code Coupon  
Offer: Unlock ₹500 off with your personal QR code — valid only on your first furniture order above ₹4,999.  
Primary Channel: WhatsApp  
Messaging Tone: Friendly and Aspirational with Urgency

Previously selected creative directions:
- WhatsApp: Bright minimalistic flyer with QR + smiling customer photo
- Instagram: Animated story zooming on modern furniture + QR reveal
- Facebook: Carousel of bestsellers with "Scan to Save" stickers

Promotional messages by platform:
- WhatsApp: "Exciting news! Scan your QR & get ₹500 OFF your first order. Limited redemptions — Hurry!"
- Instagram: "Furniture Goals? Start with ₹500 OFF! Swipe Up Now!"
- Facebook Ads: "Furnish your dreams for less! Scan your QR, save ₹500 instantly. Limited seats — Shop Now!"

Build 3 multimedia content ideas that:
- Are highly visual and mobile-friendly
- Reinforce QR redemption flow naturally
- Maximize emotional engagement and easy sharing
- Fit the attention span of Tier-2 city customers
- Are optimized under 500 KB file size
- Match urgency and excitement tone

For each idea, structure as:
- Type: ...
- Title: ...
- Concept: ...
- Engagement Tip: ...
- Mobile Optimization Tip: ...

"""


build_content_calendar="""You are an expert content strategist for digital campaigns targeting Tier-2 city audiences in India.

Campaign Insights:
- Goal: Drive 10,000 purchases from Tier-2 cities via regional influencer marketing and free shipping offers
- Offer: Unlock ₹500 off with your personal QR code — valid only on your first furniture order above ₹4,999
- Audience: Tier-2 Aspirational Buyers (Age 24–40, young professionals and homemakers in Indore, Nashik, Bhopal)
- Primary Platform: WhatsApp
- Channels Available: WhatsApp, Instagram, Facebook Ads

Available Content Assets:
- Promotional Messages: ['WhatsApp', 'Instagram', 'Facebook Ads']
- Creatives: ['WhatsApp', 'Instagram', 'Facebook Ads']
- Media Assets: ['GIF']

Campaign Timeline Milestones:
- Offer Finalization on 27-04-2025
- Creative Assets Approval on 30-04-2025
- WhatsApp & Ad Platform Setup on 02-05-2025
- Pre-Launch Testing (Chatbot + Coupon Redemption Flow) on 05-05-2025
- Campaign Go-Live on 10-05-2025
- Mid-Campaign Performance Review on 17-05-2025
- Post-Campaign Data Collection & Reporting on 24-05-2025

Please build a content release calendar that:
- Aligns assets intelligently to campaign milestones.
- Ensures teasers 3–4 days before go-live.
- Pushes heavy WhatsApp broadcasts and Instagram Stories 1 day before and on launch day.
- Launches retargeting creatives after mid-campaign review.
- Ends with a post-campaign thank-you + re-engagement message.
- Optimizes publishing slots (evenings 6–9 PM, weekends for emotional content).

Format each calendar item as:
- ContentType: (Message / Creative / Media)
- Platform: (WhatsApp / Instagram / Facebook)
- ContentReference: (Brief description or asset title)
- ScheduledFor: (DD-MM-YYYY format)
- Notes: (Optional tip like "High traffic expected", "Use emoji in CTA", etc.)

Output only structured list without any explanations.

"""




########### Stage 4 - Prelaunch #############

create_teaser_content="""You are a creative copywriter designing teaser content for a sales promotion.

Offer: Unlock ₹500 off with your personal QR code — valid only on your first furniture order above ₹4,999.  
Launch Date: 10-05-2025

Generate teaser content for:
- WhatsApp Broadcast (short, mystery, builds curiosity)
- Instagram Story Ad (visual hint + countdown)
- Facebook Post (engaging mystery reveal)

Structure:
Platform: ...
Message: ...
Recommended Launch Date: 08-05-2025
"""


create_and_distribute_teasers="""You are a creative strategist for a Tier-2 city-focused D2C campaign.

Campaign Context:
- Company Domain: Home & Living (Furniture)
- Business Model: D2C (online-only)
- Offer: ₹500 off with QR code on first purchase above ₹4,999
- Primary Channel: WhatsApp
- Target Audience: Tier-2 cities (Indore, Nashik, Bhopal)
- Promotion Type: WhatsApp-Exclusive QR Code Coupon
- Launch Date: 10-05-2025

Your task:
- Generate 3 teaser ideas optimized for WhatsApp, Instagram Story, and Facebook Ads.
- Create different teaser types: 1 Mystery, 1 Countdown, 1 Influencer Hint.
- Each teaser must include a teaserTheme, a short Message (<150 characters), and clear CTA like "Stay Tuned" or "Unlock the Mystery."
- Make sure teasers are mobile-first, quick-read friendly for Tier-2 audiences.

Format your output as:
1. Platform: ...
   TeaserTheme: ...
   Message: ...
   Recommended Launch Date: 08-05-2025
"""



clean_and_segment_contacts="""You are an advanced CRM strategist.

Here are details of an upcoming campaign:
- Offer: Unlock ₹500 off with your personal QR code — valid only on your first furniture order above ₹4,999.
- Launch Date: 10-05-2025
- Target Audience: Age 24–40, young professionals and homemakers from Tier-2 cities like Indore, Nashik, Bhopal
- Primary Platform: WhatsApp
- Promotion Style: QR code-based discount redemption
- Tone: Friendly, Aspirational, Urgent

Your task:
- Segment customers based on behavioral readiness, purchase history, and location.
- Clean the list by removing users inactive in the last 90 days.
- Recommend 3 segments creatively named but highly actionable.

For each segment, provide:
- Segment Name
- Criteria (short description of segmentation logic)
- Approximate Count

"""



engage_influencers="""You are an influencer marketing strategist for a digital furniture brand campaign.

Campaign Details:
- Business Model: Direct-to-Consumer (D2C) model with online-only storefront
- Audience: Tier-2 city young professionals and homemakers (Indore, Nashik, Bhopal)
- Promotion Type: WhatsApp-Exclusive QR Code Coupon
- Offer: Unlock ₹500 off with your personal QR code — valid only on your first furniture order above ₹4,999
- Primary Channel: WhatsApp
- Launch Date: 10-05-2025
- Teaser Phase: Start teasing 2 days before launch.

Objective:
- Build strong excitement before the launch
- Drive QR-code scans and ₹500 offer redemptions
- Focus on Tier-2 city audiences

Requirements:
- Suggest 3 influencer collaboration plans.
- Each plan should include:
  - Influencer Name (conceptual)
  - Platform (Instagram, YouTube, WhatsApp Community)
  - Post Type (Story, Reel, Static Post, Group Post)
  - Expected Impact (eg: Build Curiosity, Drive Swipes, Initiate Conversations)
  - Suggested Post Date

Be creative, practical, and specific. Tie influencer activity closely to the QR code offer and campaign urgency.

Format:
1. Influencer Name: ...
   Platform: ...
   Post Type: ...
   Expected Impact: ...
   Suggested Post Date: ...

"""



create_operational_checklist="""
You are a QA Lead preparing a professional pre-launch operational checklist for a digital campaign.

Campaign Overview:
- Promotion Type: WhatsApp QR Code ₹500 off offer
- Primary Channel: WhatsApp
- Platforms Used: WhatsApp, Instagram, Facebook Ads
- Active Systems: 
    • WhatsApp QR Code Flow
    • WhatsApp Chatbot
    • Payment Gateway
    • Landing Pages
    • Analytics (Google Analytics 4)
    • CRM Integration
    • Instagram Story Ads
    • Facebook Carousel Ads

Checklist Quality Requirements:
- For each checklist item, provide:
    1. System: (specific component like WhatsApp QR, Payment Gateway, Instagram Story Ad, etc.)
    2. Checklist Item: (specific action or verification step)
    3. Expected Outcome: (define success clearly and measurably)
    4. Responsibility: (who will validate: Tech Team, QA Team, CRM Admin, Marketing, Support)
    5. Status: Pending (default)

Guidelines:
- Each checklist item should be reviewable and assignable.
- Cover technical testing, content verification, load handling, customer journey smoothness, failure fallback, analytics correctness.

Format:
System: ...
Checklist Item: ...
Expected Outcome: ...
Responsibility: ...
Status: Pending
"""

activate_campaign="""You are a digital marketing campaign launch specialist.

You are activating the following campaign:

Campaign Details:
- Goal: Drive QR code redemptions and new customer signups
- Offer: ₹500 off via QR scan on first furniture purchase
- Target Audience: Tier-2 city young homeowners (Indore, Nashik, Bhopal)
- Launch Date: 10-05-2025
- Major Customer Segments: High Intent Shoppers, New Explorers from Tier-2, Past Buyers
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





enable_real_time_support="""You are a customer experience strategist designing real-time support for a live digital campaign.

Campaign Context:
- Product: UrbanNest Furniture QR Code Promotion
- Offer: ₹500 off on first purchase
- Launch Date: 10-May-2025
- Primary Channel: WhatsApp (chatbot + live human escalation)
- Target Audience: Tier-2 City Young Homebuyers
- Campaign Objective: Drive QR redemptions and new customer acquisitions

Support Objectives:
- Ensure instant resolution of basic queries via chatbot (under 3 seconds)
- Escalate complex issues to human agents within 2 minutes
- Escalations triggered if chatbot fails to understand after 2 replies, or if user sends keywords like "Help", "Problem", "Agent"
- Capture Customer Satisfaction (CSAT) score post-resolution
- Daily monitoring report for unresolved or delayed chats

Build a structured real-time support plan:
- Define Interaction Types
- Define Escalation Triggers
- Define SLA Monitoring Rules
- Define CSAT Collection Mechanism
- Define Daily Support Monitoring Report Structure

"""




monitor_daily_performance_metrics="""You are a Campaign Performance Analyst for a live product promotion campaign.

Campaign Details:
- Brand: UrbanNest Furniture
- Offer: ₹500 off on first furniture order above ₹4999
- Launch Date: 10-May-2025
- Primary Channels: WhatsApp, Instagram, Facebook
- Customer Segments: High Intent Shoppers, New Explorers from Tier-2
- Support Setup: WhatsApp Bot with escalation to Human Agents (SLA ≤3s for Bot, ≤2min for Human)

Objectives:
- Track daily KPIs across WhatsApp, Instagram, Facebook, Support
- Identify anomalies early (SLA breaches, drop in conversions, poor CSAT)

Build the following:
- KPIs to Track
- Suggested Thresholds for Anomaly Detection
- CSAT & SLA Monitoring strategy
- Daily Reporting Template

Examples of anomalies:
- >20% drop in conversions day-over-day
- Escalation rate >25%
- Bot SLA response failures >5%
- CSAT score average <3.5
"""





collect_customer_feedback="""You are a customer experience strategist creating a feedback collection system after a major product launch.

Campaign Context:
- Name: UrbanNest QR Code Launch Offer
- Goal: Drive first-time buyers using ₹500 off
- Main Channels: WhatsApp, Instagram, Facebook
- Offer Details: ₹500 off on first order above ₹4999
- Target Audience: Young homeowners in Tier-2 cities

Objectives:
- Collect actionable feedback post-campaign, focusing on QR code redemption experience, satisfaction, and brand impression.
- Use WhatsApp-first communication (friendly, short-form).
- Provide rating collection (1–5) and allow optional free-text comments.

Design:
- Feedback collection Message Template (for WhatsApp and Email)
- Three Specific Feedback Questions (aligned with campaign context)
- Rating Mechanism (WhatsApp tap options)
- Target Segment Selection Strategy

Output Structure:
- WhatsAppMessageTemplate
- EmailTemplate
- FeedbackQuestions
- RatingMechanism
- TargetSegments
"""



send_thank_you_messages="""You are a customer engagement specialist designing post-campaign thank-you messaging.

Campaign Context:
- Campaign Name: UrbanNest QR Code Launch
- Product: UrbanNest Furniture Collection
- Goal: Drive QR redemptions and first-time purchases
- Offer: ₹500 off on first order above ₹4999
- Launch Date: 10-May-2025
- Target Audience: Buyers, High-intent Visitors
- Primary Channels: WhatsApp, Instagram, Facebook

Objectives:
- Thank all participants warmly
- Personalize differently for:
  1. Buyers: Gratitude + hint about loyalty offers + VIP sneak peek
  2. Non-converters: Thank + nudge with gentle limited-time bonus (e.g., ₹300 extra coupon for 5 days)
- WhatsApp messages: short, casual
- Email messages: slightly richer, emotional, relational

Instructions:
- WhatsApp max 3 lines, easy to read
- Email max 6 lines with strong CTA
- Ensure re-engagement without looking desperate

Output Needed:
- WhatsAppMessageBuyer
- WhatsAppMessageNonConverter
- EmailTemplateBuyer
- EmailTemplateNonConverter
"""



retarget_interested_customers="""You are a customer retargeting strategist.

Campaign Context:
- Campaign Name: UrbanNest Furniture QR Code Campaign
- Campaign Offer: ₹500 off first purchase above ₹4999
- Key Observations: Feedback collected — users loved product variety but some dropped off during checkout.

User Segments:
- Users who scanned QR but did not checkout
- Users who interacted with chatbot but did not buy
- Users who partially added products to cart but did not pay

Objective:
- Build a powerful retargeting plan to convert high-intent users.
- Channels to consider: WhatsApp, Instagram Ads, Facebook Retargeting, Email
- Offer Options: Continue ₹500 offer OR ₹300 bonus for quick action within 5 days
- Personalize based on past interaction (if they scanned QR, visited site, abandoned cart).

Tasks:
- Identify audience segments and messaging nuances.
- Create WhatsApp Message Template (for retargeting nudge)
- Create Instagram Ad Copy Sample
- Create Facebook Ad Copy Sample
- Create Reminder Email Template
- Create UTM tracking recommendations.

Output Format:
- AudienceSegments
- WhatsAppTemplate
- InstagramAdCopy
- FacebookAdCopy
- EmailTemplate
- UTMRecommendations
"""



analyze_campaign_metrics="""You are a campaign data analyst.

Campaign Context:
- Name: UrbanNest QR Code Launch Campaign
- Period: 1-May-2025 to 10-May-2025
- Offer: ₹500 off for first-time buyers on orders above ₹4999

Available Metrics:
- Total Impressions: 74,000
- Total Clicks: 5,700
- Total QR Scans: 2,250
- Total Conversions: 380
- Average Order Value: ₹6000
- Campaign Spend: ₹200,000
- CSAT Score Average: 4.3
- Escalation Rate: 12.1%

Objectives:
- Analyze sales uplift, engagement boost, ROI
- Calculate conversion rate, engagement rate
- Summarize if traffic-to-sale ratio was healthy
- Suggest if offer value was appropriate
- Identify operational bottlenecks (like escalations)

Generate:
- Analysis Summary
- KPIs Calculated
- Recommendations
"""


document_key_learnings="""You are a campaign retrospection expert.

Campaign Context:
- Name: UrbanNest QR Code Launch Campaign
- Period: 1-May-2025 to 10-May-2025
- Offer: ₹500 off for first-time buyers

Analysis Summary:
- ROI: 1040%
- Conversion Rate: 6.67%
- Engagement Rate: 7.7%
- CSAT Average: 4.3
- Escalation Rate: 12.1%

Retargeting Result:
- Boosted conversion by +5% from non-converters using ₹300 coupon.

Stock Clearance Result:
- Additional 50 units sold during extended sale.

Feedback Insights:
- Customers appreciated QR code ease, but wanted faster delivery.
- Some confusion around applying discount code at checkout.

Objectives:
- Document what worked well during the campaign
- Identify what didn’t work or faced friction
- Establish best practices for future sales campaigns
- Highlight key areas for operational or customer experience improvement

Generate:
- What Worked
- What Didn't Work
- Best Practices
- Improvement Areas
"""
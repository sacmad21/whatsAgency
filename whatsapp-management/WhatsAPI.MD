1. Messages

    Send Message:
    Endpoint: POST /v1/messages
    Description: Sends text, media, interactive, and template messages to users.

    Retrieve Message Status:
    Endpoint: GET /v1/messages/{message_id}
    Description: Retrieves the status of a previously sent message.



2. Media

    Upload Media:
    Endpoint: POST /v1/media
    Description: Uploads media files like images, videos, and documents to WhatsApp.

    Download Media:
    Endpoint: GET /v1/media/{media_id}
    Description: Downloads previously uploaded media files using their media ID.

    Delete Media:
    Endpoint: DELETE /v1/media/{media_id}
    Description: Deletes media files stored on WhatsApp servers.



3. Templates

    List Templates:
    Endpoint: GET /v1/message_templates
    Description: Retrieves all registered templates for your account.

    Create Template:
    Endpoint: POST /v1/message_templates
    Description: Creates a new message template.

    Delete Template:
    Endpoint: DELETE /v1/message_templates/{template_name}
    Description: Deletes an existing template.



4. Contacts

    Check Contact:
    Endpoint: POST /v1/contacts
    Description: Verifies if a phone number is registered on WhatsApp.



5. Webhooks

    Set Webhook URL:
    Endpoint: POST /v1/settings/webhooks
    Description: Configures the webhook for receiving messages, events, and status updates.

    Retrieve Webhook Config:
    Endpoint: GET /v1/settings/webhooks
    Description: Gets the current webhook configuration.

    Delete Webhook Config:
    Endpoint: DELETE /v1/settings/webhooks
    Description: Removes webhook configuration.

6. Business Profile

    Get Business Profile:
    Endpoint: GET /v1/settings/profile
    Description: Retrieves the business profile information.

    Update Business Profile:
    Endpoint: POST /v1/settings/profile
    Description: Updates the business profile details.

7. Phone Numbers

    Get Phone Numbers:
    Endpoint: GET /v1/phone_numbers
    Description: Lists all phone numbers registered under your account.

    Update Phone Number Settings:
    Endpoint: POST /v1/phone_numbers/{phone_number_id}
    Description: Updates specific settings for a phone number.

8. Two-Step Verification

    Enable Two-Step Verification:
    Endpoint: POST /v1/settings/two_step_verification
    Description: Enables two-step verification for your account.

    Disable Two-Step Verification:
    Endpoint: DELETE /v1/settings/two_step_verification
    Description: Disables two-step verification.

9. Insights & Analytics

    Retrieve Metrics:
    Endpoint: GET /v1/metrics
    Description: Retrieves usage and performance metrics for your WhatsApp account.

10. Miscellaneous

    Health Check:
    Endpoint: GET /v1/health
    Description: Checks the health and connectivity of the WhatsApp API service.

    Get Application Info:
    Endpoint: GET /v1/settings/application
    Description: Retrieves application-level configuration and settings.


11. Conversation Management

    Get Active Conversations:
    Endpoint: GET /v1/conversations
    Description: Retrieves active conversations and their statuses for billing and monitoring purposes.

    Retrieve Conversation Pricing:
    Endpoint: GET /v1/pricing/conversations
    Description: Fetches the pricing details for user-initiated or business-initiated conversations.

12. Message Templates Management

    Update Template:
    Endpoint: POST /v1/message_templates/{template_name}
    Description: Updates an existing template for text, buttons, or media.

    Template Preview:
    Endpoint: POST /v1/message_templates/preview
    Description: Provides a preview of how a message template would appear to users.

13. Group Messaging (Limited Access)

    Create Group:
    Endpoint: POST /v1/groups
    Description: Creates a new group for messaging (if available for your API version).

    Add Participants to Group:
    Endpoint: POST /v1/groups/{group_id}/participants
    Description: Adds participants to a specific group.

    Remove Participants from Group:
    Endpoint: DELETE /v1/groups/{group_id}/participants/{participant_id}
    Description: Removes a participant from a specific group.

14. Opt-In/Opt-Out Management

    Get Opt-In Status:
    Endpoint: GET /v1/contacts/{contact_id}/opt_in_status
    Description: Checks if a user has opted in to receive messages from your business.

    Manage Opt-In:
    Endpoint: POST /v1/contacts/{contact_id}/opt_in
    Description: Updates a user's opt-in status for specific message types.

    Manage Opt-Out:
    Endpoint: POST /v1/contacts/{contact_id}/opt_out
    Description: Manages opt-out requests for users.

15. Message Read Receipts

    Mark Message as Read:
    Endpoint: POST /v1/messages/{message_id}/read
    Description: Marks a specific message as read by the user to trigger read receipts.

16. Multi-User Management (If Applicable)

    List Users:
    Endpoint: GET /v1/users
    Description: Retrieves all users who have access to the API instance.

    Create User:
    Endpoint: POST /v1/users
    Description: Adds a new user to the system for accessing the WhatsApp API.

    Delete User:
    Endpoint: DELETE /v1/users/{user_id}
    Description: Removes a user from accessing the API.

17. Account and Service Management

    Update Account Settings:
    Endpoint: POST /v1/settings/account
    Description: Updates account-level settings, such as payment methods or notification preferences.

    Delete Account:
    Endpoint: DELETE /v1/settings/account
    Description: Deletes the WhatsApp Business account (irreversible).

18. Opt-In Campaigns (Advanced Use Cases)

    Initiate Opt-In Campaign:
    Endpoint: POST /v1/campaigns/opt_in
    Description: Starts a campaign to gather user consent for specific types of messages.

19. Callback Configuration

    List Callback Events:
    Endpoint: GET /v1/settings/callbacks
    Description: Lists all events configured for callback notifications.

    Update Callback Events:
    Endpoint: POST /v1/settings/callbacks
    Description: Updates the callback events configuration.

    Delete Callback Event:
    Endpoint: DELETE /v1/settings/callbacks/{event_id}
    Description: Removes a specific callback event.

20. Advanced Security

    Enable Encryption Settings:
    Endpoint: POST /v1/settings/encryption
    Description: Configures end-to-end encryption settings for messages and media.

    Check Encryption Keys:
    Endpoint: GET /v1/settings/encryption/keys
    Description: Retrieves the current encryption keys used for secure communications.

21. Advanced Media Handling

    Retrieve Media Metadata:
    Endpoint: GET /v1/media/{media_id}/metadata
    Description: Retrieves metadata for uploaded media, such as file size and type.

22. Message Scheduling

    Schedule Message:
    Endpoint: POST /v1/messages/schedule
    Description: Schedules a message for delivery at a future date and time.

    Cancel Scheduled Message:
    Endpoint: DELETE /v1/messages/schedule/{schedule_id}
    Description: Cancels a previously scheduled message.

23. Archiving

    Archive Messages:
    Endpoint: POST /v1/messages/archive
    Description: Archives a set of messages for long-term storage.

    Retrieve Archived Messages:
    Endpoint: GET /v1/messages/archive
    Description: Fetches previously archived messages.


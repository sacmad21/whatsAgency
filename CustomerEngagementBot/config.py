WHATSAPP_API_URL = "https://graph.facebook.com/v16.0/<your-phone-number-id>/messages"
WHATSAPP_ACCESS_TOKEN = "your-whatsapp-access-token"

customer_segments = {
    "regulars": ["+12345678901", "+12345678902"],
    "foodies": ["+12345678903", "+12345678904"],
    "new_customers": ["+12345678905", "+12345678906"],
    "gym_members": ["+12345678907", "+12345678908"]
}

engagement_data = {
    "regulars": {"messages_sent": 0, "replies": 0},
    "foodies": {"messages_sent": 0, "replies": 0},
    "new_customers": {"messages_sent": 0, "replies": 0},
    "gym_members": {"messages_sent": 0, "replies": 0}
}

loyalty_points = {
    "+12345678907": 50,
    "+12345678908": 30
}


from azure.cosmos import exceptions
from db_config import CosmosDBConfig

# Initialize CosmosDBConfig
config = CosmosDBConfig(endpoint="<COSMOS_DB_ENDPOINT>", key="<COSMOS_DB_KEY>", database_name="real_estate_db")

# Save feedback entry
def save_feedback_entry(feedback_id, business_id, user_id, content, timestamp):
    """
    Save user feedback to the 'feedback_entries' container.
    """
    container = config.create_container("feedback_entries", {"path": "/businessId"})
    feedback_item = {
        "feedbackId": feedback_id,
        "businessId": business_id,
        "userId": user_id,
        "content": content,
        "timestamp": timestamp
    }
    try:
        container.create_item(body=feedback_item)
        return {"status": "success", "message": "Feedback entry saved successfully."}
    except exceptions.CosmosHttpResponseError as e:
        return {"status": "error", "message": str(e)}

# Fetch feedback by user
def fetch_feedback_by_user(user_id, business_id):
    """
    Retrieve feedback entries for a specific user from the 'feedback_entries' container.
    """
    container = config.create_container("feedback_entries", {"path": "/businessId"})
    query = f"SELECT * FROM feedback_entries fe WHERE fe.userId = '{user_id}' AND fe.businessId = '{business_id}'"
    try:
        results = list(container.query_items(query=query, enable_cross_partition_query=True))
        return {"status": "success", "data": results}
    except exceptions.CosmosHttpResponseError as e:
        return {"status": "error", "message": str(e)}

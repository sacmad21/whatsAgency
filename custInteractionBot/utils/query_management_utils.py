from azure.cosmos import exceptions
from db_config import CosmosDBConfig

# Initialize CosmosDBConfig
config = CosmosDBConfig(endpoint="<COSMOS_DB_ENDPOINT>", key="<COSMOS_DB_KEY>", database_name="real_estate_db")

# Save a customer query
def save_customer_query(query_id, business_id, user_id, query_text, timestamp):
    """
    Save a customer query to the 'customer_queries' container.
    """
    container = config.create_container("customer_queries", {"path": "/businessId"})
    query_item = {
        "queryId": query_id,
        "businessId": business_id,
        "userId": user_id,
        "queryText": query_text,
        "timestamp": timestamp
    }
    try:
        container.create_item(body=query_item)
        return {"status": "success", "message": "Query saved successfully."}
    except exceptions.CosmosHttpResponseError as e:
        return {"status": "error", "message": str(e)}

# Fetch queries by user
def fetch_queries_by_user(user_id, business_id):
    """
    Fetch all queries submitted by a specific user from the 'customer_queries' container.
    """
    container = config.create_container("customer_queries", {"path": "/businessId"})
    query = f"SELECT * FROM customer_queries cq WHERE cq.userId = '{user_id}' AND cq.businessId = '{business_id}'"
    try:
        results = list(container.query_items(query=query, enable_cross_partition_query=True))
        return {"status": "success", "data": results}
    except exceptions.CosmosHttpResponseError as e:
        return {"status": "error", "message": str(e)}

# Save a chatbot response
def save_chatbot_response(response_id, business_id, query_id, response_text, timestamp):
    """
    Save a chatbot response to the 'chatbot_responses' container.
    """
    container = config.create_container("chatbot_responses", {"path": "/businessId"})
    response_item = {
        "responseId": response_id,
        "businessId": business_id,
        "queryId": query_id,
        "responseText": response_text,
        "timestamp": timestamp
    }
    try:
        container.create_item(body=response_item)
        return {"status": "success", "message": "Chatbot response saved successfully."}
    except exceptions.CosmosHttpResponseError as e:
        return {"status": "error", "message": str(e)}

# Fetch responses by query
def fetch_responses_by_query(query_id, business_id):
    """
    Fetch all chatbot responses for a specific query from the 'chatbot_responses' container.
    """
    container = config.create_container("chatbot_responses", {"path": "/businessId"})
    query = f"SELECT * FROM chatbot_responses cr WHERE cr.queryId = '{query_id}' AND cr.businessId = '{business_id}'"
    try:
        results = list(container.query_items(query=query, enable_cross_partition_query=True))
        return {"status": "success", "data": results}
    except exceptions.CosmosHttpResponseError as e:
        return {"status": "error", "message": str(e)}

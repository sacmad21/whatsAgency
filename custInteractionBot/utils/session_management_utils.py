from azure.cosmos import exceptions
from db_config import CosmosDBConfig

# Initialize CosmosDBConfig
config = CosmosDBConfig(endpoint="<COSMOS_DB_ENDPOINT>", key="<COSMOS_DB_KEY>", database_name="real_estate_db")

# Create a chat session
def create_chat_session(session_id, business_id, user_id, messages):
    """
    Create a new chat session in the 'chat_sessions' container.
    """
    container = config.create_container("chat_sessions", {"path": "/businessId"})
    session_item = {
        "sessionId": session_id,
        "businessId": business_id,
        "userId": user_id,
        "messages": messages
    }
    try:
        container.create_item(body=session_item)
        return {"status": "success", "message": "Chat session created successfully."}
    except exceptions.CosmosHttpResponseError as e:
        return {"status": "error", "message": str(e)}

# Fetch chat session details
def fetch_chat_session(session_id, business_id):
    """
    Retrieve chat session details by session ID from the 'chat_sessions' container.
    """
    container = config.create_container("chat_sessions", {"path": "/businessId"})
    query = f"SELECT * FROM chat_sessions cs WHERE cs.sessionId = '{session_id}' AND cs.businessId = '{business_id}'"
    try:
        results = list(container.query_items(query=query, enable_cross_partition_query=True))
        return {"status": "success", "data": results}
    except exceptions.CosmosHttpResponseError as e:
        return {"status": "error", "message": str(e)}

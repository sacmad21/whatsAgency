from azure.cosmos import exceptions
from db_config import CosmosDBConfig

# Initialize CosmosDBConfig
config = CosmosDBConfig(endpoint="<COSMOS_DB_ENDPOINT>", key="<COSMOS_DB_KEY>", database_name="real_estate_db")

# Save user preferences
def save_user_preferences(preference_id, business_id, user_id, budget, location, property_type):
    """
    Save user preferences to the 'user_preferences' container.
    """
    container = config.create_container("user_preferences", {"path": "/businessId"})
    preference_item = {
        "preferenceId": preference_id,
        "businessId": business_id,
        "userId": user_id,
        "budget": budget,
        "location": location,
        "propertyType": property_type
    }
    try:
        container.create_item(body=preference_item)
        return {"status": "success", "message": "User preferences saved successfully."}
    except exceptions.CosmosHttpResponseError as e:
        return {"status": "error", "message": str(e)}

# Fetch user preferences
def fetch_user_preferences(user_id, business_id):
    """
    Retrieve user preferences by user ID from the 'user_preferences' container.
    """
    container = config.create_container("user_preferences", {"path": "/businessId"})
    query = f"SELECT * FROM user_preferences up WHERE up.userId = '{user_id}' AND up.businessId = '{business_id}'"
    try:
        results = list(container.query_items(query=query, enable_cross_partition_query=True))
        return {"status": "success", "data": results}
    except exceptions.CosmosHttpResponseError as e:
        return {"status": "error", "message": str(e)}

# Fetch property information
def fetch_property_info(property_id, business_id):
    """
    Retrieve property details by property ID from the 'basic_property_info' container.
    """
    container = config.create_container("basic_property_info", {"path": "/businessId"})
    query = f"SELECT * FROM basic_property_info bp WHERE bp.propertyId = '{property_id}' AND bp.businessId = '{business_id}'"
    try:
        results = list(container.query_items(query=query, enable_cross_partition_query=True))
        return {"status": "success", "data": results}
    except exceptions.CosmosHttpResponseError as e:
        return {"status": "error", "message": str(e)}

# Search properties using filters
def search_properties(business_id, filters):
    """
    Search properties using filters (e.g., budget, location, type) in the 'basic_property_info' container.
    """
    container = config.create_container("basic_property_info", {"path": "/businessId"})
    conditions = [f"bp.{key} = '{value}'" for key, value in filters.items()]
    query = f"SELECT * FROM basic_property_info bp WHERE bp.businessId = '{business_id}' AND {' AND '.join(conditions)}"
    try:
        results = list(container.query_items(query=query, enable_cross_partition_query=True))
        return {"status": "success", "data": results}
    except exceptions.CosmosHttpResponseError as e:
        return {"status": "error", "message": str(e)}

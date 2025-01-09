from azure.cosmos import CosmosClient
import os
from datetime import datetime

# Azure Cosmos DB Configuration
COSMOS_ENDPOINT = os.getenv("COSMOS_ENDPOINT", "https://gbot.documents.azure.com:443/")
COSMOS_KEY = os.getenv("COSMOS_KEY", "ugozXtut2oB1vd6QuX29VRe8gylhAIncTJ6ZSr1TjoepwMrWSEKomVi4ysmJHyRvYGsmtRqw7xIrACDbzHLqUg==")
DATABASE_NAME = "wagency"

# Initialize Cosmos DB Client
client = CosmosClient(COSMOS_ENDPOINT, COSMOS_KEY)
database = client.create_database_if_not_exists(id=DATABASE_NAME)

# Create Containers
categories_container = database.create_container_if_not_exists(
    id="categories",
    partition_key={"paths": ["/id"]},
    offer_throughput=400
)

products_container = database.create_container_if_not_exists(
    id="products",
    partition_key={"paths": ["/id"]},
    offer_throughput=400
)

customers_container = database.create_container_if_not_exists(
    id="customers",
    partition_key={"paths": ["/id"]},
    offer_throughput=400
)

promotions_container = database.create_container_if_not_exists(
    id="promotions",
    partition_key={"paths": ["/id"]},
    offer_throughput=400
)

feedback_container = database.create_container_if_not_exists(
    id="feedback",
    partition_key={"paths": ["/id"]},
    offer_throughput=400
)

# Additional Enhancements
def log_customer_interaction(customer_id, interaction_type, details):
    feedback_container.upsert_item({
        "id": str(uuid.uuid4()),
        "customer_id": customer_id,
        "interaction_type": interaction_type,
        "details": details,
        "timestamp": datetime.utcnow().isoformat(),
    })

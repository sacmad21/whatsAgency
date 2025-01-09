from azure.cosmos import CosmosClient
import os



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

bot_config_container = database.create_container_if_not_exists(
    id="bot_config",
    partition_key={"paths": ["/id"]},
    offer_throughput=400
)

chatbot_config_container = database.create_container_if_not_exists(
    id="bot_config",
    partition_key={"paths": ["/id"]},
    offer_throughput=400
)

customer_messages_container = database.create_container_if_not_exists(
    id="customer_messages",
    partition_key={"paths": ["/id"]},
    offer_throughput=400
)

promotions_container = database.create_container_if_not_exists(
    id="promotions",
    partition_key={"paths": ["/id"]},
    offer_throughput=400
)

engagement_metrics_container = database.create_container_if_not_exists(
    id="engagement_metrics",
    partition_key={"paths": ["/id"]},
    offer_throughput=400
)

order_history_container = database.create_container_if_not_exists(
    id="order_history",
    partition_key={"paths": ["/id"]},
    offer_throughput=400
)

api_config_container = database.create_container_if_not_exists(
    id="api_config",
    partition_key={"paths": ["/id"]},
    offer_throughput=400
)

feedback_container = database.create_container_if_not_exists(
    id="feedback",
    partition_key={"paths": ["/id"]},
    offer_throughput=400
)

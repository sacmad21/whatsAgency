import random
import datetime
from faker import Faker
from db_config import (
    categories_container,
    products_container,
    customers_container,
    bot_config_container,
    customer_messages_container,
    promotions_container,
    engagement_metrics_container,
    order_history_container,
    api_config_container,
    feedback_container
)

fake = Faker()

def generate_test_data():
    # Generate Categories
    categories = [
        {"id": f"cat-{i+1}", "name": name, "description": f"Category focused on {name}"}
        for i, name in enumerate(["Electronics", "Apparel", "Home & Kitchen", "Tools", "Books", "Beauty", "Sports", "Toys", "Automotive", "Health"])
    ]
    for category in categories:
        categories_container.create_item(body=category)

    # Generate Product Inventory
    products = []
    for i in range(200):
        product = {
            "id": f"prod-{i+1}",
            "category_id": random.choice(categories)["id"],
            "name": fake.catch_phrase(),
            "price": round(random.uniform(10.0, 1000.0), 2),
            "availability": random.choice([True, False]),
            "description": fake.text(max_nb_chars=100)
        }
        products.append(product)
        products_container.create_item(body=product)

    # Generate Customer Information
    customers = [
        {"id": f"cust-{i+1}", "name": fake.name(), "preferences": fake.random_element(elements=("Electronics", "Books", "Apparel", "Beauty"))}
        for i in range(100)
    ]
    for customer in customers:
        customers_container.create_item(body=customer)

    # Generate Chatbot Configurations
    bot_configs = [
        {"id": f"config-{i+1}", "key": f"welcome_message_{i+1}", "value": fake.sentence()} for i in range(10)
    ]
    for config in bot_configs:
        bot_config_container.create_item(body=config)

    # Generate Customer Messages
    customer_messages = [
        {
            "id": f"msg-{i+1}",
            "customer_id": random.choice(customers)["id"],
            "message_body": fake.text(max_nb_chars=200),
            "timestamp": datetime.datetime.now().isoformat(),
            "direction": random.choice(["incoming", "outgoing"])
        }
        for i in range(300)
    ]
    for message in customer_messages:
        customer_messages_container.create_item(body=message)

    # Generate Promotions
    promotions = [
        {
            "id": f"promo-{i+1}",
            "category_id": random.choice(categories)["id"],
            "product_id": random.choice(products)["id"],
            "description": f"Buy more, save more on {fake.catch_phrase()}!",
            "start_date": (datetime.datetime.now() - datetime.timedelta(days=random.randint(1, 30))).isoformat(),
            "end_date": (datetime.datetime.now() + datetime.timedelta(days=random.randint(1, 30))).isoformat()
        }
        for i in range(50)
    ]
    for promo in promotions:
        promotions_container.create_item(body=promo)

    # Generate Engagement Metrics
    engagement_metrics = [
        {
            "id": f"eng-{i+1}",
            "customer_id": random.choice(customers)["id"],
            "interaction_count": random.randint(1, 100),
            "last_interaction": datetime.datetime.now().isoformat()
        }
        for i in range(200)
    ]
    for metric in engagement_metrics:
        engagement_metrics_container.create_item(body=metric)

    # Generate Order History
    order_history = [
        {
            "id": f"order-{i+1}",
            "customer_id": random.choice(customers)["id"],
            "product_id": random.choice(products)["id"],
            "order_date": (datetime.datetime.now() - datetime.timedelta(days=random.randint(1, 365))).isoformat(),
            "quantity": random.randint(1, 10),
            "total_price": round(random.uniform(20.0, 5000.0), 2)
        }
        for i in range(150)
    ]
    for order in order_history:
        order_history_container.create_item(body=order)

    # Generate API Configurations
    api_configs = [
        {"id": f"api-{i+1}", "key": f"api_key_{i+1}", "value": fake.uri()} for i in range(5)
    ]
    for config in api_configs:
        api_config_container.create_item(body=config)

    # Generate Feedback
    feedback = [
        {
            "id": f"feedback-{i+1}",
            "customer_id": random.choice(customers)["id"],
            "product_id": random.choice(products)["id"],
            "rating": random.randint(1, 5),
            "comments": fake.text(max_nb_chars=200),
            "timestamp": datetime.datetime.now().isoformat()
        }
        for i in range(400)
    ]
    for item in feedback:
        feedback_container.create_item(body=item)

    print("Realistic test data generation complete.")

if __name__ == "__main__":
    generate_test_data()

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.tabbedpanel import TabbedPanel
from kivy.uix.tabbedpanel import TabbedPanelItem
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout
from kivy.uix.image import Image
import matplotlib.pyplot as plt
import io
from kivy.core.image import Image as CoreImage
from product_inventory_manager import ProductInventoryManager
from customer_information_manager import CustomerInformationManager
from feedback_manager import FeedbackManager
from customer_messages_manager import CustomerMessageManager
from api_configuration_manager import APIConfigurationManager
from category_manager import ProductCategoriesManager
from engagement_metrics_manager import EngagementMetricsManager
from order_history_manager import OrderHistoryManager
from promotions_manager import PromotionManager
from chatbot_config_manager import ChatbotConfigManager
from db_config import (
    products_container,
    customers_container,
    feedback_container,
    customer_messages_container,
    promotions_container,
    engagement_metrics_container,
    order_history_container,
    categories_container
)

class MainTabbedNavigation(TabbedPanel):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.do_default_tab = False  # Disable default tab

        # Add Home Tab
        self.add_tab("Home", self.create_home_tab())
        self.default_tab = self.tab_list[0]  # Set the Home tab as the default

        # Add Other Tabs
        self.add_tab("Product", ProductInventoryManager())
        self.add_tab("Customer", CustomerInformationManager())
        self.add_tab("Feedback", FeedbackManager())
        self.add_tab("Chatbot", ChatbotConfigManager())
        self.add_tab("Messages", CustomerMessageManager())
        self.add_tab("Promotions", PromotionManager())
        self.add_tab("Order", OrderHistoryManager())
        self.add_tab("Engagement", EngagementMetricsManager())
        self.add_tab("API", APIConfigurationManager())
        self.add_tab("Categories", ProductCategoriesManager())

    def add_tab(self, title, content):
        tab = TabbedPanelItem(text=title)
        tab.add_widget(content)
        self.add_widget(tab)

    def create_home_tab(self):
        home_layout = GridLayout(cols=4, size_hint=(1, 1), padding=10, spacing=10)

        # Create charts for each entity
        entities = [
            ("Product", self.create_product_chart()),
            ("Customer", self.get_entity_count(customers_container)),
            ("Feedback", self.get_entity_count(feedback_container)),
            ("Messages", self.get_entity_count(customer_messages_container)),
            ("Promotions", self.get_entity_count(promotions_container)),
            ("Order", self.get_entity_count(order_history_container)),
            ("Categories", self.get_entity_count(categories_container)),
            ("Engagement", self.get_entity_count(engagement_metrics_container))
        ]

        for entity_name, chart in entities:
            if entity_name == "Product":
                home_layout.add_widget(chart)
            else:
                pie_chart = self.create_pie_chart(entity_name, chart)
                home_layout.add_widget(pie_chart)

        return home_layout

    def get_entity_count(self, container):
        return len(list(container.query_items(query="SELECT * FROM c", enable_cross_partition_query=True)))

    def create_product_chart(self):
        products = list(products_container.query_items(query="SELECT * FROM c", enable_cross_partition_query=True))
        categories = {}
        for product in products:
            category = product.get('category_id', 'Unknown')
            categories[category] = categories.get(category, 0) + 1

        plt.figure(figsize=(4, 5))
        plt.bar(categories.keys(), categories.values(), color='skyblue')
        plt.xlabel('Category')
        plt.ylabel('Number of Products')
        plt.title('Inventory Distribution by Category')

        buf = io.BytesIO()
        plt.savefig(buf, format='png')
        buf.seek(0)
        chart_image = CoreImage(buf, ext='png').texture
        buf.close()

        return Image(texture=chart_image, size_hint=(1, 1))

    def create_pie_chart(self, entity_name, count):
        count = max(count, 0)
        others = max(100 - count, 0)

        plt.figure(figsize=(4, 5))
        plt.pie([count, others], labels=[entity_name, "Others"], autopct='%1.1f%%', startangle=90)
        plt.title(entity_name)

        buf = io.BytesIO()
        plt.savefig(buf, format='png')
        buf.seek(0)
        chart_image = CoreImage(buf, ext='png').texture
        buf.close()

        return Image(texture=chart_image, size_hint=(1, 1))

class MainApp(App):
    def build(self):
        return MainTabbedNavigation()

if __name__ == '__main__':
    MainApp().run()

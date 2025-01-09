from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.spinner import Spinner
from kivy.uix.popup import Popup
from kivy.uix.image import Image
from kivy.uix.screenmanager import ScreenManager, Screen
from db_config import order_history_container, customers_container, products_container
import random
import matplotlib.pyplot as plt
import io
from kivy.core.image import Image as CoreImage
from kivy.graphics import Color, Rectangle

class OrderHistoryManager(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'

        # Title with Background
        with self.canvas.before:
            Color(0.2, 0.6, 0.8, 1)
            self.rect = Rectangle(size=self.size, pos=self.pos)
            self.bind(size=self._update_rect, pos=self._update_rect)

        # Header Layout with Navigation Button
        header_layout = BoxLayout(orientation='horizontal', size_hint_y=None, height=80, padding=10, spacing=10)
        back_button = Button(text="Back", size_hint=(None, None), size=(100, 40))
        back_button.bind(on_press=self.navigate_back)
        header_image = Image(source='order_history_icon.png', size_hint=(None, None), size=(60, 60))
        header_label = Label(text="[b]Order History Manager[/b]", font_size='28sp', markup=True)
        header_layout.add_widget(back_button)
        header_layout.add_widget(header_image)
        header_layout.add_widget(header_label)
        self.add_widget(header_layout)

        # Input Form Layout
        form_layout = GridLayout(cols=2, size_hint_y=None, spacing=15, padding=10)
        form_layout.bind(minimum_height=form_layout.setter('height'))

        # Input Fields
        customers = [customer['id'] for customer in customers_container.query_items(query="SELECT * FROM c", enable_cross_partition_query=True)]
        products = [product['id'] for product in products_container.query_items(query="SELECT * FROM c", enable_cross_partition_query=True)]

        self.customer_spinner = Spinner(text="Select Customer", values=customers, size_hint_y=None, height=40)
        form_layout.add_widget(Label(text="Customer ID:", size_hint_y=None, height=40))
        form_layout.add_widget(self.customer_spinner)

        self.product_spinner = Spinner(text="Select Product", values=products, size_hint_y=None, height=40)
        form_layout.add_widget(Label(text="Product ID:", size_hint_y=None, height=40))
        form_layout.add_widget(self.product_spinner)

        self.quantity_input = TextInput(hint_text="Enter Quantity", size_hint_y=None, height=40)
        form_layout.add_widget(Label(text="Quantity:", size_hint_y=None, height=40))
        form_layout.add_widget(self.quantity_input)

        self.total_price_input = TextInput(hint_text="Enter Total Price", size_hint_y=None, height=40)
        form_layout.add_widget(Label(text="Total Price:", size_hint_y=None, height=40))
        form_layout.add_widget(self.total_price_input)

        self.add_widget(form_layout)

        # Buttons
        button_layout = BoxLayout(size_hint_y=None, height=50, spacing=10, padding=10)
        self.add_order_button = Button(text="Add Order", size_hint_x=0.5, background_color=(0.2, 0.6, 0.8, 1))
        self.add_order_button.bind(on_press=self.add_order)
        button_layout.add_widget(self.add_order_button)

        self.view_chart_button = Button(text="View Order Chart", size_hint_x=0.5, background_color=(0.2, 0.6, 0.8, 1))
        self.view_chart_button.bind(on_press=self.show_chart)
        button_layout.add_widget(self.view_chart_button)

        self.add_widget(button_layout)

        # Order List Header
        self.add_widget(Label(text="Order List", font_size='22sp', size_hint_y=None, height=40))

        # Scrollable Order List
        self.scroll_view = ScrollView(size_hint=(1, None), size_hint_y=1)
        self.order_list_layout = GridLayout(cols=1, size_hint_y=None, spacing=10, padding=10)
        self.order_list_layout.bind(minimum_height=self.order_list_layout.setter('height'))
        self.scroll_view.add_widget(self.order_list_layout)
        self.add_widget(self.scroll_view)

        # Load Order List
        self.load_orders()

    def _update_rect(self, instance, value):
        self.rect.size = instance.size
        self.rect.pos = instance.pos

    def navigate_back(self, instance):
        # Logic to navigate back to the main screen
        app = App.get_running_app()
        app.root.current = 'main_screen'

    def add_order(self, instance):
        customer_id = self.customer_spinner.text
        product_id = self.product_spinner.text
        quantity = self.quantity_input.text
        total_price = self.total_price_input.text

        if not customer_id or not product_id or not quantity or not total_price:
            popup = Popup(title="Error", content=Label(text="All fields are required!"), size_hint=(0.8, 0.4))
            popup.open()
            return

        order = {
            "id": f"order-{random.randint(1000, 9999)}",
            "customer_id": customer_id,
            "product_id": product_id,
            "quantity": int(quantity),
            "total_price": float(total_price)
        }
        order_history_container.create_item(body=order)

        self.load_orders()

        self.quantity_input.text = ""
        self.total_price_input.text = ""

    def load_orders(self):
        self.order_list_layout.clear_widgets()
        orders = order_history_container.query_items(query="SELECT * FROM c", enable_cross_partition_query=True)
        for order in orders:
            order_box = BoxLayout(orientation='horizontal', size_hint_y=None, height=40, spacing=10)

            order_label = Label(text=f"Order ID: {order['id']} | Customer: {order['customer_id']} | Product: {order['product_id']} | Quantity: {order['quantity']} | Total Price: ${order['total_price']}")
            order_box.add_widget(order_label)

            edit_button = Button(text="Edit", size_hint_x=0.2, on_press=lambda instance, o=order: self.edit_order(o))
            order_box.add_widget(edit_button)

            delete_button = Button(text="Delete", size_hint_x=0.2, on_press=lambda instance, o=order: self.delete_order(o))
            order_box.add_widget(delete_button)

            self.order_list_layout.add_widget(order_box)

    def edit_order(self, order):
        self.customer_spinner.text = order['customer_id']
        self.product_spinner.text = order['product_id']
        self.quantity_input.text = str(order['quantity'])
        self.total_price_input.text = str(order['total_price'])

        def save_changes(instance):
            order['customer_id'] = self.customer_spinner.text
            order['product_id'] = self.product_spinner.text
            order['quantity'] = int(self.quantity_input.text)
            order['total_price'] = float(self.total_price_input.text)

            order_history_container.upsert_item(body=order)
            self.load_orders()

        self.add_order_button.text = "Save Changes"
        self.add_order_button.unbind(on_press=self.add_order)
        self.add_order_button.bind(on_press=save_changes)

    def delete_order(self, order):
        order_history_container.delete_item(item=order['id'], partition_key=order['id'])
        self.load_orders()

    def show_chart(self, instance):
        orders = list(order_history_container.query_items(query="SELECT * FROM c", enable_cross_partition_query=True))
        products = {}
        for order in orders:
            product = order.get('product_id', 'Unknown')
            products[product] = products.get(product, 0) + order['quantity']

        plt.bar(products.keys(), products.values(), color='skyblue')
        plt.xlabel('Product ID')
        plt.ylabel('Total Quantity Ordered')
        plt.title('Order Distribution by Product')

        buf = io.BytesIO()
        plt.savefig(buf, format='png')
        buf.seek(0)
        chart_image = CoreImage(buf, ext='png').texture

        popup = Popup(title="Order Chart", content=Image(texture=chart_image),  size_hint=(0.9, 0.7))

        popup.open()
        buf.close()

class OrderHistoryManagerApp(App):
    def build(self):
        return OrderHistoryManager()

if __name__ == "__main__":
    OrderHistoryManagerApp().run()

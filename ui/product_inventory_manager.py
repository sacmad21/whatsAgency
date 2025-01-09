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
from db_config import products_container, categories_container
import random
import matplotlib.pyplot as plt
import io
from kivy.core.image import Image as CoreImage
from kivy.graphics import Color, Rectangle

class ProductInventoryManager(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'

        # Title with Background
        with self.canvas.before:
            Color(0.2, 0.6, 0.8, 1)
            self.rect = Rectangle(size=self.size, pos=self.pos)
            self.bind(size=self._update_rect, pos=self._update_rect)

        # Header Layout with Animation Placeholder
        header_layout = BoxLayout(orientation='horizontal', size_hint_y=None, height=80, padding=10, spacing=10)
        header_image = Image(source='inventory_icon.png', size_hint=(None, None), size=(60, 60))
        header_label = Label(text="[b]Product Inventory Manager[/b]", font_size='28sp', markup=True)
        header_layout.add_widget(header_image)
        header_layout.add_widget(header_label)
        self.add_widget(header_layout)

        # Input Form Layout
        form_layout = GridLayout(cols=2, size_hint_y=None, spacing=15, padding=10)
        form_layout.bind(minimum_height=form_layout.setter('height'))

        # Input Fields
        categories = [category['name'] for category in categories_container.query_items(query="SELECT * FROM c", enable_cross_partition_query=True)]
        self.category_spinner = Spinner(text="Select Category", values=categories, size_hint_y=None, height=40)
        form_layout.add_widget(Label(text="Category:", size_hint_y=None, height=40))
        form_layout.add_widget(self.category_spinner)

        self.name_input = TextInput(hint_text="Enter Product Name", size_hint_y=None, height=40)
        form_layout.add_widget(Label(text="Product Name:", size_hint_y=None, height=40))
        form_layout.add_widget(self.name_input)

        self.price_input = TextInput(hint_text="Enter Price", size_hint_y=None, height=40)
        form_layout.add_widget(Label(text="Price:", size_hint_y=None, height=40))
        form_layout.add_widget(self.price_input)

        self.description_input = TextInput(hint_text="Enter Description", multiline=True, size_hint_y=None, height=80)
        form_layout.add_widget(Label(text="Description:", size_hint_y=None, height=40))
        form_layout.add_widget(self.description_input)

        self.availability_spinner = Spinner(text="In Stock", values=["In Stock", "Out of Stock"], size_hint_y=None, height=40)
        form_layout.add_widget(Label(text="Availability:", size_hint_y=None, height=40))
        form_layout.add_widget(self.availability_spinner)

        self.add_widget(form_layout)

        # Buttons
        button_layout = BoxLayout(size_hint_y=None, height=50, spacing=10, padding=10)
        self.add_product_button = Button(text="Add Product", size_hint_x=0.5, background_color=(0.2, 0.6, 0.8, 1))
        self.add_product_button.bind(on_press=self.add_product)
        button_layout.add_widget(self.add_product_button)

        self.view_chart_button = Button(text="View Inventory Chart", size_hint_x=0.5, background_color=(0.2, 0.6, 0.8, 1))
        self.view_chart_button.bind(on_press=self.show_chart)
        button_layout.add_widget(self.view_chart_button)

        self.add_widget(button_layout)

        # Product List Header
        self.add_widget(Label(text="Product List", font_size='22sp', size_hint_y=None, height=40))

        # Scrollable Product List
        self.scroll_view = ScrollView(size_hint=(1, None), size_hint_y=1)
        self.product_list_layout = GridLayout(cols=1, size_hint_y=None, spacing=10, padding=10)
        self.product_list_layout.bind(minimum_height=self.product_list_layout.setter('height'))
        self.scroll_view.add_widget(self.product_list_layout)
        self.add_widget(self.scroll_view)

        # Load Product List
        self.load_products()

    def _update_rect(self, instance, value):
        self.rect.size = instance.size
        self.rect.pos = instance.pos

    def add_product(self, instance):
        category_name = self.category_spinner.text
        name = self.name_input.text
        price = self.price_input.text
        description = self.description_input.text
        availability = self.availability_spinner.text

        if not name or not price or not description or category_name == "Select Category":
            popup = Popup(title="Error", content=Label(text="All fields are required!"), size_hint=(0.8, 0.4))
            popup.open()
            return

        category_id = next((category['id'] for category in categories_container.query_items(query="SELECT * FROM c", enable_cross_partition_query=True) if category['name'] == category_name), None)

        if not category_id:
            popup = Popup(title="Error", content=Label(text="Invalid category selected!"), size_hint=(0.8, 0.4))
            popup.open()
            return

        product = {
            "id": f"prod-{random.randint(1000, 9999)}",
            "category_id": category_id,
            "name": name,
            "price": float(price),
            "availability": availability == "In Stock",
            "description": description
        }
        products_container.create_item(body=product)

        self.load_products()

        self.name_input.text = ""
        self.price_input.text = ""
        self.description_input.text = ""

    def load_products(self):
        self.product_list_layout.clear_widgets()
        categories = {category['id']: category['name'] for category in categories_container.query_items(query="SELECT * FROM c", enable_cross_partition_query=True)}
        products = products_container.query_items(query="SELECT * FROM c", enable_cross_partition_query=True)
        for product in products:
            category_name = categories.get(product['category_id'], "Unknown Category")
            product_box = BoxLayout(orientation='horizontal', size_hint_y=None, height=40, spacing=10)

            product_label = Label(text=f"{product['name']} | {category_name} | ${product['price']} | {'In Stock' if product['availability'] else 'Out of Stock'}")
            product_box.add_widget(product_label)

            edit_button = Button(text="Edit", size_hint_x=0.2, on_press=lambda instance, p=product: self.edit_product(p))
            product_box.add_widget(edit_button)

            delete_button = Button(text="Delete", size_hint_x=0.2, on_press=lambda instance, p=product: self.delete_product(p))
            product_box.add_widget(delete_button)

            self.product_list_layout.add_widget(product_box)

    def edit_product(self, product):
        self.name_input.text = product['name']
        self.price_input.text = str(product['price'])
        self.description_input.text = product['description']
        self.category_spinner.text = next((category['name'] for category in categories_container.query_items(query="SELECT * FROM c", enable_cross_partition_query=True) if category['id'] == product['category_id']), "Select Category")
        self.availability_spinner.text = "In Stock" if product['availability'] else "Out of Stock"

        def save_changes(instance):
            product['name'] = self.name_input.text
            product['price'] = float(self.price_input.text)
            product['description'] = self.description_input.text
            product['availability'] = self.availability_spinner.text == "In Stock"
            product['category_id'] = next((category['id'] for category in categories_container.query_items(query="SELECT * FROM c", enable_cross_partition_query=True) if category['name'] == self.category_spinner.text), None)

            products_container.upsert_item(body=product)
            self.load_products()

        self.add_product_button.text = "Save Changes"
        self.add_product_button.unbind(on_press=self.add_product)
        self.add_product_button.bind(on_press=save_changes)

    def delete_product(self, product):
        products_container.delete_item(item=product['id'], partition_key=product['id'])
        self.load_products()

    def show_chart(self, instance):
        products = list(products_container.query_items(query="SELECT * FROM c", enable_cross_partition_query=True))
        categories = {}
        for product in products:
            category = product.get('category_id', 'Unknown')
            categories[category] = categories.get(category, 0) + 1

        plt.bar(categories.keys(), categories.values(), color='skyblue')
        plt.xlabel('Category')
        plt.ylabel('Number of Products')
        plt.title('Inventory Distribution by Category')

        buf = io.BytesIO()
        plt.savefig(buf, format='png')
        buf.seek(0)
        chart_image = CoreImage(buf, ext='png').texture

        popup = Popup(title="Inventory Chart", content=Image(texture=chart_image), size_hint=(0.9, 0.7))
        popup.open()
        buf.close()

class ProductInventoryApp(App):
    def build(self):
        return ProductInventoryManager()

if __name__ == "__main__":
    ProductInventoryApp().run()

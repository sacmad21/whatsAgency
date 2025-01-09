from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.spinner import Spinner
from kivy.uix.popup import Popup
from kivy.graphics import Color, Rectangle
from db_config import promotions_container, categories_container, products_container
import random
import datetime

class PromotionManager(BoxLayout):
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
        header_label = Label(text="[b]Promotion Manager[/b]", font_size='28sp', markup=True)
        header_layout.add_widget(back_button)
        header_layout.add_widget(header_label)
        self.add_widget(header_layout)

        # Input Form Layout
        form_layout = GridLayout(cols=2, size_hint_y=None, spacing=15, padding=10)
        form_layout.bind(minimum_height=form_layout.setter('height'))

        # Input Fields
        categories = [category['name'] for category in categories_container.query_items(query="SELECT * FROM c", enable_cross_partition_query=True)]
        products = [product['name'] for product in products_container.query_items(query="SELECT * FROM c", enable_cross_partition_query=True)]

        self.category_spinner = Spinner(text="Select Category", values=categories, size_hint_y=None, height=40)
        form_layout.add_widget(Label(text="Category:", size_hint_y=None, height=40))
        form_layout.add_widget(self.category_spinner)

        self.product_spinner = Spinner(text="Select Product", values=products, size_hint_y=None, height=40)
        form_layout.add_widget(Label(text="Product:", size_hint_y=None, height=40))
        form_layout.add_widget(self.product_spinner)

        self.description_input = TextInput(hint_text="Enter Promotion Description", multiline=True, size_hint_y=None, height=80)
        form_layout.add_widget(Label(text="Description:", size_hint_y=None, height=40))
        form_layout.add_widget(self.description_input)

        self.start_date_input = TextInput(hint_text="YYYY-MM-DD", size_hint_y=None, height=40)
        form_layout.add_widget(Label(text="Start Date:", size_hint_y=None, height=40))
        form_layout.add_widget(self.start_date_input)

        self.end_date_input = TextInput(hint_text="YYYY-MM-DD", size_hint_y=None, height=40)
        form_layout.add_widget(Label(text="End Date:", size_hint_y=None, height=40))
        form_layout.add_widget(self.end_date_input)

        self.add_widget(form_layout)

        # Buttons
        button_layout = BoxLayout(size_hint_y=None, height=50, spacing=10, padding=10)
        self.add_promotion_button = Button(text="Add Promotion", size_hint_x=0.5, background_color=(0.2, 0.6, 0.8, 1))
        self.add_promotion_button.bind(on_press=self.add_promotion)
        button_layout.add_widget(self.add_promotion_button)

        self.add_widget(button_layout)

        # Promotion List Header
        self.add_widget(Label(text="Promotion List", font_size='22sp', size_hint_y=None, height=40))

        # Scrollable Promotion List
        self.scroll_view = ScrollView(size_hint=(1, None), size_hint_y=1)
        self.promotion_list_layout = GridLayout(cols=1, size_hint_y=None, spacing=10, padding=10)
        self.promotion_list_layout.bind(minimum_height=self.promotion_list_layout.setter('height'))
        self.scroll_view.add_widget(self.promotion_list_layout)
        self.add_widget(self.scroll_view)

        # Load Promotion List
        self.load_promotions()

    def _update_rect(self, instance, value):
        self.rect.size = instance.size
        self.rect.pos = instance.pos

    def navigate_back(self, instance):
        app = App.get_running_app()
        app.root.current = 'main_screen'

    def add_promotion(self, instance):
        category_name = self.category_spinner.text
        product_name = self.product_spinner.text
        description = self.description_input.text
        start_date = self.start_date_input.text
        end_date = self.end_date_input.text

        if not description or not start_date or not end_date:
            popup = Popup(title="Error", content=Label(text="All fields are required!"), size_hint=(0.8, 0.4))
            popup.open()
            return

        try:
            start_date_obj = datetime.datetime.strptime(start_date, "%Y-%m-%d")
            end_date_obj = datetime.datetime.strptime(end_date, "%Y-%m-%d")
        except ValueError:
            popup = Popup(title="Error", content=Label(text="Invalid date format. Use YYYY-MM-DD."), size_hint=(0.8, 0.4))
            popup.open()
            return

        category_id = next((category['id'] for category in categories_container.query_items(query="SELECT * FROM c", enable_cross_partition_query=True) if category['name'] == category_name), None)
        product_id = next((product['id'] for product in products_container.query_items(query="SELECT * FROM c", enable_cross_partition_query=True) if product['name'] == product_name), None)

        promotion = {
            "id": f"promo-{random.randint(1000, 9999)}",
            "category_id": category_id,
            "product_id": product_id,
            "description": description,
            "start_date": start_date,
            "end_date": end_date
        }
        promotions_container.create_item(body=promotion)

        self.load_promotions()

        self.description_input.text = ""
        self.start_date_input.text = ""
        self.end_date_input.text = ""

    def load_promotions(self):
        self.promotion_list_layout.clear_widgets()
        promotions = promotions_container.query_items(query="SELECT * FROM c", enable_cross_partition_query=True)
        for promotion in promotions:
            promotion_box = BoxLayout(orientation='horizontal', size_hint_y=None, height=40, spacing=10)

            promotion_label = Label(text=f"{promotion['description']} | {promotion['start_date']} - {promotion['end_date']}")
            promotion_box.add_widget(promotion_label)

            edit_button = Button(text="Edit", size_hint_x=0.2, on_press=lambda instance, p=promotion: self.edit_promotion(p))
            promotion_box.add_widget(edit_button)

            delete_button = Button(text="Delete", size_hint_x=0.2, on_press=lambda instance, p=promotion: self.delete_promotion(p))
            promotion_box.add_widget(delete_button)

            self.promotion_list_layout.add_widget(promotion_box)

    def edit_promotion(self, promotion):
        self.description_input.text = promotion['description']
        self.start_date_input.text = promotion['start_date']
        self.end_date_input.text = promotion['end_date']

        def save_changes(instance):
            promotion['description'] = self.description_input.text
            promotion['start_date'] = self.start_date_input.text
            promotion['end_date'] = self.end_date_input.text

            promotions_container.upsert_item(body=promotion)
            self.load_promotions()

        self.add_promotion_button.text = "Save Changes"
        self.add_promotion_button.unbind(on_press=self.add_promotion)
        self.add_promotion_button.bind(on_press=save_changes)

    def delete_promotion(self, promotion):
        promotions_container.delete_item(item=promotion['id'], partition_key=promotion['id'])
        self.load_promotions()

class PromotionManagerApp(App):
    def build(self):
        return PromotionManager()

if __name__ == "__main__":
    PromotionManagerApp().run()

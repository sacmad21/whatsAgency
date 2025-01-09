from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.popup import Popup
from kivy.uix.spinner import Spinner
from kivy.uix.image import Image
from kivy.graphics import Color, Rectangle
from db_config import customers_container
import random
import matplotlib.pyplot as plt
import io
from kivy.core.image import Image as CoreImage

class CustomerInformationManager(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'

        # Title with Background
        with self.canvas.before:
            Color(0.2, 0.6, 0.8, 1)
            self.rect = Rectangle(size=self.size, pos=self.pos)
            self.bind(size=self._update_rect, pos=self._update_rect)

        # Header Layout with Back Button
        header_layout = BoxLayout(orientation='horizontal', size_hint_y=None, height=80, padding=10, spacing=10)
        back_button = Button(text="Back", size_hint=(None, None), size=(100, 40))
        back_button.bind(on_press=self.navigate_back)
        header_image = Image(source='customer_icon.png', size_hint=(None, None), size=(60, 60))
        header_label = Label(text="[b]Customer Information Manager[/b]", font_size='28sp', markup=True)
        header_layout.add_widget(back_button)
        header_layout.add_widget(header_image)
        header_layout.add_widget(header_label)
        self.add_widget(header_layout)

        # Input Form Layout
        form_layout = GridLayout(cols=2, size_hint_y=None, spacing=15, padding=10)
        form_layout.bind(minimum_height=form_layout.setter('height'))

        # Input Fields
        self.name_input = TextInput(hint_text="Enter Customer Name", size_hint_y=None, height=40)
        form_layout.add_widget(Label(text="Name:", size_hint_y=None, height=40))
        form_layout.add_widget(self.name_input)

        self.preference_input = TextInput(hint_text="Enter Preferences (comma-separated)", size_hint_y=None, height=40)
        form_layout.add_widget(Label(text="Preferences:", size_hint_y=None, height=40))
        form_layout.add_widget(self.preference_input)

        self.add_widget(form_layout)

        # Buttons
        button_layout = BoxLayout(size_hint_y=None, height=50, spacing=10, padding=10)
        self.add_customer_button = Button(text="Add Customer", size_hint_x=0.5, background_color=(0.2, 0.6, 0.8, 1))
        self.add_customer_button.bind(on_press=self.add_customer)
        button_layout.add_widget(self.add_customer_button)

        self.view_chart_button = Button(text="View Chart", size_hint_x=0.5, background_color=(0.2, 0.6, 0.8, 1))
        self.view_chart_button.bind(on_press=self.show_chart)
        button_layout.add_widget(self.view_chart_button)

        self.add_widget(button_layout)

        # Customer List Header
        self.add_widget(Label(text="Customer List", font_size='22sp', size_hint_y=None, height=40))

        # Scrollable Customer List
        self.scroll_view = ScrollView(size_hint=(1, None), size_hint_y=1)
        self.customer_list_layout = GridLayout(cols=1, size_hint_y=None, spacing=10, padding=10)
        self.customer_list_layout.bind(minimum_height=self.customer_list_layout.setter('height'))
        self.scroll_view.add_widget(self.customer_list_layout)
        self.add_widget(self.scroll_view)

        # Load Customer List
        self.load_customers()

    def _update_rect(self, instance, value):
        self.rect.size = instance.size
        self.rect.pos = instance.pos

    def navigate_back(self, instance):
        app = App.get_running_app()
        app.root.current = 'main_screen'

    def add_customer(self, instance):
        name = self.name_input.text
        preferences = self.preference_input.text

        if not name or not preferences:
            popup = Popup(title="Error", content=Label(text="All fields are required!"), size_hint=(0.8, 0.4))
            popup.open()
            return

        customer = {
            "id": f"cust-{random.randint(1000, 9999)}",
            "name": name,
            "preferences": preferences.split(",")
        }
        customers_container.create_item(body=customer)
        self.load_customers()
        self.name_input.text = ""
        self.preference_input.text = ""

    def load_customers(self):
        self.customer_list_layout.clear_widgets()
        customers = customers_container.query_items(query="SELECT * FROM c", enable_cross_partition_query=True)
        for customer in customers:
            customer_box = BoxLayout(orientation='horizontal', size_hint_y=None, height=40, spacing=10)

            customer_label = Label(text=f"{customer['name']} | Preferences: {', '.join(customer['preferences'])}")
            customer_box.add_widget(customer_label)

            edit_button = Button(text="Edit", size_hint_x=0.2, on_press=lambda instance, c=customer: self.edit_customer(c))
            customer_box.add_widget(edit_button)

            delete_button = Button(text="Delete", size_hint_x=0.2, on_press=lambda instance, c=customer: self.delete_customer(c))
            customer_box.add_widget(delete_button)

            self.customer_list_layout.add_widget(customer_box)

    def edit_customer(self, customer):
        self.name_input.text = customer['name']
        self.preference_input.text = ", ".join(customer['preferences'])

        def save_changes(instance):
            customer['name'] = self.name_input.text
            customer['preferences'] = self.preference_input.text.split(",")
            customers_container.upsert_item(body=customer)
            self.load_customers()

        self.add_customer_button.text = "Save Changes"
        self.add_customer_button.unbind(on_press=self.add_customer)
        self.add_customer_button.bind(on_press=save_changes)

    def delete_customer(self, customer):
        customers_container.delete_item(item=customer['id'], partition_key=customer['id'])
        self.load_customers()

    def show_chart(self, instance):
        customers = list(customers_container.query_items(query="SELECT * FROM c", enable_cross_partition_query=True))
        preferences = {}
        for customer in customers:
            for preference in customer['preferences']:
                preferences[preference] = preferences.get(preference, 0) + 1

        plt.bar(preferences.keys(), preferences.values(), color='skyblue')
        plt.xlabel('Preferences')
        plt.ylabel('Number of Customers')
        plt.title('Customer Preferences Distribution')

        buf = io.BytesIO()
        plt.savefig(buf, format='png')
        buf.seek(0)
        chart_image = CoreImage(buf, ext='png').texture

        popup = Popup(title="Preferences Chart", content=Image(texture=chart_image), size_hint=(0.9, 0.7))
        popup.open()
        buf.close()

class CustomerInformationApp(App):
    def build(self):
        return CustomerInformationManager()

if __name__ == "__main__":
    CustomerInformationApp().run()

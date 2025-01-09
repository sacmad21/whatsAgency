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
from db_config import customer_messages_container
import random
import matplotlib.pyplot as plt
import io
from kivy.core.image import Image as CoreImage
from kivy.graphics import Color, Rectangle

class CustomerMessageManager(BoxLayout):
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
        header_image = Image(source='messages_icon.png', size_hint=(None, None), size=(60, 60))
        header_label = Label(text="[b]Customer Message Manager[/b]", font_size='28sp', markup=True)
        header_layout.add_widget(back_button)
        header_layout.add_widget(header_image)
        header_layout.add_widget(header_label)
        self.add_widget(header_layout)

        # Input Form Layout
        form_layout = GridLayout(cols=2, size_hint_y=None, spacing=15, padding=10)
        form_layout.bind(minimum_height=form_layout.setter('height'))

        # Input Fields
        self.customer_id_input = TextInput(hint_text="Enter Customer ID", size_hint_y=None, height=40)
        form_layout.add_widget(Label(text="Customer ID:", size_hint_y=None, height=40))
        form_layout.add_widget(self.customer_id_input)

        self.message_body_input = TextInput(hint_text="Enter Message Body", multiline=True, size_hint_y=None, height=80)
        form_layout.add_widget(Label(text="Message Body:", size_hint_y=None, height=40))
        form_layout.add_widget(self.message_body_input)

        self.direction_spinner = Spinner(text="Select Direction", values=["Incoming", "Outgoing"], size_hint_y=None, height=40)
        form_layout.add_widget(Label(text="Direction:", size_hint_y=None, height=40))
        form_layout.add_widget(self.direction_spinner)

        self.add_widget(form_layout)

        # Buttons
        button_layout = BoxLayout(size_hint_y=None, height=50, spacing=10, padding=10)
        self.add_message_button = Button(text="Add Message", size_hint_x=0.5, background_color=(0.2, 0.6, 0.8, 1))
        self.add_message_button.bind(on_press=self.add_message)
        button_layout.add_widget(self.add_message_button)

        self.view_chart_button = Button(text="View Message Chart", size_hint_x=0.5, background_color=(0.2, 0.6, 0.8, 1))
        self.view_chart_button.bind(on_press=self.show_chart)
        button_layout.add_widget(self.view_chart_button)

        self.add_widget(button_layout)

        # Message List Header
        self.add_widget(Label(text="Message List", font_size='22sp', size_hint_y=None, height=40))

        # Scrollable Message List
        self.scroll_view = ScrollView(size_hint=(1, None), size_hint_y=1)
        self.message_list_layout = GridLayout(cols=1, size_hint_y=None, spacing=10, padding=10)
        self.message_list_layout.bind(minimum_height=self.message_list_layout.setter('height'))
        self.scroll_view.add_widget(self.message_list_layout)
        self.add_widget(self.scroll_view)

        # Load Message List
        self.load_messages()

    def _update_rect(self, instance, value):
        self.rect.size = instance.size
        self.rect.pos = instance.pos

    def navigate_back(self, instance):
        # Logic to navigate back to the main screen
        app = App.get_running_app()
        app.root.current = 'main_screen'

    def add_message(self, instance):
        customer_id = self.customer_id_input.text
        message_body = self.message_body_input.text
        direction = self.direction_spinner.text

        if not customer_id or not message_body or direction == "Select Direction":
            popup = Popup(title="Error", content=Label(text="All fields are required!"), size_hint=(0.8, 0.4))
            popup.open()
            return

        message = {
            "id": f"msg-{random.randint(1000, 9999)}",
            "customer_id": customer_id,
            "message_body": message_body,
            "direction": direction,
            "timestamp": random.randint(1633046400, 1635724800)  # Placeholder timestamp
        }
        customer_messages_container.create_item(body=message)

        self.load_messages()

        self.customer_id_input.text = ""
        self.message_body_input.text = ""
        self.direction_spinner.text = "Select Direction"

    def load_messages(self):
        self.message_list_layout.clear_widgets()
        messages = customer_messages_container.query_items(query="SELECT * FROM c", enable_cross_partition_query=True)
        for message in messages:
            message_box = BoxLayout(orientation='horizontal', size_hint_y=None, height=40, spacing=10)

            message_label = Label(text=f"{message['customer_id']} | {message['message_body']} | {message['direction']}")
            message_box.add_widget(message_label)

            edit_button = Button(text="Edit", size_hint_x=0.2, on_press=lambda instance, m=message: self.edit_message(m))
            message_box.add_widget(edit_button)

            delete_button = Button(text="Delete", size_hint_x=0.2, on_press=lambda instance, m=message: self.delete_message(m))
            message_box.add_widget(delete_button)

            self.message_list_layout.add_widget(message_box)

    def edit_message(self, message):
        self.customer_id_input.text = message['customer_id']
        self.message_body_input.text = message['message_body']
        self.direction_spinner.text = message['direction']

        def save_changes(instance):
            message['customer_id'] = self.customer_id_input.text
            message['message_body'] = self.message_body_input.text
            message['direction'] = self.direction_spinner.text

            customer_messages_container.upsert_item(body=message)
            self.load_messages()

        self.add_message_button.text = "Save Changes"
        self.add_message_button.unbind(on_press=self.add_message)
        self.add_message_button.bind(on_press=save_changes)

    def delete_message(self, message):
        customer_messages_container.delete_item(item=message['id'], partition_key=message['id'])
        self.load_messages()

    def show_chart(self, instance):
        messages = list(customer_messages_container.query_items(query="SELECT * FROM c", enable_cross_partition_query=True))
        directions = {"INCOMING": 0, "OUTGOING": 0}
        for message in messages:
            directions[message['direction'].upper()] += 1

        plt.bar(directions.keys(), directions.values(), color='skyblue')
        plt.xlabel('Direction')
        plt.ylabel('Number of Messages')
        plt.title('Message Distribution by Direction')

        buf = io.BytesIO()
        plt.savefig(buf, format='png')
        buf.seek(0)
        chart_image = CoreImage(buf, ext='png').texture

        popup = Popup(title="Message Chart", content=Image(texture=chart_image), size_hint=(0.9, 0.7))
        popup.open()
        buf.close()

class CustomerMessageApp(App):
    def build(self):
        return CustomerMessageManager()

if __name__ == "__main__":
    CustomerMessageApp().run()

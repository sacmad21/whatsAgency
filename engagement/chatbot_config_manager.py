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
from kivy.graphics import Color, Rectangle
from db_config import bot_config_container
import random
import matplotlib.pyplot as plt
import io
from kivy.core.image import Image as CoreImage

class ChatbotConfigManager(BoxLayout):
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
        header_image = Image(source='chatbot_icon.png', size_hint=(None, None), size=(60, 60))
        header_label = Label(text="[b]Chatbot Config Manager[/b]", font_size='28sp', markup=True)
        header_layout.add_widget(back_button)
        header_layout.add_widget(header_image)
        header_layout.add_widget(header_label)
        self.add_widget(header_layout)

        # Input Form Layout
        form_layout = GridLayout(cols=2, size_hint_y=None, spacing=15, padding=10)
        form_layout.bind(minimum_height=form_layout.setter('height'))

        # Input Fields
        self.key_input = TextInput(hint_text="Enter Config Key", size_hint_y=None, height=40)
        form_layout.add_widget(Label(text="Config Key:", size_hint_y=None, height=40))
        form_layout.add_widget(self.key_input)

        self.value_input = TextInput(hint_text="Enter Config Value", size_hint_y=None, height=40)
        form_layout.add_widget(Label(text="Config Value:", size_hint_y=None, height=40))
        form_layout.add_widget(self.value_input)

        self.add_widget(form_layout)

        # Buttons
        button_layout = BoxLayout(size_hint_y=None, height=50, spacing=10, padding=10)
        self.add_placeholder_button = Button(text="Add", size_hint_x=0.5, background_color=(0.2, 0.6, 0.8, 1))
        self.add_placeholder_button.bind(on_press=self.add_placeholder)
        button_layout.add_widget(self.add_placeholder_button)

        self.view_chart_button = Button(text="View Chart", size_hint_x=0.5, background_color=(0.2, 0.6, 0.8, 1))
        self.view_chart_button.bind(on_press=self.show_chart)
        button_layout.add_widget(self.view_chart_button)

        self.add_widget(button_layout)

        # Placeholder List Header
        self.add_widget(Label(text="Config", font_size='22sp', size_hint_y=None, height=40))

        # Scrollable Placeholder List
        self.scroll_view = ScrollView(size_hint=(1, None), size_hint_y=1)
        self.placeholder_list_layout = GridLayout(cols=1, size_hint_y=None, spacing=10, padding=10)
        self.placeholder_list_layout.bind(minimum_height=self.placeholder_list_layout.setter('height'))
        self.scroll_view.add_widget(self.placeholder_list_layout)
        self.add_widget(self.scroll_view)

        # Load Placeholder List
        self.load_placeholders()

    def _update_rect(self, instance, value):
        self.rect.size = instance.size
        self.rect.pos = instance.pos

    def navigate_back(self, instance):
        # Logic to navigate back to the main screen
        app = App.get_running_app()
        app.root.current = 'main_screen'

    def add_placeholder(self, instance):
        key = self.key_input.text
        value = self.value_input.text

        if not key or not value:
            popup = Popup(title="Error", content=Label(text="Both fields are required!"), size_hint=(0.8, 0.4))
            popup.open()
            return

        placeholder = {
            "id": f"config-{random.randint(1000, 9999)}",
            "key": key,
            "value": value
        }
        bot_config_container.create_item(body=placeholder)

        self.load_placeholders()

        self.key_input.text = ""
        self.value_input.text = ""

    def load_placeholders(self):
        self.placeholder_list_layout.clear_widgets()
        placeholders = bot_config_container.query_items(query="SELECT * FROM c", enable_cross_partition_query=True)
        for placeholder in placeholders:
            placeholder_box = BoxLayout(orientation='horizontal', size_hint_y=None, height=40, spacing=10)

            placeholder_label = Label(text=f"Key: {placeholder['key']} | Value: {placeholder['value']}")
            placeholder_box.add_widget(placeholder_label)

            edit_button = Button(text="Edit", size_hint_x=0.2, on_press=lambda instance, p=placeholder: self.edit_placeholder(p))
            placeholder_box.add_widget(edit_button)

            delete_button = Button(text="Delete", size_hint_x=0.2, on_press=lambda instance, p=placeholder: self.delete_placeholder(p))
            placeholder_box.add_widget(delete_button)

            self.placeholder_list_layout.add_widget(placeholder_box)

    def edit_placeholder(self, placeholder):
        self.key_input.text = placeholder['key']
        self.value_input.text = placeholder['value']

        def save_changes(instance):
            placeholder['key'] = self.key_input.text
            placeholder['value'] = self.value_input.text

            bot_config_container.upsert_item(body=placeholder)
            self.load_placeholders()

        self.add_placeholder_button.text = "Save Changes"
        self.add_placeholder_button.unbind(on_press=self.add_placeholder)
        self.add_placeholder_button.bind(on_press=save_changes)

    def delete_placeholder(self, placeholder):
        bot_config_container.delete_item(item=placeholder['id'], partition_key=placeholder['id'])
        self.load_placeholders()

    def show_chart(self, instance):
        placeholders = list(bot_config_container.query_items(query="SELECT * FROM c", enable_cross_partition_query=True))
        keys = [placeholder['key'] for placeholder in placeholders]
        values = [len(placeholder['value']) for placeholder in placeholders]

        plt.bar(keys, values, color='skyblue')
        plt.xlabel('Keys')
        plt.ylabel('Value Length')
        plt.title('Chart Placeholder')

        buf = io.BytesIO()
        plt.savefig(buf, format='png')
        buf.seek(0)
        chart_image = CoreImage(buf, ext='png').texture

        popup = Popup(title="Chart Placeholder", content=Image(texture=chart_image), size_hint=(0.9, 0.7))
        popup.open()
        buf.close()

class ChatbotConfigApp(App):
    def build(self):
        return ChatbotConfigManager()

if __name__ == "__main__":
    ChatbotConfigApp().run()

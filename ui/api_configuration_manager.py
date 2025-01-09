from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.popup import Popup
from kivy.uix.image import Image
from kivy.graphics import Color, Rectangle
import random
import io
from kivy.core.image import Image as CoreImage
import matplotlib.pyplot as plt
from db_config import api_config_container

class APIConfigurationManager(BoxLayout):
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
        header_image = Image(source='api_icon.png', size_hint=(None, None), size=(60, 60))
        header_label = Label(text="[b]API Configuration Manager[/b]", font_size='28sp', markup=True)
        header_layout.add_widget(back_button)
        header_layout.add_widget(header_image)
        header_layout.add_widget(header_label)
        self.add_widget(header_layout)

        # Input Form Layout
        form_layout = GridLayout(cols=2, size_hint_y=None, spacing=15, padding=10)
        form_layout.bind(minimum_height=form_layout.setter('height'))

        # Input Fields
        self.key_input = TextInput(hint_text="Enter API Key", size_hint_y=None, height=40)
        form_layout.add_widget(Label(text="API Key:", size_hint_y=None, height=40))
        form_layout.add_widget(self.key_input)

        self.value_input = TextInput(hint_text="Enter API Value", size_hint_y=None, height=40)
        form_layout.add_widget(Label(text="API Value:", size_hint_y=None, height=40))
        form_layout.add_widget(self.value_input)

        self.add_widget(form_layout)

        # Buttons
        button_layout = BoxLayout(size_hint_y=None, height=50, spacing=10, padding=10)
        self.add_config_button = Button(text="Add Configuration", size_hint_x=0.5, background_color=(0.2, 0.6, 0.8, 1))
        self.add_config_button.bind(on_press=self.add_config)
        button_layout.add_widget(self.add_config_button)

        self.view_chart_button = Button(text="View Config Chart", size_hint_x=0.5, background_color=(0.2, 0.6, 0.8, 1))
        self.view_chart_button.bind(on_press=self.show_chart)
        button_layout.add_widget(self.view_chart_button)

        self.add_widget(button_layout)

        # Configuration List Header
        self.add_widget(Label(text="API Configurations", font_size='22sp', size_hint_y=None, height=40))

        # Scrollable Configuration List
        self.scroll_view = ScrollView(size_hint=(1, None), size_hint_y=1)
        self.config_list_layout = GridLayout(cols=1, size_hint_y=None, spacing=10, padding=10)
        self.config_list_layout.bind(minimum_height=self.config_list_layout.setter('height'))
        self.scroll_view.add_widget(self.config_list_layout)
        self.add_widget(self.scroll_view)

        # Load Configurations
        self.load_configurations()

    def _update_rect(self, instance, value):
        self.rect.size = instance.size
        self.rect.pos = instance.pos

    def navigate_back(self, instance):
        app = App.get_running_app()
        app.root.current = 'main_screen'

    def add_config(self, instance):
        key = self.key_input.text
        value = self.value_input.text

        if not key or not value:
            popup = Popup(title="Error", content=Label(text="Both fields are required!"), size_hint=(0.8, 0.4))
            popup.open()
            return

        config = {
            "id": f"config-{random.randint(1000, 9999)}",
            "key": key,
            "value": value
        }
        api_config_container.create_item(body=config)

        self.load_configurations()

        self.key_input.text = ""
        self.value_input.text = ""

    def load_configurations(self):
        self.config_list_layout.clear_widgets()
        configurations = api_config_container.query_items(query="SELECT * FROM c", enable_cross_partition_query=True)
        for config in configurations:
            config_box = BoxLayout(orientation='horizontal', size_hint_y=None, height=40, spacing=10)

            config_label = Label(text=f"{config['key']} | {config['value']}")
            config_box.add_widget(config_label)

            edit_button = Button(text="Edit", size_hint_x=0.2, on_press=lambda instance, c=config: self.edit_config(c))
            config_box.add_widget(edit_button)

            delete_button = Button(text="Delete", size_hint_x=0.2, on_press=lambda instance, c=config: self.delete_config(c))
            config_box.add_widget(delete_button)

            self.config_list_layout.add_widget(config_box)

    def edit_config(self, config):
        self.key_input.text = config['key']
        self.value_input.text = config['value']

        def save_changes(instance):
            config['key'] = self.key_input.text
            config['value'] = self.value_input.text

            api_config_container.upsert_item(body=config)
            self.load_configurations()

        self.add_config_button.text = "Save Changes"
        self.add_config_button.unbind(on_press=self.add_config)
        self.add_config_button.bind(on_press=save_changes)

    def delete_config(self, config):
        api_config_container.delete_item(item=config['id'], partition_key=config['id'])
        self.load_configurations()

    def show_chart(self, instance):
        configurations = list(api_config_container.query_items(query="SELECT * FROM c", enable_cross_partition_query=True))
        keys = [config['key'] for config in configurations]
        values = [len(config['value']) for config in configurations]

        plt.bar(keys, values, color='skyblue')
        plt.xlabel('Keys')
        plt.ylabel('Value Length')
        plt.title('API Configurations Overview')

        buf = io.BytesIO()
        plt.savefig(buf, format='png')
        buf.seek(0)
        chart_image = CoreImage(buf, ext='png').texture

        popup = Popup(title="Configuration Chart", content=Image(texture=chart_image), size_hint=(0.9, 0.7))
        popup.open()
        buf.close()

class APIConfigurationApp(App):
    def build(self):
        return APIConfigurationManager()

if __name__ == "__main__":
    APIConfigurationApp().run()

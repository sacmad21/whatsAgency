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
from db_config import categories_container
import random
import matplotlib.pyplot as plt
import io
from kivy.core.image import Image as CoreImage

class ProductCategoriesManager(BoxLayout):
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
        header_image = Image(source='categories_icon.png', size_hint=(None, None), size=(60, 60))
        header_label = Label(text="[b]Product Categories Manager[/b]", font_size='28sp', markup=True)
        header_layout.add_widget(back_button)
        header_layout.add_widget(header_image)
        header_layout.add_widget(header_label)
        self.add_widget(header_layout)

        # Input Form Layout
        form_layout = GridLayout(cols=2, size_hint_y=None, spacing=15, padding=10)
        form_layout.bind(minimum_height=form_layout.setter('height'))

        # Input Fields
        self.name_input = TextInput(hint_text="Enter Category Name", size_hint_y=None, height=40)
        form_layout.add_widget(Label(text="Category Name:", size_hint_y=None, height=40))
        form_layout.add_widget(self.name_input)

        self.description_input = TextInput(hint_text="Enter Description", multiline=True, size_hint_y=None, height=80)
        form_layout.add_widget(Label(text="Description:", size_hint_y=None, height=40))
        form_layout.add_widget(self.description_input)

        self.add_widget(form_layout)

        # Buttons
        button_layout = BoxLayout(size_hint_y=None, height=50, spacing=10, padding=10)
        self.add_category_button = Button(text="Add Category", size_hint_x=0.5, background_color=(0.2, 0.6, 0.8, 1))
        self.add_category_button.bind(on_press=self.add_category)
        button_layout.add_widget(self.add_category_button)

        self.view_chart_button = Button(text="View Categories Chart", size_hint_x=0.5, background_color=(0.2, 0.6, 0.8, 1))
        self.view_chart_button.bind(on_press=self.show_chart)
        button_layout.add_widget(self.view_chart_button)

        self.add_widget(button_layout)

        # Category List Header
        self.add_widget(Label(text="Category List", font_size='22sp', size_hint_y=None, height=40))

        # Scrollable Category List
        self.scroll_view = ScrollView(size_hint=(1, None), size_hint_y=1)
        self.category_list_layout = GridLayout(cols=1, size_hint_y=None, spacing=10, padding=10)
        self.category_list_layout.bind(minimum_height=self.category_list_layout.setter('height'))
        self.scroll_view.add_widget(self.category_list_layout)
        self.add_widget(self.scroll_view)

        # Load Category List
        self.load_categories()

    def _update_rect(self, instance, value):
        self.rect.size = instance.size
        self.rect.pos = instance.pos

    def navigate_back(self, instance):
        # Logic to navigate back to the main screen
        app = App.get_running_app()
        app.root.current = 'main_screen'

    def add_category(self, instance):
        name = self.name_input.text
        description = self.description_input.text

        if not name or not description:
            popup = Popup(title="Error", content=Label(text="All fields are required!"), size_hint=(0.8, 0.4))
            popup.open()
            return

        category = {
            "id": f"cat-{random.randint(1000, 9999)}",
            "name": name,
            "description": description
        }
        categories_container.create_item(body=category)

        self.load_categories()

        self.name_input.text = ""
        self.description_input.text = ""

    def load_categories(self):
        self.category_list_layout.clear_widgets()
        categories = categories_container.query_items(query="SELECT * FROM c", enable_cross_partition_query=True)
        for category in categories:
            category_box = BoxLayout(orientation='horizontal', size_hint_y=None, height=40, spacing=10)

            category_label = Label(text=f"{category['name']} | {category['description']}")
            category_box.add_widget(category_label)

            edit_button = Button(text="Edit", size_hint_x=0.2, on_press=lambda instance, c=category: self.edit_category(c))
            category_box.add_widget(edit_button)

            delete_button = Button(text="Delete", size_hint_x=0.2, on_press=lambda instance, c=category: self.delete_category(c))
            category_box.add_widget(delete_button)

            self.category_list_layout.add_widget(category_box)

    def edit_category(self, category):
        self.name_input.text = category['name']
        self.description_input.text = category['description']

        def save_changes(instance):
            category['name'] = self.name_input.text
            category['description'] = self.description_input.text

            categories_container.upsert_item(body=category)
            self.load_categories()

        self.add_category_button.text = "Save Changes"
        self.add_category_button.unbind(on_press=self.add_category)
        self.add_category_button.bind(on_press=save_changes)

    def delete_category(self, category):
        categories_container.delete_item(item=category['id'], partition_key=category['id'])
        self.load_categories()

    def show_chart(self, instance):
        categories = list(categories_container.query_items(query="SELECT * FROM c", enable_cross_partition_query=True))
        category_names = [category['name'] for category in categories]
        category_counts = [1 for _ in categories]  # Each category counts as 1

        plt.bar(category_names, category_counts, color='skyblue')
        plt.xlabel('Category')
        plt.ylabel('Number of Categories')
        plt.title('Category Distribution')

        buf = io.BytesIO()
        plt.savefig(buf, format='png')
        buf.seek(0)
        chart_image = CoreImage(buf, ext='png').texture

        popup = Popup(title="Categories Chart", content=Image(texture=chart_image), size_hint=(0.9, 0.7))
        popup.open()
        buf.close()

class ProductCategoriesApp(App):
    def build(self):
        return ProductCategoriesManager()

if __name__ == "__main__":
    ProductCategoriesApp().run()

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.spinner import Spinner
from kivy.uix.popup import Popup
from kivy.uix.screenmanager import ScreenManager, Screen
from db_config import feedback_container, customers_container, products_container
import random
from kivy.graphics import Color, Rectangle
import matplotlib.pyplot as plt
import io
from kivy.core.image import Image as CoreImage


class FeedbackManager(BoxLayout):
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
        header_label = Label(text="[b]Feedback Manager[/b]", font_size='28sp', markup=True)
        header_layout.add_widget(back_button)
        header_layout.add_widget(header_label)
        self.add_widget(header_layout)

        # Input Form Layout
        form_layout = GridLayout(cols=2, size_hint_y=None, spacing=15, padding=10)
        form_layout.bind(minimum_height=form_layout.setter('height'))

        # Input Fields
        customers = [customer['name'] for customer in customers_container.query_items(query="SELECT * FROM c", enable_cross_partition_query=True)]
        self.customer_spinner = Spinner(text="Select Customer", values=customers, size_hint_y=None, height=40)
        form_layout.add_widget(Label(text="Customer:", size_hint_y=None, height=40))
        form_layout.add_widget(self.customer_spinner)

        products = [product['name'] for product in products_container.query_items(query="SELECT * FROM c", enable_cross_partition_query=True)]
        self.product_spinner = Spinner(text="Select Product", values=products, size_hint_y=None, height=40)
        form_layout.add_widget(Label(text="Product:", size_hint_y=None, height=40))
        form_layout.add_widget(self.product_spinner)

        self.rating_input = TextInput(hint_text="Enter Rating (1-5)", size_hint_y=None, height=40)
        form_layout.add_widget(Label(text="Rating:", size_hint_y=None, height=40))
        form_layout.add_widget(self.rating_input)

        self.comments_input = TextInput(hint_text="Enter Comments", multiline=True, size_hint_y=None, height=80)
        form_layout.add_widget(Label(text="Comments:", size_hint_y=None, height=40))
        form_layout.add_widget(self.comments_input)

        self.add_widget(form_layout)

        # Buttons
        button_layout = BoxLayout(size_hint_y=None, height=50, spacing=10, padding=10)
        self.add_feedback_button = Button(text="Add Feedback", size_hint_x=0.3, background_color=(0.2, 0.6, 0.8, 1))
        self.add_feedback_button.bind(on_press=self.add_feedback)
        button_layout.add_widget(self.add_feedback_button)

        self.view_chart_button = Button(text="View Chart", size_hint_x=0.3, background_color=(0.2, 0.6, 0.8, 1))
        self.view_chart_button.bind(on_press=self.view_chart)
        button_layout.add_widget(self.view_chart_button)

        self.add_widget(button_layout)

        # Feedback List Header
        self.add_widget(Label(text="Feedback List", font_size='22sp', size_hint_y=None, height=40))

        # Scrollable Feedback List
        self.scroll_view = ScrollView(size_hint=(1, None), size_hint_y=1)
        self.feedback_list_layout = GridLayout(cols=1, size_hint_y=None, spacing=10, padding=10)
        self.feedback_list_layout.bind(minimum_height=self.feedback_list_layout.setter('height'))
        self.scroll_view.add_widget(self.feedback_list_layout)
        self.add_widget(self.scroll_view)

        # Load Feedback List
        self.load_feedback()

    def _update_rect(self, instance, value):
        self.rect.size = instance.size
        self.rect.pos = instance.pos

    def navigate_back(self, instance):
        app = App.get_running_app()
        app.root.current = 'main_screen'

    def add_feedback(self, instance):
        customer_name = self.customer_spinner.text
        product_name = self.product_spinner.text
        rating = self.rating_input.text
        comments = self.comments_input.text

        if not customer_name or not product_name or not rating or not comments:
            popup = Popup(title="Error", content=Label(text="All fields are required!"), size_hint=(0.8, 0.4))
            popup.open()
            return

        try:
            rating = int(rating)
            if rating < 1 or rating > 5:
                raise ValueError("Rating must be between 1 and 5.")
        except ValueError:
            popup = Popup(title="Error", content=Label(text="Invalid rating value!"), size_hint=(0.8, 0.4))
            popup.open()
            return

        customer_id = next((customer['id'] for customer in customers_container.query_items(query="SELECT * FROM c", enable_cross_partition_query=True) if customer['name'] == customer_name), None)
        product_id = next((product['id'] for product in products_container.query_items(query="SELECT * FROM c", enable_cross_partition_query=True) if product['name'] == product_name), None)

        feedback = {
            "id": f"feedback-{random.randint(1000, 9999)}",
            "customer_id": customer_id,
            "product_id": product_id,
            "rating": rating,
            "comments": comments
        }
        feedback_container.create_item(body=feedback)

        self.load_feedback()

        self.rating_input.text = ""
        self.comments_input.text = ""

    def load_feedback(self):
        self.feedback_list_layout.clear_widgets()
        customers = {customer['id']: customer['name'] for customer in customers_container.query_items(query="SELECT * FROM c", enable_cross_partition_query=True)}
        products = {product['id']: product['name'] for product in products_container.query_items(query="SELECT * FROM c", enable_cross_partition_query=True)}
        feedbacks = feedback_container.query_items(query="SELECT * FROM c", enable_cross_partition_query=True)
        for feedback in feedbacks:
            customer_name = customers.get(feedback['customer_id'], "Unknown Customer")
            product_name = products.get(feedback['product_id'], "Unknown Product")

            feedback_box = BoxLayout(orientation='horizontal', size_hint_y=None, height=40, spacing=10)

            feedback_label = Label(text=f"{customer_name} | {product_name} | Rating: {feedback['rating']} | Comments: {feedback['comments']}")
            feedback_box.add_widget(feedback_label)

            edit_button = Button(text="Edit", size_hint_x=0.2, on_press=lambda instance, fb=feedback: self.edit_feedback(fb))
            feedback_box.add_widget(edit_button)

            delete_button = Button(text="Delete", size_hint_x=0.2, on_press=lambda instance, fb=feedback: self.delete_feedback(fb))
            feedback_box.add_widget(delete_button)

            self.feedback_list_layout.add_widget(feedback_box)

    def edit_feedback(self, feedback):
        self.customer_spinner.text = next((customer['name'] for customer in customers_container.query_items(query="SELECT * FROM c", enable_cross_partition_query=True) if customer['id'] == feedback['customer_id']), "Select Customer")
        self.product_spinner.text = next((product['name'] for product in products_container.query_items(query="SELECT * FROM c", enable_cross_partition_query=True) if product['id'] == feedback['product_id']), "Select Product")
        self.rating_input.text = str(feedback['rating'])
        self.comments_input.text = feedback['comments']

        def save_changes(instance):
            feedback['rating'] = int(self.rating_input.text)
            feedback['comments'] = self.comments_input.text
            feedback['customer_id'] = next((customer['id'] for customer in customers_container.query_items(query="SELECT * FROM c", enable_cross_partition_query=True) if customer['name'] == self.customer_spinner.text), None)
            feedback['product_id'] = next((product['id'] for product in products_container.query_items(query="SELECT * FROM c", enable_cross_partition_query=True) if product['name'] == self.product_spinner.text), None)

            feedback_container.upsert_item(body=feedback)
            self.load_feedback()

        self.add_feedback_button.text = "Save Changes"
        self.add_feedback_button.unbind(on_press=self.add_feedback)
        self.add_feedback_button.bind(on_press=save_changes)

    def delete_feedback(self, feedback):
        feedback_container.delete_item(item=feedback['id'], partition_key=feedback['id'])
        self.load_feedback()

    def view_chart(self, instance):
        feedbacks = list(feedback_container.query_items(query="SELECT * FROM c", enable_cross_partition_query=True))
        ratings = [feedback['rating'] for feedback in feedbacks]

        if not ratings:
            popup = Popup(title="Info", content=Label(text="No feedback data available for visualization!"), size_hint=(0.8, 0.4))
            popup.open()
            return

        plt.hist(ratings, bins=5, range=(1, 5), color='skyblue', edgecolor='black')
        plt.title('Feedback Ratings Distribution')
        plt.xlabel('Rating')
        plt.ylabel('Frequency')

        buf = io.BytesIO()
        plt.savefig(buf, format='png')
        buf.seek(0)
        chart_image = CoreImage(buf, ext='png').texture

        popup = Popup(title="Feedback Chart", content=Image(texture=chart_image), size_hint=(0.9, 0.7))
        popup.open()
        buf.close()

class FeedbackManagerApp(App):
    def build(self):
        return FeedbackManager()

if __name__ == "__main__":
    FeedbackManagerApp().run()

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
import matplotlib.pyplot as plt
import io
from kivy.core.image import Image as CoreImage
from db_config import engagement_metrics_container, customers_container

class EngagementMetricsManager(BoxLayout):
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
        header_image = Image(source='engagement_icon.png', size_hint=(None, None), size=(60, 60))
        header_label = Label(text="[b]Engagement Metrics Manager[/b]", font_size='28sp', markup=True)
        header_layout.add_widget(back_button)
        header_layout.add_widget(header_image)
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

        self.interaction_count_input = TextInput(hint_text="Enter Interaction Count", size_hint_y=None, height=40)
        form_layout.add_widget(Label(text="Interaction Count:", size_hint_y=None, height=40))
        form_layout.add_widget(self.interaction_count_input)

        self.last_interaction_input = TextInput(hint_text="Enter Last Interaction Date", size_hint_y=None, height=40)
        form_layout.add_widget(Label(text="Last Interaction:", size_hint_y=None, height=40))
        form_layout.add_widget(self.last_interaction_input)

        self.add_widget(form_layout)

        # Buttons
        button_layout = BoxLayout(size_hint_y=None, height=50, spacing=10, padding=10)
        self.add_metric_button = Button(text="Add Metric", size_hint_x=0.5, background_color=(0.2, 0.6, 0.8, 1))
        self.add_metric_button.bind(on_press=self.add_metric)
        button_layout.add_widget(self.add_metric_button)

        self.view_chart_button = Button(text="View Engagement Chart", size_hint_x=0.5, background_color=(0.2, 0.6, 0.8, 1))
        self.view_chart_button.bind(on_press=self.show_chart)
        button_layout.add_widget(self.view_chart_button)

        self.add_widget(button_layout)

        # Engagement Metrics List Header
        self.add_widget(Label(text="Engagement Metrics List", font_size='22sp', size_hint_y=None, height=40))

        # Scrollable Metrics List
        self.scroll_view = ScrollView(size_hint=(1, None), size_hint_y=1)
        self.metrics_list_layout = GridLayout(cols=1, size_hint_y=None, spacing=10, padding=10)
        self.metrics_list_layout.bind(minimum_height=self.metrics_list_layout.setter('height'))
        self.scroll_view.add_widget(self.metrics_list_layout)
        self.add_widget(self.scroll_view)

        # Load Engagement Metrics List
        self.load_metrics()

    def _update_rect(self, instance, value):
        self.rect.size = instance.size
        self.rect.pos = instance.pos

    def navigate_back(self, instance):
        app = App.get_running_app()
        app.root.current = 'main_screen'

    def add_metric(self, instance):
        customer_name = self.customer_spinner.text
        interaction_count = self.interaction_count_input.text
        last_interaction = self.last_interaction_input.text

        if not customer_name or not interaction_count or not last_interaction:
            popup = Popup(title="Error", content=Label(text="All fields are required!"), size_hint=(0.8, 0.4))
            popup.open()
            return

        customer_id = next((customer['id'] for customer in customers_container.query_items(query="SELECT * FROM c", enable_cross_partition_query=True) if customer['name'] == customer_name), None)

        if not customer_id:
            popup = Popup(title="Error", content=Label(text="Invalid customer selected!"), size_hint=(0.8, 0.4))
            popup.open()
            return

        metric = {
            "id": f"metric-{random.randint(1000, 9999)}",
            "customer_id": customer_id,
            "interaction_count": int(interaction_count),
            "last_interaction": last_interaction
        }
        engagement_metrics_container.create_item(body=metric)

        self.load_metrics()

        self.customer_spinner.text = "Select Customer"
        self.interaction_count_input.text = ""
        self.last_interaction_input.text = ""

    def load_metrics(self):
        self.metrics_list_layout.clear_widgets()
        customers = {customer['id']: customer['name'] for customer in customers_container.query_items(query="SELECT * FROM c", enable_cross_partition_query=True)}
        metrics = engagement_metrics_container.query_items(query="SELECT * FROM c", enable_cross_partition_query=True)
        for metric in metrics:
            customer_name = customers.get(metric['customer_id'], "Unknown Customer")
            metric_box = BoxLayout(orientation='horizontal', size_hint_y=None, height=40, spacing=10)

            metric_label = Label(text=f"{customer_name} | {metric['interaction_count']} Interactions | Last: {metric['last_interaction']}")
            metric_box.add_widget(metric_label)

            edit_button = Button(text="Edit", size_hint_x=0.2, on_press=lambda instance, m=metric: self.edit_metric(m))
            metric_box.add_widget(edit_button)

            delete_button = Button(text="Delete", size_hint_x=0.2, on_press=lambda instance, m=metric: self.delete_metric(m))
            metric_box.add_widget(delete_button)

            self.metrics_list_layout.add_widget(metric_box)

    def edit_metric(self, metric):
        customers = {customer['id']: customer['name'] for customer in customers_container.query_items(query="SELECT * FROM c", enable_cross_partition_query=True)}
        self.customer_spinner.text = customers.get(metric['customer_id'], "Select Customer")
        self.interaction_count_input.text = str(metric['interaction_count'])
        self.last_interaction_input.text = metric['last_interaction']

        def save_changes(instance):
            metric['interaction_count'] = int(self.interaction_count_input.text)
            metric['last_interaction'] = self.last_interaction_input.text
            metric['customer_id'] = next((customer['id'] for customer in customers_container.query_items(query="SELECT * FROM c", enable_cross_partition_query=True) if customer['name'] == self.customer_spinner.text), None)

            engagement_metrics_container.upsert_item(body=metric)
            self.load_metrics()

        self.add_metric_button.text = "Save Changes"
        self.add_metric_button.unbind(on_press=self.add_metric)
        self.add_metric_button.bind(on_press=save_changes)

    def delete_metric(self, metric):
        engagement_metrics_container.delete_item(item=metric['id'], partition_key=metric['id'])
        self.load_metrics()

    def show_chart(self, instance):
        metrics = list(engagement_metrics_container.query_items(query="SELECT * FROM c", enable_cross_partition_query=True))
        interaction_counts = [metric['interaction_count'] for metric in metrics]
        customer_names = [metric['customer_id'] for metric in metrics]

        plt.bar(customer_names, interaction_counts, color='skyblue')
        plt.xlabel('Customers')
        plt.ylabel('Interaction Count')
        plt.title('Customer Engagement Metrics')

        buf = io.BytesIO()
        plt.savefig(buf, format='png')
        buf.seek(0)
        chart_image = CoreImage(buf, ext='png').texture

        popup = Popup(title="Engagemment Metrics", content=Image(texture=chart_image), size_hint=(0.9, 0.7))
        popup.open()
        buf.close()

class EngagementMetricsManagerApp(App):
    def build(self):
        return EngagementMetricsManager()

if __name__ == "__main__":
    EngagementMetricsManagerApp().run()

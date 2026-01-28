from kivy.lang import Builder
from kivymd.app import MDApp
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.garden.matplotlib.backend_kivyagg import FigureCanvasKivyAgg
import matplotlib.pyplot as plt

# Backend imports
from core.loader import DataLoader
from core.config import AppConfig
from core.eda import EDAEngine
from core.insights import InsightEngine
from core.anomalies import AnomalyEngine

from kivymd.uix.menu import MDDropdownMenu
from kivymd.uix.filemanager import MDFileManager
from kivy.metrics import dp

KV = '''
<HomeScreen>:
    name: 'home'
    MDBoxLayout:
        orientation: 'vertical'
        spacing: 20
        padding: 30

        MDLabel:
            text: 'Auto Insight Data Explorer'
            halign: 'center'
            font_style: 'H3'

        MDTextField:
            id: csv_input
            hint_text: 'Path to CSV file'
            text: 'data/sample.csv'
            size_hint_x: 0.9
            pos_hint: {'center_x': 0.5}
            mode: "rectangle"

        MDRaisedButton:
            text: 'Select CSV'
            pos_hint: {'center_x': 0.5}
            on_release: app.file_manager_open()

        MDRaisedButton:
            text: 'Load CSV'
            pos_hint: {'center_x': 0.5}
            on_release: app.load_csv(csv_input.text)

        MDRaisedButton:
            text: 'Visualization'
            pos_hint: {'center_x': 0.5}
            on_release:
                app.root.current = 'visualization'
                app.update_visualization()


<EdaScreen>:
    name: 'eda'
    MDBoxLayout:
        orientation: 'vertical'
        padding: 20
        spacing: 15
        md_bg_color: 0.95, 0.95, 0.95, 1

        ScrollView:
            MDBoxLayout:
                orientation: 'vertical'
                padding: 15
                spacing: 15
                size_hint_y: None
                height: self.minimum_height
                canvas.before:
                    Color:
                        rgba: 1, 1, 1, 1
                    RoundedRectangle:
                        pos: self.pos
                        size: self.size
                        radius: [15]

                MDLabel:
                    id: eda_output
                    text: ''
                    size_hint_y: None
                    height: self.texture_size[1]
                    theme_text_color: 'Primary'

        MDRaisedButton:
            text: 'Next: Insights'
            pos_hint: {'center_x': 0.5}
            md_bg_color: app.theme_cls.primary_color
            on_release: app.root.current = 'insights'


<InsightsScreen>:
    name: 'insights'
    MDBoxLayout:
        orientation: 'vertical'
        padding: 20
        spacing: 15
        md_bg_color: 0.95, 0.95, 1, 1

        ScrollView:
            MDBoxLayout:
                orientation: 'vertical'
                padding: 15
                spacing: 15
                size_hint_y: None
                height: self.minimum_height
                canvas.before:
                    Color:
                        rgba: 1, 1, 0.95, 1
                    RoundedRectangle:
                        pos: self.pos
                        size: self.size
                        radius: [15]

                MDLabel:
                    id: insights_output
                    text: ''
                    size_hint_y: None
                    height: self.texture_size[1]
                    theme_text_color: 'Primary'

        MDRaisedButton:
            text: 'Next: Anomalies'
            pos_hint: {'center_x': 0.5}
            md_bg_color: app.theme_cls.accent_color
            on_release: app.root.current = 'anomalies'


<AnomaliesScreen>:
    name: 'anomalies'
    MDBoxLayout:
        orientation: 'vertical'
        padding: 20
        spacing: 15
        md_bg_color: 1, 0.95, 0.95, 1

        ScrollView:
            MDBoxLayout:
                orientation: 'vertical'
                padding: 15
                spacing: 15
                size_hint_y: None
                height: self.minimum_height
                canvas.before:
                    Color:
                        rgba: 1, 1, 1, 1
                    RoundedRectangle:
                        pos: self.pos
                        size: self.size
                        radius: [15]

                MDLabel:
                    id: anomalies_output
                    text: ''
                    size_hint_y: None
                    height: self.texture_size[1]
                    theme_text_color: 'Primary'

        MDRaisedButton:
            text: 'Back to Home'
            pos_hint: {'center_x': 0.5}
            md_bg_color: app.theme_cls.primary_color
            on_release: app.root.current = 'home'


<VisualizationScreen>:
    name: 'visualization'
    MDBoxLayout:
        orientation: 'vertical'
        spacing: 10
        padding: 10

        MDBoxLayout:
            size_hint_y: None
            height: "40dp"
            spacing: 10

            MDLabel:
                text: "Plot type:"
                size_hint_x: None
                width: "80dp"
                valign: "center"

            MDRaisedButton:
                id: plot_button
                text: "Histogram"
                on_release: app.menu.open()

        ScrollView:
            MDBoxLayout:
                id: plot_container
                orientation: 'vertical'
                size_hint_y: None
                height: self.minimum_height

        MDRaisedButton:
            text: 'Back to Home'
            pos_hint: {'center_x': 0.5}
            on_release: app.root.current = 'home'
'''


# ------------------------------
# Screens
# ------------------------------
class HomeScreen(Screen):
    pass

class EdaScreen(Screen):
    pass

class InsightsScreen(Screen):
    pass

class AnomaliesScreen(Screen):
    pass

class VisualizationScreen(Screen):
    pass


# ------------------------------
# Main App
# ------------------------------
class AutoInsightApp(MDApp):

    def build(self):
        self.sm = ScreenManager()
        Builder.load_string(KV)

        self.sm.add_widget(HomeScreen())
        self.sm.add_widget(EdaScreen())
        self.sm.add_widget(InsightsScreen())
        self.sm.add_widget(AnomaliesScreen())
        self.sm.add_widget(VisualizationScreen())

        self.sm.current = 'home'

        self.config = AppConfig()
        self.df = None

        # Dropdown menu for plots
        menu_items = [
            {"text": "Histogram", "on_release": lambda x="hist": self.set_plot_type(x)},
            {"text": "Line Plot", "on_release": lambda x="line": self.set_plot_type(x)},
            {"text": "Box Plot", "on_release": lambda x="box": self.set_plot_type(x)},
        ]
        self.menu = MDDropdownMenu(
            caller=None,
            items=menu_items,
            width_mult=4,
        )
        self.plot_type = 'hist'

        # File manager for CSV selection
        self.file_manager = MDFileManager(
            exit_manager=self.exit_manager,
            select_path=self.select_path,
        )

        return self.sm

    # -------------------------
    # File Manager
    # -------------------------
    def file_manager_open(self):
        self.file_manager.show('/')  # Start from root

    def select_path(self, path):
        self.sm.get_screen('home').ids.csv_input.text = path
        self.exit_manager()

    def exit_manager(self, *args):
        self.file_manager.close()

    # -------------------------
    # Load CSV
    # -------------------------
    def load_csv(self, path):
        try:
            self.df = DataLoader(self.config).load_csv(path)
            self.eda_engine = EDAEngine(self.df)
            self.insight_engine = InsightEngine(self.eda_engine)
            self.anomaly_engine = AnomalyEngine(self.df, self.config)

            self.update_eda()
            self.update_insights()
            self.update_anomalies()

            self.sm.current = 'eda'

        except Exception as e:
            print("ERROR:", e)

    # -------------------------
    # EDA
    # -------------------------
    def update_eda(self):
        summary = self.eda_engine.dataset_summary()

        text = (
            f"[b]Dataset Summary[/b]\n"
            f"Rows: {summary['rows']}\n"
            f"Columns: {summary['columns']}\n"
            f"Numeric: {summary['numeric_columns']}\n"
            f"Categorical: {summary['categorical_columns']}\n\n"
        )

        for col, p in self.eda_engine.profile_columns().items():
            text += f"[color=1a73e8][b]{col}[/b][/color] ({p.dtype})\n"
            if hasattr(p, 'mean'):
                text += f"  mean={p.mean:.2f}, std={p.std:.2f}\n"
            text += "\n"

        self.sm.get_screen('eda').ids.eda_output.text = text
        self.sm.get_screen('eda').ids.eda_output.markup = True

    # -------------------------
    # Insights
    # -------------------------
    def update_insights(self):
        insights = self.insight_engine.generate()

        text = "[b][color=388E3C]Insights:[/color][/b]\n\n"
        for i, ins in enumerate(insights, 1):
            text += f"[b]{i}. [{ins.severity}][/b] {ins.title}\n"
            text += f"{ins.description}\n\n"

        self.sm.get_screen('insights').ids.insights_output.text = text
        self.sm.get_screen('insights').ids.insights_output.markup = True

    # -------------------------
    # Anomalies
    # -------------------------
    def update_anomalies(self):
        anomalies = self.anomaly_engine.detect()

        if not anomalies:
            text = "[b][color=D32F2F]No anomalies detected.[/color][/b]"
        else:
            text = "[b][color=D32F2F]Anomalies:[/color][/b]\n\n"
            for a in anomalies:
                text += f"Row {a.index} | Score: {a.score}\n"

        self.sm.get_screen('anomalies').ids.anomalies_output.text = text
        self.sm.get_screen('anomalies').ids.anomalies_output.markup = True

    # -------------------------
    # Visualization (NO CHANGE)
    # -------------------------
    def update_visualization(self):
        if self.df is None:
            print("No data loaded.")
            return

        screen = self.sm.get_screen('visualization')
        container = screen.ids.plot_container
        container.clear_widgets()

        numeric_cols = self.df.select_dtypes(include='number').columns
        print(f"Plotting ({self.plot_type}):", numeric_cols)

        for col in numeric_cols:
            fig, ax = plt.subplots(figsize=(5, 3))

            if self.plot_type == 'hist':
                ax.hist(self.df[col], bins=10, color='skyblue', edgecolor='black')
                ax.set_title(f'Histogram of {col}')
                ax.set_ylabel('Frequency')
            elif self.plot_type == 'line':
                ax.plot(self.df[col], color='green')
                ax.set_title(f'Line Plot of {col}')
            elif self.plot_type == 'box':
                ax.boxplot(self.df[col])
                ax.set_title(f'Box Plot of {col}')

            ax.set_xlabel(col)
            fig.tight_layout()

            canvas = FigureCanvasKivyAgg(fig)
            canvas.size_hint_y = None
            canvas.height = 300
            container.add_widget(canvas)

        container.height = 300 * len(numeric_cols)

    # -------------------------
    # Dropdown menu callback
    # -------------------------
    def set_plot_type(self, plot_type):
        self.plot_type = plot_type
        self.sm.get_screen('visualization').ids.plot_button.text = plot_type.capitalize()
        self.menu.dismiss()
        self.update_visualization()

    # -------------------------
    # Set caller for menu after build
    # -------------------------
    def on_start(self):
        self.menu.caller = self.sm.get_screen('visualization').ids.plot_button


# ------------------------------
# Run app
# ------------------------------
if __name__ == '__main__':
    AutoInsightApp().run()

from kivy.metrics import dp
from kivymd.app import MDApp
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.list import ThreeLineIconListItem, TwoLineIconListItem, IconLeftWidget

from components.listComponent.Employees import Employees
from components.saveComponent.Save import Save

from files.backend import *

backend = DataBase()

class Body(MDBoxLayout):
    def __init__(self, *args):
        super(Body, self).__init__(*args)

class Main(MDApp):
    def build(self):
        self.theme_cls.theme_style = 'Dark'
        self.theme_cls.primary_palette = 'Blue'
        return Body()

    def on_start(self):
        self.save = Save()
        self.employees = Employees()
        self.root.ids.tabs.add_widget(self.save)
        self.root.ids.tabs.add_widget(self.employees)

    def on_tab_switch(
        self, instance_tabs, instance_tab, instance_tab_label, tab_text
    ):

        if tab_text == 'Employers':
            employees_list = backend.getEmployeesByNom('tous')
            for employee in employees_list:
                instance_tab.ids.listContainer.add_widget(
                    TwoLineIconListItem(
                        text=f'{employee[1]} {employee[2]} {employee[3]}',
                        secondary_text=f'Paiements : {employee[4]} F CFA -> Dettes : {employee[5]} F CFA -> Epargne : {employee[6]} F CFA',
                        theme_text_color='Custom',
                        text_color=self.theme_cls.primary_color,
                        font_style='H6',
                        secondary_theme_text_color='Primary'
                    )
                )

if __name__=='__main__':
    Main().run()
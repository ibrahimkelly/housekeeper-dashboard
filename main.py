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
            instance_tab.ids.listContainer.clear_widgets()
            for i in range(len(employees_list)):
                instance_tab.ids.listContainer.add_widget(
                    ThreeLineIconListItem(
                        text=f'{employees_list[i][1]} {employees_list[i][2]} {employees_list[i][3]}',
                        secondary_text=f'PAIEMENTS : [b][color=#ff0]{employees_list[i][4]} F CFA[/color][/b]',
                        tertiary_text=f'EPARGNE : [b][color=#ff0]{employees_list[i][6]} F CFA[/color][/b]',
                        theme_text_color='Primary',
                        font_style='H6',
                        secondary_theme_text_color='Primary',
                        tertiary_theme_text_color='Primary',
                        bg_color= (0, 0, 0) if i%2==0 else self.theme_cls.primary_color,
                        on_release=lambda x: print(employees_list[i][0])
                    )
                )

if __name__=='__main__':
    Main().run()
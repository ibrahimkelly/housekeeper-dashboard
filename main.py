from kivy.event import EventDispatcher
from kivy.properties import ObjectProperty
from kivymd.app import MDApp
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.list import ThreeLineIconListItem

from components.details.Details import Details
from components.listComponent.List import List
from components.saveComponent.Save import Save

from files.backend import *

class Body(MDBoxLayout):

    screenManager = ObjectProperty(None)
    details = ObjectProperty(None)

    def __init__(self, **kwargs):
        super(Body, self).__init__(**kwargs)

    def showEmployeesDetails(self, instence) -> None:
        prenom, surnom, nom = instence.text.split(' ')
        self.screenManager.transition.direction = 'left'
        self.screenManager.current = 'details'

        #clear the widget with it contains last user informations...
        self.details.clear_widgets()
        self.detailsCls = Details()
        self.detailsCls.setUser(prenom, surnom, nom)
        self.details.add_widget(self.detailsCls.details)

class Main(MDApp):
    def build(self):
        self.backend = DataBase()
        self.theme_cls.theme_style = 'Dark'
        self.theme_cls.primary_palette = 'Blue'
        self.body = Body()
        return self.body

    def backToHome(self):
        self.body.screenManager.transition.direction = 'right'
        self.body.screenManager.current = 'home'

    def on_start(self):
        self.save = Save()
        self.employees = List()
        self.root.ids.tabs.add_widget(self.save)
        self.root.ids.tabs.add_widget(self.employees)

    def on_tab_switch(
        self, instance_tabs, instance_tab, instance_tab_label, tab_text
    ):
        if tab_text == 'Employers':
            employees_list = self.backend.getEmployeesByNom('tous')
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
                        bg_color=(0, 0, 0) if i%2==0 else self.theme_cls.primary_color,
                        on_release=self.body.showEmployeesDetails
                    )
                )

if __name__=='__main__':
    Main().run()
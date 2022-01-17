from kivy.properties import ObjectProperty
from kivymd.uix.floatlayout import MDFloatLayout
from kivymd.uix.tab import MDTabsBase
from kivymd.uix.list import ThreeLineIconListItem

from files.backend import *

class Employees(MDFloatLayout, MDTabsBase):
    '''Class implementing content for a tab.'''
    listContainer = ObjectProperty(None)

    def __init__(self, *args):
        super(Employees, self).__init__(*args)
        self.title = 'Employers'
        self.backend = DataBase()

    def showEmployeesList(self, filtre: str):
        nom = filtre.capitalize()
        employees_list = self.backend.getEmployeesByNom(nom)
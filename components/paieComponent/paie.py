from kivymd.uix.floatlayout import MDFloatLayout
from kivymd.uix.tab import MDTabsBase

from files.backend import *

class Paie(MDFloatLayout, MDTabsBase):
    def __init__(self, prenom, surnom, nom):
        self.backend = DataBase()
        foundUser = self.backend.getEmployeesByFullName(prenom, surnom, nom)
        print(foundUser)
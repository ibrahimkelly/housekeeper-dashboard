from kivy.metrics import dp
from kivy.properties import ObjectProperty, NumericProperty
from kivy.uix.widget import WidgetException
from kivy.utils import get_color_from_hex
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.button import MDFillRoundFlatIconButton
from kivymd.uix.pickers import MDDatePicker

from files.backend import *

class Details(MDBoxLayout):

    montantPaiement = ObjectProperty(None)
    paiementYear = ObjectProperty(None)
    detailToolbar = ObjectProperty(None)
    year = ObjectProperty(None)
    addYearButton = ObjectProperty(None)
    paie_tab = ObjectProperty(None)

    MONTH = [
        "janvier", "fevrier", "mars", "avril",
        "mai", "juin", "juillet", "aout",
        "septembre", "octobre", "novembre", "decembre"
    ]

    def __init__(self, **kwargs):
        super(Details, self).__init__(**kwargs)
        self.user = list()
        self.id = None
        self.backend = DataBase()
        self.hide_button()

    def setUser(self, prenom: str, surnom: str, nom: str):
        self.user = self.backend.getEmployeesByFullName(prenom, surnom, nom)
        self.detailToolbar.title = f'{self.user[0][1]} {self.user[0][2]} {self.user[0][3]}'
        self.id = self.user[0][0]

    def on_save(self, instance, value, date_range):
        self.year.text = str(value.year)
        paie = self.backend.getYearPaiement(self.id, value.year)
        if (paie==[]):
            self.clear_paiement()
            self.showButton()
        else:
            self.paie_tab.remove_widget(self.addYearButton)
            for i in range(len(paie[0]) - 4):
                self.ids[self.MONTH[i]].text = str(paie[0][i + 3])

    def updateSomme(self, year: int) -> int:
        self.backend.updateTotal(self.id, year)
        self.backend.updateTotalPaiement(self.id)
        self.updateEpargne(self.id)
        total_paiement = self.getUpdateTotal(self.id, year)
        total_paiement = 0 if total_paiement is None else total_paiement
        self.ids["total_paiement"].text = f"[b]Total des paiements : [color=#ffff00]{total_paiement} F[/color][/b]"

    def updatePaiement(self, year: int, mois: str, salaire: int) -> None:
        self.backend.updatePaiement(self.id, year, mois, salaire)

    def addNewYear(self) -> None:
        check_year_existence = self.backend.checkAnneeExistence(self.id, self.year.text)
        if (check_year_existence):
            pass
        else:
            self.backend.insertPaiement(self.id, self.year.text)
            self.hide_button()
            paie = self.backend.getYearPaiement(self.id, self.year.text)
            for i in range(len(paie[0]) - 4):
                self.ids[self.MONTH[i]].text = str(paie[0][i + 3])

    def clear_paiement(self) -> None:
        """Clear all paiements input contents"""
        for textInput in Details.MONTH:
            self.ids[textInput].text = ""
        self.ids["total_paiement"].text = ""

    def hide_button(self) -> None:
        try:
            self.paie_tab.remove_widget(self.addYearButton)
        except WidgetException:
            pass

    def showButton(self):
        try:
            self.paie_tab.add_widget(self.addYearButton)
        except WidgetException:
            self.paie_tab.remove_widget(self.addYearButton)
            self.paie_tab.add_widget(self.addYearButton)

    def getUpdateTotal(self, id: int, annee: int):
        result = self.backend.getUpdateTotal(id, annee)
        return result

    def updateEpargne(self, id: int) -> None:
        self.backend.updateEpargne(id)

    def show_date_picker(self):
        date_dialog = MDDatePicker(
            min_year=2019,
            max_year=2038
        )
        date_dialog.bind(on_save=self.on_save, on_cancel=self.on_cancel)
        date_dialog.open()

    def on_cancel(self, instance, value):
        '''Events called when the "CANCEL" dialog box button is clicked.'''
        pass
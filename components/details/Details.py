import datetime

from kivy.clock import Clock
from kivy.properties import ObjectProperty
from kivy.uix.widget import WidgetException
from kivymd.app import MDApp
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.list import OneLineIconListItem
from kivymd.uix.pickers import MDDatePicker

from files.backend import *

class Details(MDBoxLayout, MDApp):

    montantPaiement = ObjectProperty(None)
    paiementYear = ObjectProperty(None)
    detailToolbar = ObjectProperty(None)
    year = ObjectProperty(None)
    addYearButton = ObjectProperty(None)
    paie_tab = ObjectProperty(None)
    detteMontant = ObjectProperty(None)
    listDette = ObjectProperty(None)

    MONTH = [
        "janvier", "fevrier", "mars", "avril",
        "mai", "juin", "juillet", "aout",
        "septembre", "octobre", "novembre", "decembre"
    ]

    def __init__(self, **kwargs):
        super(Details, self).__init__(**kwargs)
        self.theme_cls.theme_style = 'Dark'
        self.theme_cls.primary_palette = 'Blue'
        self.user = list()
        self.id = None
        self.backend = DataBase()
        self.hide_button()

    def setUser(self, prenom: str, surnom: str, nom: str):
        self.user = self.backend.getEmployeesByFullName(prenom, surnom, nom)
        self.detailToolbar.title = f'{self.user[0][1]} {self.user[0][2]} {self.user[0][3]}'
        self.id = self.user[0][0]
        self.get_user_details()

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
        self.updateEpargne()
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

    def updateEpargne(self) -> None:
        self.backend.updateEpargne(self.id)

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

#==================================Dette=============================================

    def setDette(self, montant: int):

        if (int(montant) < 1000 or int(montant) >= 1000000):
            self.ids["detteInfos"].text = "[color=#ffff00]Montant n'est pas dans la fourchette...[/color]"
            Clock.schedule_once(self.hideDetteInfos, 3)
        elif (montant.isnumeric()==False):
            self.ids["detteInfos"].text = "[color=#ffff00]Montant invalide...[/color]"
            Clock.schedule_once(self.hideDetteInfos, 3)
        else:
            date = datetime.datetime.now()
            date = date.strftime("%d-%m-%Y")
            self.backend.insertDette(self.id, date, montant)
            self.updateEpargne()
            self.updateSommeDette()
            self.clearDette()
            self.getEmployeesDetteList()
            self.ids["detteInfos"].text = "[color=#00ff00]Dette accorder avec succès...[/color]"
            Clock.schedule_once(self.hideDetteInfos, 3)

    def getEmployeesDetteList(self) -> None:
        """MDList for credits on allowed to an employee"""
        self.listDette.clear_widgets()
        dettes = self.backend.getEmployeesDetteList(self.id)
        for i in range(len(dettes)):
            self.listDette.add_widget(
                OneLineIconListItem(
                    text=f'[b]{dettes[i][2]} [color=#ff0]{dettes[i][3]} F CFA[/color][/b]',
                    bg_color=(0, 0, 0) if i%2==0 else self.theme_cls.primary_color
                )
            )

    def updateSommeDette(self):
        """Make the somme of credits allowed to employee"""
        self.backend.updateTotalDette(self.id)

    def getSommeDette(self) -> int:
        """Get somme of credits allowed to employee"""
        result = self.backend.getTotalDette(self.id)
        return result

    def hideDetteInfos(self, instence):
        self.ids["detteInfos"].text = ''

    def clearDette(self):
        self.detteMontant.text = ''

# ================================Update================================

    def get_user_details(self):

        self.ids["updatePrenom"].text = str(self.user[0][1])
        self.ids["updateSurnom"].text = str(self.user[0][2])
        self.ids["updateNom"].text = str(self.user[0][3])

        self.ids["updateDateEntrer"].text = str(self.user[0][4])
        self.ids["updateSalaire"].text = str(self.user[0][6])
        self.ids["updateDateDebut"].text = str(self.user[0][5])

        self.ids["updatePrenomTuteur"].text = str(self.user[0][10])
        self.ids["updateNomTutuer"].text = str(self.user[0][11])
        self.ids["updateTuteurContact"].text = str(self.user[0][12])
        self.ids["updateAdressTuteur"].text = str(self.user[0][13])

        self.ids["updateInfos"].text = ""

    def hideUpdateInfos(self, instence):
        self.ids["updateInfos"].text = ""

    def setEnterDate(self, instance, value, date_range):
        self.ids.updateDateEntrer.text = str(value)

    def setStartDate(self, instance, value, date_range):
        self.ids.updateDateDebut.text = str(value)

    def on_cancel(self, instance, value):
        '''Events called when the "CANCEL" dialog box button is clicked.'''

    def shooseEnterDate(self):
        date_dialog = MDDatePicker()  # max_date=datetime.datetime.now(); primary_color=app.theme_cls.primary_color
        date_dialog.bind(on_save=self.setEnterDate, on_cancel=self.on_cancel)
        date_dialog.open()

    def shooseStartDate(self):
        date_dialog = MDDatePicker()  # max_date=datetime.datetime.now(); primary_color=app.theme_cls.primary_color
        date_dialog.bind(on_save=self.setStartDate, on_cancel=self.on_cancel)
        date_dialog.open()

    def set_update(self):

        prenom, surnom, nom = (
            self.ids["updatePrenom"].text,
            self.ids["updateSurnom"].text,
            self.ids["updateNom"].text
        )
        date_in, date_start, salaire = (
            self.ids["updateDateEntrer"].text,
            self.ids["updateDateDebut"].text,
            self.ids["updateSalaire"].text
        )
        t_prenom, t_nom, t_contact, t_adress = (
            self.ids["updatePrenomTuteur"].text,
            self.ids["updateNomTutuer"].text,
            self.ids["updateTuteurContact"].text,
            self.ids["updateAdressTuteur"].text
        )
        self.backend.updateEmployee(
            self.id, prenom, surnom, nom,
            date_in, date_start, salaire,
            t_prenom, t_nom, t_contact, t_adress
        )
        Clock.schedule_once(self.updateSuccess, 0.8)

    def updateSuccess(self, event):
        self.ids["updateInfos"].text = "[color=#00ff00]Mise en jour effectuée...[/color]"
        Clock.schedule_once(self.hideUpdateInfos, 1.9)
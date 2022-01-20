from kivy.metrics import dp
from kivy.properties import ObjectProperty
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.button import MDFillRoundFlatIconButton

from files.backend import *

class Details(MDBoxLayout):

    montantPaiement = ObjectProperty(None)
    paiementYear = ObjectProperty(None)
    detailToolbar = ObjectProperty(None)

    MONTH = [
        "janvier", "fevrier", "mars", "avril",
        "mai", "juin", "juillet", "aout",
        "septembre", "octobre", "novembre", "decembre"
    ]

    def __init__(self, user, **kwargs):
        super(Details, self).__init__(user, **kwargs)

        print('args : ', user, 'kwargs : ', kwargs)
        self.backend = DataBase()

    def getUserInfosForPaiement(self):
        self.id = self.foundUser[0]
        print(self.id)
        if (len(str(self.paiementYear.text)) == 4):
            self.table = self.backend.getYearPaiement(self.id, self.paiementYear.text)
            if (self.table == []):
                self.clearPaiement()
                self.addYearButton = MDFillRoundFlatIconButton(
                    icon='plus',
                    text='Ajouter',
                    font_size=dp(24),
                    on_press=lambda x: self.addNewYear(id)
                )
                self.detailToolbar.add_widget(self.addYearButton)
            else:
                for i in range(len(self.table[0]) - 4):  # Code slow for about 2.20 seconds
                    self.ids[self.MONTH[i]].text = str(self.table[0][i + 3])
        else:
            self.hideButton()
            for i in range(len(self.MONTH)):
                self.ids[self.MONTH[i]].text = ""

    def updatePaiement(self, year: int, mois: str, salaire: int) -> None:
        self.backend.updatePaiement(self.id, year, mois, salaire)

    def hideButton(self):
        self.detailToolbar.remove_widget(self.addYearButton)

    def addNewYear(self):
        check_year_existence = self.backend.checkAnneeExistence(self.id, self.paiementYear.text)
        if (check_year_existence):
            pass
        else:
            self.backend.insertPaiement(self.id, self.paiementYear.text)
            self.hideButton()

    def updateSomme(self):
        self.backend.updateTotal(self.id, self.paiementYear.text)
        self.backend.updateTotalPaiement(self.id)
        self.backend.updateEpargne(self.id)
        total_paiement = self.getUpdateTotal(self.id, self.paiementYear.text)
        total_paiement = 0 if total_paiement is None else total_paiement
        self.ids["total_paiement"].text = f"[b]Total des paiements : [color=#ffff00]{total_paiement} F[/color][/b]"

        if (len(str(self.paiementYear.text)) != 4):
            self.ids["total_paiement"].text = ""

    def clearPaiement(self):
        for textInput in Details.MONTH:
            self.ids[textInput].text = ""
        self.ids["total_paiement"].text = ""

    def getUpdateTotal(self, annee: int):
        result = self.backend.getUpdateTotal(self.id, annee)

    def updateEpargne(self) -> None:
        self.backend.updateEpargne(self.id)
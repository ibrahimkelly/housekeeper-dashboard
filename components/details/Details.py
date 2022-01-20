from kivy.metrics import dp
from kivy.properties import ObjectProperty
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.button import MDFillRoundFlatIconButton

from files.backend import *

class Details(MDBoxLayout):

    montantPaiement = ObjectProperty(None)
    paiementYear = ObjectProperty(None)
    pToolbar = ObjectProperty(None)

    MONTH = [
        "janvier", "fevrier", "mars", "avril",
        "mai", "juin", "juillet", "aout",
        "septembre", "octobre", "novembre", "decembre"
    ]

    def __init__(self, **kwargs):
        super(Details, self).__init__(**kwargs)

        self.backend = DataBase()

    def setUser(self, user):
        prenom, surnom, nom = user
        self.foundUser = self.backend.getEmployeesByFullName(prenom, surnom, nom)

    def getUser(self):
        return self.foundUser

    def getUserInfosForPaiement(self, id: int):

        try:  # if id not found in the database, the foundUser = backend.getEmployeeById(id)[0] will raise an IndexError
            if (id == "" or id.isnumeric() == False):
                self.ids["pUserName"].text = ""
                self.ids.idForPaiement.text = ''
                self.hideButton()
                self.clearPaiement()
            else:
                foundUser = self.backend.getEmployeeById(id)[0]
                if (foundUser != []):
                    self.ids["pUserName"].text = f"[b]{foundUser[1]} {foundUser[2]} {foundUser[3]}[/b]"
                    if (len(str(self.paiementYear.text)) == 4):
                        id = self.ids["idForPaiement"].text
                        self.table = self.backend.getYearPaiement(id, self.paiementYear.text)
                        if (self.table == []):
                            self.clearPaiement()
                            self.addYearButton = MDFillRoundFlatIconButton(
                                icon='plus',
                                text='Ajouter',
                                font_size=dp(24),
                                on_press=lambda x: self.addNewYear(id)
                            )
                            self.pToolbar.add_widget(self.addYearButton)
                        else:
                            for i in range(len(self.table[0]) - 4):  # Code slow for about 2.20 seconds
                                self.ids[self.MONTH[i]].text = str(self.table[0][i + 3])
                    else:
                        self.hideButton()
                        for i in range(len(self.MONTH)):
                            self.ids[self.MONTH[i]].text = ""
                else:
                    self.hideButton()
        except(IndexError):
            self.ids["pUserName"].text = f"[color=#ff0][b]Aucun employé (e) trouvée avec l'id : {id}[/b][/color]"

    def updatePaiement(self, id: int, year: int, mois: str, salaire: int) -> None:
        self.backend.updatePaiement(id, year, mois, salaire)

    def hideButton(self):
        self.pToolbar.remove_widget(self.addYearButton)

    def addNewYear(self, id: int):
        check_year_existence = self.backend.checkAnneeExistence(id, self.paiementYear.text)
        if (check_year_existence):
            pass
        else:
            self.backend.insertPaiement(id, self.paiementYear.text)
            self.hideButton()

    def updateSomme(self, id: int):
        if (id == "" or id.isnumeric() == False):
            pass
        else:
            self.backend.updateTotal(id, self.paiementYear.text)
            self.backend.updateTotalPaiement(id)
            self.backend.updateEpargne(id)
            total_paiement = self.getUpdateTotal(id, self.paiementYear.text)
            total_paiement = 0 if total_paiement is None else total_paiement
            self.ids["total_paiement"].text = f"[b]Total des paiements : [color=#ffff00]{total_paiement} F[/color][/b]"

            if (len(str(self.paiementYear.text)) != 4):
                self.ids["total_paiement"].text = ""

    def clearPaiement(self):
        for textInput in Details.MONTH:
            self.ids[textInput].text = ""
        self.ids["total_paiement"].text = ""

    def getUpdateTotal(self, id, annee: int):
        result = str()
        if (id == "" or annee.isnumeric() == False):
            pass
        else:
            result = self.backend.getUpdateTotal(id, annee)
        return result

    def updateEpargne(self, id: int) -> None:
        self.backend.updateEpargne(id)
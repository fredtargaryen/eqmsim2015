from PyQt4.QtGui import QDialog, QGroupBox, QFormLayout, QLineEdit, QLabel, QRadioButton, \
    QGridLayout, QVBoxLayout, QPushButton, QCheckBox, QMessageBox
import re
from chem.Reaction import Reaction

class ConditionsDialog(QDialog):
    def __init__(self, reaction):
        super(ConditionsDialog, self).__init__()
        self.setGeometry(300, 200, 700, 350)
        self.setWindowTitle('Edit Conditions')
        if reaction is None:
            self._reaction = Reaction()
        else:
            self._reaction = reaction
        self._CanReturnReaction = False

        # Sets up GUI widgets

        # Reactants section
        self._reactantbox = QGroupBox("Reactants", self)
        self._reactantform = QFormLayout()
        self._reactantinfoboxes = []
        self._productinfoboxes = []
        self._catalystinfoboxes = []
        self._checkbuttons = []
        for x in range(Reaction.REACTING_SPECIES_LIMIT):
            self._reactantinfoboxes.append(QLineEdit())
            self._reactantinfoboxes[x*2].setText(self._reaction.GetReactants()[x].GetFormula())
            self._reactantinfoboxes.append(QLineEdit())
            self._reactantinfoboxes[x*2+1].setText(str(self._reaction.GetReactants()[x].GetInitialMoles()))
            self._reactantform.addRow(QLabel(str(x + 1)+".\tFormula:"), self._reactantinfoboxes[x*2])
            self._reactantform.addRow(QLabel("\tFinal Moles:"), self._reactantinfoboxes[x*2+1])
            self._checkbuttons.append(QCheckBox("Use this reactant", self))
            self._checkbuttons[-1].setChecked(self._reaction.GetReactants()[x].GetUsed())
            self._reactantform.addRow(self._checkbuttons[-1])
        self._reactantbox.setLayout(self._reactantform)

        # Products section
        self._productbox = QGroupBox("Products", self)
        self._productform = QFormLayout()
        for x in range(Reaction.REACTING_SPECIES_LIMIT):
            self._productinfoboxes.append(QLineEdit())
            self._productinfoboxes[x*2].setText(self._reaction.GetProducts()[x].GetFormula())
            self._productinfoboxes.append(QLineEdit())
            self._productinfoboxes[x*2+1].setText(str(self._reaction.GetProducts()[x].GetInitialMoles()))
            self._productform.addRow(QLabel(str(x + 1)+".\tFormula:"), self._productinfoboxes[x*2])
            self._productform.addRow(QLabel("\tFinal Moles:"), self._productinfoboxes[x*2+1])
            self._checkbuttons.append(QCheckBox("Use this product", self))
            self._checkbuttons[-1].setChecked(self._reaction.GetProducts()[x].GetUsed())
            self._productform.addRow(self._checkbuttons[-1])
        self._productbox.setLayout(self._productform)

        # Catalyst section
        self._catalystbox = QGroupBox("Catalyst", self)
        self._catalystform = QFormLayout()
        self._catalystinfoboxes.append(QLineEdit())
        self._catalystinfoboxes.append(QLineEdit())
        self._catalystinfoboxes[0].setText(self._reaction.GetCatalyst().GetFormula())
        self._catalystinfoboxes[1].setText(str(self._reaction.GetCatalyst().GetInitialMoles()))
        self._catalystform.addRow(QLabel("Formula:"), self._catalystinfoboxes[0])
        self._catalystform.addRow(QLabel("Moles:"), self._catalystinfoboxes[1])
        self._good = QRadioButton("Good")
        self._poor = QRadioButton("Poor")
        self._inhibitor = QRadioButton("Inhibitor")
        self._checkbuttons.append(QCheckBox("Use this catalyst", self))
        self._checkbuttons[-1].setChecked(self._reaction.GetCatalyst().GetUsed())
        efficacy = self._reaction.GetCatalyst().GetEfficacy()
        if efficacy == 5:
            self._good.setChecked(True)
        elif efficacy == 2:
            self._poor.setChecked(True)
        else:
            self._inhibitor.setChecked(True)
        self._cataefficacygroup = QVBoxLayout()
        self._cataefficacygroup.addWidget(self._good)
        self._cataefficacygroup.addWidget(self._poor)
        self._cataefficacygroup.addWidget(self._inhibitor)
        self._catalystform.addRow(QLabel("Efficacy:"), self._cataefficacygroup)
        self._catalystform.addRow(self._checkbuttons[-1])
        self._catalystbox.setLayout(self._catalystform)

        # Forward heat transfer section
        self._heatbox = QGroupBox("Forward heat transfer", self)
        self._heatform = QFormLayout()
        self._endo = QRadioButton("Endothermic")
        self._exo = QRadioButton("Exothermic")
        if self._reaction.GetEndothermic():
            self._endo.setChecked(True)
        else:
            self._exo.setChecked(True)
        self._heatform.addRow(self._endo)
        self._heatform.addRow(self._exo)
        self._heatbox.setLayout(self._heatform)

        # Other conditions section: vessel volume; temperature
        self._otherbox = QGroupBox("Other conditions")
        self._otherform = QFormLayout()
        self._tempbox = QLineEdit()
        self._volbox = QLineEdit()
        self._tempbox.setText(str(self._reaction.GetTemperature()))
        self._volbox.setText(str(self._reaction.GetVolume()))
        self._otherform.addRow(QLabel("Vessel volume:"), self._volbox)
        self._otherform.addRow(QLabel("Temperature:"), self._tempbox)
        self._otherbox.setLayout(self._otherform)

        # Help text explaining how to enter super/subscript characters.
        self._scriptinfo1 = QLabel("Enter _ before a subscript character.")
        self._scriptinfo2 = QLabel("Enter ^ before a superscript one.")

        # OK and cancel buttons; checkbox so that students can try to balance the equation before it is revealed
        self._try = QCheckBox("Students attempt to balance equation")
        self._try.setChecked(False)
        self._okbtn = QPushButton("OK")
        self._okbtn.clicked.connect(self.ApplyChanges)
        self._cancelbtn = QPushButton("Cancel")

        self._rightbox = QGroupBox()
        self._rightbox.setFlat(False)
        self._rightform = QVBoxLayout()
        self._rightform.addWidget(self._catalystbox)
        self._rightform.addWidget(self._heatbox)
        self._rightform.addWidget(self._otherbox)
        self._rightbox.setLayout(self._rightform)

        # Layout of all those group boxes
        self._grid = QGridLayout()
        self._grid.addWidget(self._scriptinfo1, 0, 0)
        self._grid.addWidget(self._scriptinfo2, 1, 0)
        self._grid.addWidget(self._reactantbox, 2, 0)
        self._grid.addWidget(self._productbox, 2, 1)
        self._grid.addWidget(self._rightbox, 2, 2)
        self._grid.addWidget(self._try, 3, 0)
        self._grid.addWidget(self._okbtn, 3, 1)
        self._grid.addWidget(self._cancelbtn, 3, 2)
        self.setLayout(self._grid)

        if reaction is None:
            self._reaction = Reaction()
        else:
            self._reaction = reaction

        self._cancelbtn.clicked.connect(self.close)
        self.exec_()

    def ApplyChanges(self):
        errorlist = []
        # Validation. If invalid data has been entered, a message describing where the problem is
        # and explaining what constitutes valid data is added to errorlist.
        formularegex = "[2-9]?(\(([A-Z][a-z]?(_[0-9])*)+\)(_[0-9])*|[A-Z][a-z]?(_[0-9])*)+((\^[0-9])*\^(\+|-))?"
        molesorvolumeregex = "[0-9]?[0-9]\.[0-9][0-9]?"

        # VALIDATES REACTANT AND PRODUCT DATA (if used)
        for x in range(Reaction.REACTING_SPECIES_LIMIT):
            if self._checkbuttons[x].isChecked():
                formula = self._reactantinfoboxes[x*2].text()
                moles = self._reactantinfoboxes[x*2 + 1].text()
                if len(formula) not in range(1, 26):
                    errorlist.append("The formula of reactant "+str(x + 1)+" must be 1-25 characters long inclusive.")
                else:
                    try:
                        if formula != re.match(formularegex, formula).group():
                            errorlist.append("The formula you have entered for reactant "+str(x + 1)+" is invalid.")
                    except:
                        errorlist.append("The formula you have entered for reactant "+str(x + 1)+" is invalid.")
                try:
                    if float(moles) < 0.01 or float(moles) > 99.99:
                        errorlist.append("The number of moles of reactant "+str(x + 1)+" must be between 0.01 and 99.99 inclusive.")
                    else:
                        try:
                            if moles != re.match(molesorvolumeregex, moles).group():
                                errorlist.append("The number of moles must be between 0.01 and 99.99 inclusive, and must have a maximum of 2 decimal places.")
                        except:
                            errorlist.append("The number of moles must be between 0.01 and 99.99 inclusive, and must have a maximum of 2 decimal places.")
                except:
                    errorlist.append("Number of moles of reactant "+str(x + 1)+" must be a decimal number.")
            if self._checkbuttons[x + Reaction.REACTING_SPECIES_LIMIT].isChecked():
                formula = self._productinfoboxes[x*2].text()
                moles = self._productinfoboxes[x*2 + 1].text()
                if len(formula) not in range(1, 26):
                    errorlist.append("The formula of product "+str(x + 1)+" must be 1-25 characters long inclusive.")
                else:
                    try:
                        if formula != re.match(formularegex, formula).group():
                            errorlist.append("The formula you have entered for product "+str(x + 1)+" is invalid.")
                    except:
                        errorlist.append("The formula you have entered for product "+str(x + 1)+" is invalid.")
                try:
                    if float(moles) < 0.01 or float(moles) > 99.99:
                        errorlist.append("The number of moles of product "+str(x + 1)+" must be between 0.01 and 99.99 inclusive.")
                    else:
                        try:
                            if moles != re.match(molesorvolumeregex, moles).group():
                                errorlist.append("The number of moles must be between 0.01 and 99.99 inclusive, and must have a maximum of 2 decimal places.")
                        except:
                            errorlist.append("The number of moles must be between 0.01 and 99.99 inclusive, and must have a maximum of 2 decimal places.")
                except:
                    errorlist.append("Number of moles of product "+str(x + 1)+" must be a decimal number.")

        # VALIDATES CATALYST DATA (if used)
        if self._checkbuttons[2 * Reaction.REACTING_SPECIES_LIMIT].isChecked():
            formula = self._catalystinfoboxes[0].text()
            moles = self._catalystinfoboxes[1].text()
            if len(formula) not in range(1, 26):
                errorlist.append("The formula of the catalyst must be 1-25 characters long inclusive.")
            else:
                try:
                    if formula != re.match(formularegex, formula).group():
                        errorlist.append("The formula you have entered for the catalyst is invalid.")
                except:
                    errorlist.append("The formula you have entered for the catalyst is invalid.")
            try:
                if float(moles) < 0.01 or float(moles) > 99.99:
                    errorlist.append("The number of moles of the catalyst must be between 0.01 and 99.99 inclusive.")
                else:
                    try:
                        if moles != re.match(molesorvolumeregex, moles).group():
                            errorlist.append("The number of moles must be between 0.01 and 99.99 inclusive, and must have a maximum of 2 decimal places.")
                    except:
                        errorlist.append("The number of moles must be between 0.01 and 99.99 inclusive, and must have a maximum of 2 decimal places.")
            except:
                errorlist.append("Number of moles of catalyst must be a decimal number.")

        # VALIDATES TEMPERATURE DATA
        try:
            if int(self._tempbox.text()) not in range(1, 1000):
                errorlist.append("Temperature must be between 1 and 999 inclusive.")
        except:
            errorlist.append("Temperature must be a whole number.")

        # VALIDATES VOLUME DATA
        try:
            volume = self._volbox.text()
            if float(volume) < 0.01 or float(volume) > 99.99:
                errorlist.append("Volume must be between 0.01 and 99.99 inclusive.")
            else:
                try:
                    if volume != re.match(molesorvolumeregex, volume).group():
                        errorlist.append("Volume must be between 0.01 and 99.99 inclusive, and must have a maximum of 2 decimal places.")
                except:
                    errorlist.append("Volume must be between 0.01 and 99.99 inclusive, and must have a maximum of 2 decimal places.")
        except:
            errorlist.append("Volume must be a decimal number.")

        # If all data is valid, it applies this data to the reaction.
        if len(errorlist) == 0:
            for x in range(Reaction.REACTING_SPECIES_LIMIT):
                self._reaction.GetReactants()[x].SetFormula(self._reactantinfoboxes[x*2].text())
                self._reaction.GetReactants()[x].SetInitialMoles(float(str(self._reactantinfoboxes[x*2+1].text())))
                self._reaction.GetReactants()[x].SetUsed(self._checkbuttons[x].isChecked())
                self._reaction.GetProducts()[x].SetFormula(self._productinfoboxes[x*2].text())
                self._reaction.GetProducts()[x].SetInitialMoles(float(str(self._productinfoboxes[x*2+1].text())))
                self._reaction.GetProducts()[x].SetUsed(self._checkbuttons[x + Reaction.REACTING_SPECIES_LIMIT].isChecked())
            self._reaction.GetCatalyst().SetFormula(self._catalystinfoboxes[0].text())
            self._reaction.GetCatalyst().SetInitialMoles(float(str(self._catalystinfoboxes[1].text())))
            self._reaction.GetCatalyst().SetUsed(self._checkbuttons[2 * Reaction.REACTING_SPECIES_LIMIT].isChecked())

            if self._good.isChecked():
                self._reaction.GetCatalyst().SetEfficacy(5)
            elif self._poor.isChecked():
                self._reaction.GetCatalyst().SetEfficacy(2)
            elif self._inhibitor.isChecked():
                self._reaction.GetCatalyst().SetEfficacy(0.75)

            if self._endo.isChecked():
                self._reaction.SetEndothermic(True)
            elif self._exo.isChecked():
                self._reaction.SetEndothermic(False)
            self._reaction.SetTemperature(int(self._tempbox.text()))
            self._reaction.SetVolume(float(self._volbox.text()))
            self._CanReturnReaction = True
            self._showformulae = not self._try.isChecked()
            self.close()
        else:
            # Sets up the error list to be displayed (if not empty) and displays
            self._errorbox = QMessageBox()
            self._errorbox.setWindowTitle("Invalid Data")
            texttoadd = """"""
            for x in errorlist:
                texttoadd += x + "\n"
            self._errorbox.setText("Some of the data you entered is invalid:\n"+texttoadd)
            self._errorbox.setStandardButtons(QMessageBox.Ok)
            self._errorbox.setDefaultButton(QMessageBox.Ok)
            self._CanReturnReaction = False
            self._showformulae = True
            self._errorbox.exec_()

    # To avoid errors, make sure to check in case of a NoneType object being returned
    # None is returned when the window is unable to return the reaction; for example,
    # when some data is invalid
    def GetReaction(self):
        if self._CanReturnReaction:
            return self._reaction
        else:
            return None

    #GETTERS AND SETTERS
    def GetCanShowFormulae(self):
        return self._showformulae
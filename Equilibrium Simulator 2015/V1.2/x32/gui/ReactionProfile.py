import copy
from decimal import *
from PyQt4.QtCore import QRectF, Qt, QTimer
from PyQt4.QtGui import QWidget, QPainter, QPushButton, QPen, QPixmap, QFont, QColorDialog, QColor, QPlainTextEdit, \
    QLabel, QPalette, QCheckBox
from gui.GraphWindow import GraphWindow
from gui.GraphWindowGroup import GraphWindowGroup
from gui.Square import Square


class ReactionProfile(QWidget):
    def __init__(self, reaction, readonly):
        super(ReactionProfile, self).__init__()
        self._painter = QPainter()
        self._canshowreaction = True
        self._IsReadOnly = readonly
        # Show labels checkbox widget
        self._showlabels = QCheckBox("Show data", self)
        self._showlabels.setChecked(False)
        self._showlabels.setGeometry(0, 0, 80, 20)
        self._showlabels.clicked.connect(self.update)
        # The buttons
        if self._IsReadOnly:
            self._CurrentReaction = copy.deepcopy(reaction)
        else:
            self._CurrentReaction = reaction
            self._rcolbtn = QPushButton("Set reactant colour", self)
            self._rcolbtn.setGeometry(140, 60, 110, 30)
            self._rcolbtn.clicked.connect(self.SetReactantColour)
            self._pcolbtn = QPushButton("Set product colour", self)
            self._pcolbtn.setGeometry(350, 60, 110, 30)
            self._pcolbtn.clicked.connect(self.SetProductColour)
            self._clonebtn = QPushButton("Compare reaction", self)
            self._clonebtn.setGeometry(10, 310, 120, 30)
            self._clonebtn.clicked.connect(self.Clone)
            self._concbtn = QPushButton("Concentration graphs", self)
            self._concbtn.setGeometry(10, 100, 120, 30)
            self._concbtn.clicked.connect(self.MakeConcGraphs)
            self._ratebtn = QPushButton("Rate graphs", self)
            self._ratebtn.setGeometry(10, 130, 120, 30)
            self._ratebtn.clicked.connect(self.MakeRateGraphs)
        self._getkcbtn = QPushButton("Calculate Kc", self)
        self._getkcbtn.setGeometry(10, 180, 120, 30)
        self._getkcbtn.clicked.connect(self.GetKc)
        self._workingbtn = QPushButton("Show working", self)
        self._workingbtn.setGeometry(10, 225, 120, 30)
        self._workingbtn.clicked.connect(self.ShowWorking)
        self._startanim = QPushButton("Start animation", self)
        self._startanim.setGeometry(10, 260, 120, 30)
        self._startanim.clicked.connect(self.StartAnimation)
        # The labels
        self._catalabel = QLabel("", self)
        self._catalabel.setGeometry(250, 60, 100, 40)
        self._catalabel.setAlignment(Qt.AlignCenter)
        self._kclabel = QLabel(self)
        self._kclabel.setGeometry(20, 205, 140, 20)
        self._volumelabel = QLabel(self)
        self._volumelabel.setGeometry(200, 317, 140, 20)
        # Set up reactant and product labels
        formulafont = QFont()
        formulafont.setBold(True)
        formulafont.setPointSize(12)
        self._rpalette = QPalette()
        self._ppalette = QPalette()
        self._reactantlabel = QLabel("", self)
        self._reactantlabel.setGeometry(0, 20, 268, 32)
        self._reactantlabel.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        self._reactantlabel.setFont(formulafont)
        self._reactantlabel.setPalette(self._rpalette)
        self._reactantlabel.show()
        self._productlabel = QLabel("", self)
        self._productlabel.setGeometry(332, 20, 268, 32)
        self._productlabel.setAlignment(Qt.AlignVCenter)
        self._productlabel.setFont(formulafont)
        self._productlabel.setPalette(self._ppalette)
        self._productlabel.show()
        # Other properties
        self._Squares = []
        for x in range(100):
            self._Squares.append(Square(200+((x % 10) * 20), 120 + ((x // 10) * 20), self._CurrentReaction))
        self._timer = QTimer(self)
        self._timer.setInterval(30)
        self._timer.setSingleShot(False)
        self._timer.timeout.connect(self.ContinueAnimation)
        self._no_of_anim_updates = 0
        self._ExtraWindows = []
        self._kcdifference = ""
        self._rflipchance = 0
        self._pflipchance = 0
        self._graphs = None

    def paintEvent(self, e):
        reactantside = ""
        productside = ""
        for x in range(len(self._CurrentReaction.GetReactants())):
            reactant = self._CurrentReaction.GetReactants()[x]
            if reactant.GetUsed():
                if x > 0:
                    reactantside += " + "
                reactantside += reactant.GetFormulaForLabels()
        for x in range(len(self._CurrentReaction.GetProducts())):
            product = self._CurrentReaction.GetProducts()[x]
            if product.GetUsed():
                if x > 0:
                    productside += " + "
                productside += product.GetFormulaForLabels()
        self._rpalette.setColor(QPalette.WindowText, self._CurrentReaction.GetReactantColour())
        self._ppalette.setColor(QPalette.WindowText, self._CurrentReaction.GetProductColour())
        self._reactantlabel.setPalette(self._rpalette)
        self._productlabel.setPalette(self._ppalette)
        self._painter.begin(self)
        self._painter.setFont(QFont("Arial", 20, 50, False))
        self._painter.setPen(QPen(self._CurrentReaction.GetReactantColour()))
        if self._CurrentReaction.GetCatalyst().GetUsed():
            self._catalabel.setText("Catalyst: "+
                                    self._CurrentReaction.GetCatalyst().GetFormulaForLabels()+"<br>Moles: "+
                                    str(self._CurrentReaction.GetCatalyst().GetInitialMoles())+"<br>Strength: "+
                                    self._CurrentReaction.GetCatalyst().GetEfficacyAsString())
            self._catalabel.show()
        else:
            self._catalabel.hide()
        self._reactantlabel.setText(reactantside)
        self._productlabel.setText(productside)
        target = QRectF(278, 20, 44, 32)
        arrows = QPixmap("assets/double arrow h.png")
        portion = QRectF(10, 0, 44, 32)
        self._painter.drawPixmap(target, arrows, portion)
        self._painter.setPen(QPen(self._CurrentReaction.GetProductColour()))
        self._painter.setPen(QPen(QColor(0, 0, 0, 255)))
        self._painter.setFont(QFont("Arial", 8, 50, False))
        self._volumelabel.setText("Vessel volume: "+str(self._CurrentReaction.GetVolume())+" dm<sup>3</sup>")
        self._painter.drawText(200, 340, "Vessel temperature: "+str(self._CurrentReaction.GetTemperature())+" K")
        if self._CurrentReaction.GetEndothermic():
            self._painter.drawText(200, 350, "Reaction is endothermic")
        else:
            self._painter.drawText(200, 350, "Reaction is exothermic")
        if self._showlabels.isChecked():
            if self._kcdifference == "":
                self._kclabel.show()
            else:
                self._kclabel.hide()
            self._painter.drawText(420, 330, self._kcdifference)
        else:
            self._kclabel.hide()
        for x in self._Squares:
            x.Draw(self._painter)
        self._painter.end()

    def SetReaction(self, reaction):
        if self._IsReadOnly:
            self._CurrentReaction = copy.deepcopy(reaction)
        else:
            self._CurrentReaction = reaction
        self.update()

    def GetReaction(self):
        return self._CurrentReaction

    def MakeConcGraphs(self):
        gwg = GraphWindowGroup(GraphWindow(self._CurrentReaction, "Concentration", self, False),
                               GraphWindow(self.parent().parent().parent().GetComparingReaction(), "Concentration", self, False),
                               self)
        gwg.setGeometry(0, 400, 800, 320)
        self._ExtraWindows.append(gwg)
        self._ExtraWindows[-1].show()

    def MakeRateGraphs(self):
        gwg = GraphWindowGroup(GraphWindow(self._CurrentReaction, "Rate", self, False),
                               GraphWindow(self.parent().parent().parent().GetComparingReaction(), "Rate", self, False),
                               self)
        gwg.setGeometry(420, 400, 800, 320)
        self._ExtraWindows.append(gwg)
        self._ExtraWindows[-1].show()

    def SetReactantColour(self):
        picker = QColorDialog()
        picker.exec_()
        if picker.selectedColor() is not None:
            self._CurrentReaction.SetReactantColour(picker.selectedColor())

    def SetProductColour(self):
        picker = QColorDialog()
        picker.exec_()
        if picker.selectedColor() is not None:
            self._CurrentReaction.SetProductColour(picker.selectedColor())

    def GetKc(self):
        kc = self._CurrentReaction.GetKc()
        newkc = "K<sub>c</sub>"
        x = 2
        while x in range(len(kc)):
            if kc[x] == "^":
                x += 1
                newkc += "<sup>"
                newkc += kc[x]
                newkc += "</sup>"
            else:
                newkc += kc[x]
            x += 1
        self._kclabel.setText(newkc)
        self.update()

    def ShowWorking(self):
        getcontext().prec = 3
        working = QPlainTextEdit()
        working.setWindowTitle("Kc calculation")
        reactants = []
        products = []
        for x in self._CurrentReaction.GetReactants():
            if x.GetUsed():
                reactants.append(x)
        for x in self._CurrentReaction.GetProducts():
            if x.GetUsed():
                products.append(x)
        working.appendPlainText("Concentration = moles / volume")
        volume = self._CurrentReaction.GetVolume()
        working.appendPlainText("Volume = "+str(volume)+" dm^3")
        pvalues = []
        rvalues = []
        for x in products:
            working.appendPlainText("Concentration of "+x.GetFormula()+" = "+str(Decimal(x.GetConcentration(volume)) + Decimal(0.0))+" mol dm^-3")
            pvalues.append(x.GetConcentration(volume))
            pvalues.append(x.GetSRatio())
        for x in reactants:
            working.appendPlainText("Concentration of "+x.GetFormula()+" = "+str(Decimal(x.GetConcentration(volume)) + Decimal(0.0))+" mol dm^-3")
            rvalues.append(x.GetConcentration(volume))
            rvalues.append(x.GetSRatio())
        kcvalue = "Value of Kc ="
        x = 0
        while x < len(pvalues):
            kcvalue += " ("+str(Decimal(pvalues[x]) + Decimal(0.0))+")^"
            x += 1
            kcvalue += str(pvalues[x])
            x += 1
        kcvalue += " /"
        x = 0
        while x < len(rvalues):
            kcvalue += " ("+str(Decimal(rvalues[x]) + Decimal(0.0))+")^"
            x += 1
            kcvalue += str(rvalues[x])
            x += 1
        working.appendPlainText(kcvalue)
        rproductsum = 0
        for x in reactants:
            rproductsum += x.GetSRatio()
        pproductsum = 0
        for x in products:
            pproductsum += x.GetSRatio()
        working.appendPlainText("There are "+str(len(reactants))+" reactants, with units mol dm^-3.")
        working.appendPlainText("The product of these units is mol^"+str(rproductsum)+" dm^"+str(rproductsum * -3)+".")
        working.appendPlainText("There are "+str(len(products))+" products, with units mol dm^-3.")
        working.appendPlainText("The product of these units is mol^"+str(pproductsum)+" dm^"+str(pproductsum * -3)+".")
        working.appendPlainText("The product units must be divided by the reactant units, so")
        working.appendPlainText(self._CurrentReaction.GetKc())
        self._ExtraWindows.append(working)
        working.show()

    def StartAnimation(self):
        self._no_of_anim_updates = 0
        reactants = []
        for x in self._CurrentReaction.GetReactants():
            if x.GetUsed():
                reactants.append(x)
        products = []
        for x in self._CurrentReaction.GetProducts():
            if x.GetUsed():
                products.append(x)
        self._eqmratio = self.GetRPRatio(reactants, products)
        self._rflipchance = int(self._eqmratio * 100)
        # self._pflipchance = int((1 / self._eqmratio) * 100)
        self._pflipchance = int((1 - self._eqmratio) * 100)
        if self._CurrentReaction.GetCatalyst().GetUsed():
            efficacy = self._CurrentReaction.GetCatalyst().GetEfficacy()
            self._rflipchance /= efficacy
            self._pflipchance /= efficacy
            flipchancechangefromcata = 2.0 * (self._CurrentReaction.GetCatalyst().GetInitialMoles() / 100)
            if efficacy > 1:
                flipchancechangefromcata *= -1
            self._rflipchance = int(self._rflipchance + flipchancechangefromcata)
            self._pflipchance = int(self._pflipchance + flipchancechangefromcata)
        for x in self._Squares:
            x.Reset()
        self._timer.start()

    def ContinueAnimation(self):
        self._no_of_anim_updates += 1
        reactantsquares = 0
        for x in self._Squares:
            if x.GetIsReactant():
                reactantsquares += 1
        print("Reactant squares: "+str(reactantsquares))
        # currentratio = reactantsquares / (101 - reactantsquares)
        currentratio = reactantsquares / 100
        newrflipchance = self._rflipchance
        newpflipchance = self._pflipchance
        if currentratio < int(self._eqmratio * 100):
            newrflipchance -= currentratio * 0.2
            newpflipchance += currentratio * 0.2
        elif currentratio > int(self._eqmratio * 100):
            newrflipchance += currentratio * 0.2
            newpflipchance -= currentratio * 0.2
        for x in self._Squares:
            x.Flip(newrflipchance, newpflipchance)
        self.update()
        for x in self._ExtraWindows:
            if type(x) == GraphWindowGroup:
                x.update()
        if self._no_of_anim_updates > 1000:
            self._timer.stop()

    def RemoveMe(self, qwidg):
        self._ExtraWindows.remove(qwidg)

    def Clone(self):
        self.parent().parent().parent().SetComparingReaction(self._CurrentReaction)

    def SetKcDifference(self, string):
        self._kcdifference = string

    def PrintGraph(self, painter, graphof):
        GraphWindow(self._CurrentReaction, graphof, self, True).render(painter)

    def GetRPRatio(self, reactants, products):
        # volume = self._CurrentReaction.GetVolume()
        # arc = 0
        # for x in reactants:
        #     arc += x.GetConcentration(volume)
        # arc /= len(reactants)
        # apc = 0
        # for x in products:
        #     apc += x.GetConcentration(volume)
        # apc /= len(products)
        # return arc / apc
        rm = 0
        for x in reactants:
            rm += x.GetInitialMoles()
        pm = 0
        for x in products:
            pm += x.GetInitialMoles()
        return rm / (rm + pm)

    def GetAnimUpdates(self):
        return self._no_of_anim_updates
from decimal import *
from PyQt4.QtGui import QColor
from chem.Reactant import Reactant
from chem.Product import Product
from chem.Catalyst import Catalyst

class Reaction():
    # Fixed constant. The maximum number of reactants and products that can take part in the reaction
    REACTING_SPECIES_LIMIT = 3

    def __init__(self):
        self._Temperature = 1
        self._Reactants = []
        self._Products = []
        for x in range(Reaction.REACTING_SPECIES_LIMIT):
            self._Reactants.append(Reactant())
            self._Products.append(Product())
        self._Catalyst = Catalyst()
        self._Volume = 0.1
        self._Endothermic = True
        self._ReactantColour = QColor(255, 0, 0, 255)
        self._ProductColour = QColor(0, 0, 255, 255)

    # Returns the value and units of the reaction's equilibrium constant as a string
    def GetKc(self):
        getcontext().prec = 3
        # Ensures only valid reactants and products are used
        reactants = []
        for x in self._Reactants:
            if x.GetUsed():
                reactants.append(x)
        products = []
        for x in self._Products:
            if x.GetUsed():
                products.append(x)
        # The actual calculation
        numerator = 1
        for x in range(len(products)):
            numerator *= (products[x].GetConcentration(self._Volume) ** products[x].GetSRatio())
        denominator = 1
        for x in range(len(reactants)):
            denominator *= (reactants[x].GetConcentration(self._Volume) ** reactants[x].GetSRatio())
        value = int((numerator / denominator) * 100) / 100
        rpower = 0
        for x in reactants:
            rpower += x.GetSRatio()
        ppower = 0
        for x in products:
            ppower += x.GetSRatio()
        power = ppower - rpower
        return "Kc = "+str(Decimal(value) + Decimal(0.00))+" mol^"+str(power)+" dm^"+str(power * -3)

    # Returns whether Kc has increased, decreased or not changed from the right to the left reaction window.
    # Cannot be calculated because Kc differs so much for each reaction
    def GetKcChange(self, temperaturechange):
        if temperaturechange == 0:
            return 'not changed'
        elif temperaturechange < 0:
            if not self._Endothermic:
                return 'increased'
            else:
                return 'decreased'
        else:
            if not self._Endothermic:
                return 'decreased'
            else:
                return 'increased'

    #GETTERS AND SETTERS
    def GetTemperature(self):
        return self._Temperature

    def SetTemperature(self, newtemp):
        self._Temperature = newtemp

    def GetReactants(self):
        return self._Reactants

    def SetReactants(self, newr):
        self._Reactants = newr

    def GetProducts(self):
        return self._Products

    def SetProducts(self, newp):
        self._Products = newp

    def GetCatalyst(self):
        return self._Catalyst

    def SetCatalyst(self, newc):
        self._Catalyst = newc

    def GetVolume(self):
        return self._Volume

    def SetVolume(self, newv):
        self._Volume = newv

    def GetEndothermic(self):
        return self._Endothermic

    def SetEndothermic(self, newe):
        self._Endothermic = newe

    def GetReactantColour(self):
        return self._ReactantColour

    def GetProductColour(self):
        return self._ProductColour

    def SetReactantColour(self, colour):
        self._ReactantColour = colour

    def SetProductColour(self, colour):
        self._ProductColour = colour
from chem.Reactant import Reactant
from chem.Product import Product
from chem.Catalyst import Catalyst

class Reaction():
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

    def GetKc(self):
        numerator = 1
        for x in range(len(self._Reactants)):
            numerator *= (self._Reactants[x].GetConcentration(self._Volume) ** self._Reactants[x].GetSRatio())
        denominator = 1
        for x in range(len(self._Products)):
            denominator *= (self._Products[x].GetConcentration(self._Volume) ** self._Products[x].GetSRatio())
        return numerator / denominator

    def GetKcChange(self, temperaturechange):
        if temperaturechange == 0:
            return 'None'
        elif temperaturechange < 0:
            if not self._Endothermic:
                return 'Increase'
            else:
                return 'Decrease'
        else:
            if not self._Endothermic:
                return 'Decrease'
            else:
                return 'Increase'

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
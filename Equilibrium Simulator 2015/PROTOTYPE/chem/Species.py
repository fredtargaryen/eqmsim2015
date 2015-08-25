class Species():
    _ValidCharacters = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz1234567890+-"

    def __init__(self):
        self._Formula = ""
        self._InitialMoles = 0.0

    def ValidateFormula(self, index, formula):
        if formula not in Species._ValidCharacters:
            return False
        else:
            if index == len(formula) - 1:
                return True
            else:
                return self.ValidateFormula(index + 1, formula)

    def GetConcentration(self, volume):
        return self._InitialMoles / volume

    # GETTERS AND SETTERS
    def GetInitialMoles(self):
        return self._InitialMoles

    def SetInitialMoles(self, newmoles):
        self._InitialMoles = newmoles

    def GetFormula(self):
        return self._Formula

    def SetFormula(self, newformula):
        self._Formula = newformula
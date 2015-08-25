class Species():
    def __init__(self):
        self._Formula = ""
        self._InitialMoles = 0.01
        self._used = False

    def GetConcentration(self, volume):
        return self._InitialMoles / volume

    # Returns its formula, edited for user-friendly display. The other getter is for internal use
    # Ensure that the widget displaying this formula supports HTML.
    def GetFormulaForLabels(self):
        x = 0
        newformula = ""
        while x in range(len(self._Formula)):
            if self._Formula[x] == "_":
                newformula += "<sub>"
                x += 1
                newformula += self._Formula[x]
                newformula += "</sub>"
            elif self._Formula[x] == "^":
                newformula += "<sup>"
                x += 1
                newformula += self._Formula[x]
                newformula += "</sup>"
            else:
                newformula += self._Formula[x]
            x += 1
        return newformula

    # GETTERS AND SETTERS
    def GetInitialMoles(self):
        return self._InitialMoles

    def SetInitialMoles(self, newmoles):
        self._InitialMoles = newmoles

    def GetFormula(self):
        return self._Formula

    def SetFormula(self, newformula):
        self._Formula = newformula

    def GetUsed(self):
        return self._used

    def SetUsed(self, u):
        self._used = u
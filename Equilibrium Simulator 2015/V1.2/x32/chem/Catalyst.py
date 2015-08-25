from chem.Species import Species

class Catalyst(Species):
    def __init__(self):
        super(Catalyst, self).__init__()
        self._Efficacy = 5

    # User-friendly representation of catalyst strength.
    # The other getter is for calculations; this one is for display on the GUI
    def GetEfficacyAsString(self):
        if self._used:
            if self._Efficacy == 5:
                return "Good"
            elif self._Efficacy == 2:
                return "Poor"
            elif self._Efficacy == 0.75:
                return "Inhibitor"
        else:
            return "Not used"

    #GETTERS AND SETTERS
    def SetEfficacy(self, e):
        self._Efficacy = e

    def GetEfficacy(self):
        return self._Efficacy
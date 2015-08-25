from chem.Species import Species

class Catalyst(Species):
    def __init__(self):
        super(Catalyst, self).__init__()
        self._EaChangePerMole = 0

    def GetEaChangePerMole(self):
        return self._EaChangePerMole

    def SetEaChangePerMole(self, neweachange):
        self._EaChangePerMole = neweachange

    def GetTotalEaChange(self):
        return self._EaChangePerMole * self._InitialMoles
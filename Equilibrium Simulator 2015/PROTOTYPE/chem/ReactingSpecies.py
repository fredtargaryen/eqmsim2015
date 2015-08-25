from chem.Species import Species

class ReactingSpecies(Species):
    def __init__(self):
        super(ReactingSpecies, self).__init__()

    def isNumber(self, ch):
        try:
            int(ch)
            return True
        except:
            return False

    def GetSRatio(self):
        if not self.isNumber(self._Formula[0]):
            return 1
        else:
            x = 1
            while self.isNumber(self._Formula[x]):
                x += 1
            return int(self._Formula[:x])
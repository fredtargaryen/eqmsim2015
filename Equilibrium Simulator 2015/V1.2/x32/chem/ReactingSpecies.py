from chem.Species import Species

class ReactingSpecies(Species):
    def __init__(self):
        super(ReactingSpecies, self).__init__()

    # Returns the species' stoichiometric ratio from its formula
    def GetSRatio(self):
        try:
            return int(self._Formula[0])
        except:
            return 1
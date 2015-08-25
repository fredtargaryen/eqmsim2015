from chem.ReactingSpecies import ReactingSpecies

class Reactant(ReactingSpecies):
    def __init__(self):
        super(Reactant,self).__init__()

    def GetUnreactedMoles(self):
        return self._TotalMoles - self._ReactingMoles
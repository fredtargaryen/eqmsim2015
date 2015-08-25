from chem.Reaction import Reaction

class ReactionFile():
    def __init__(self):
        self._Reactions = []
        self.AddReaction(Reaction())
        self._LastTabIndex = 0

    def AddReaction(self, r):
        if len(self._Reactions) < 5:
            self._Reactions.append(r)

    def DeleteReaction(self, index):
        if len(self._Reactions) > 1:
            self._Reactions.remove(index)
        else:
            self._Reactions[0] = Reaction()

    def GetReactions(self):
        return self._Reactions

    def GetLastTabOpen(self):
        return self._LastTabIndex

    def SetLastTabOpen(self, i):
        self._LastTabIndex = i
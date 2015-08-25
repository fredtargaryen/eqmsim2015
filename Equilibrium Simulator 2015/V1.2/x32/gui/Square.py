from random import randrange

# A square in the animation
class Square():
    def __init__(self, x, y, reaction):
        self._x = x
        self._y = y
        self._reactantcolour = reaction.GetReactantColour()
        self._productcolour = reaction.GetProductColour()
        self._currentcolour = self._reactantcolour

    def Flip(self, rflipchance, pflipchance):
        rflipchance = int(rflipchance)
        pflipchance = int(pflipchance)
        if self._currentcolour == self._reactantcolour:
            if rflipchance == 0:
                self._currentcolour = self._productcolour
            elif rflipchance > 0:
                if randrange(rflipchance) == 0:
                    self._currentcolour = self._productcolour
        elif self._currentcolour == self._productcolour:
            if pflipchance == 0:
                self._currentcolour = self._reactantcolour
            elif pflipchance > 0:
                if randrange(pflipchance) == 0:
                    self._currentcolour = self._reactantcolour

    def Draw(self, painter):
        painter.setBrush(self._currentcolour)
        painter.drawRect(self._x, self._y, 20, 20)

    def Reset(self):
        # Sets the square to its default state (reactant)
        self._currentcolour = self._reactantcolour

    def GetIsReactant(self):
        return self._reactantcolour == self._currentcolour
import pickle
from PyQt4.QtCore import SIGNAL
from PyQt4.QtGui import QPushButton, QTabWidget, QFileDialog
from ReactionFile import ReactionFile
from chem.Reaction import Reaction
from gui.BalanceWindow import BalanceWindow
from gui.ConditionsDialog import ConditionsDialog
from gui.ReactionProfile import ReactionProfile

class ReactionWidget(QTabWidget):
    def __init__(self):
        super(ReactionWidget, self).__init__()
        self._CurrentFile = ReactionFile()
        self.setTabsClosable(True)
        self.addTab(ReactionProfile(self._CurrentFile.GetReactions()[0], False), "Reaction 1")
        self._CurrentReaction = self._CurrentFile.GetReactions()[0]
        self._plusbtn = QPushButton("+")
        self._plusbtn.setGeometry(578, 2, 20, 20)
        self._plusbtn.clicked.connect(self.newtab)
        self._plusbtn.setParent(self)
        self._plusbtn.show()
        self.currentChanged.connect(self.SetCurrentReaction)
        self.tabBar().connect(self.tabBar(), SIGNAL("tabCloseRequested(int)"), self.RemoveReaction)
        self._errorbox = None

    def newtab(self):
        length = len(self._CurrentFile.GetReactions())
        if length < 5:
            self._CurrentFile.AddReaction(Reaction())
            self.addTab(ReactionProfile(self._CurrentFile.GetReactions()[length], False), "Reaction "+str(length + 1))

    def save(self):
        saveto = open("last.ptr", "r")
        fileaddress = saveto.read()
        saveto.close()
        if ".rctn" in fileaddress:
            saveto = open(fileaddress, "wb")
            pickle.dump(self._CurrentFile, saveto)
            saveto.close()
        else:
            self.showsaveas()

    def showsaveas(self):
        fileaddress = QFileDialog.getSaveFileName(self, "Save As...", "", "Simulator Files (*.rctn)")
        if fileaddress != "":
            self.saveas(fileaddress)
            self.parent().open(fileaddress)

    def saveas(self, fileaddress):
        saveto = open(fileaddress, "wb")
        pickle.dump(self._CurrentFile, saveto)
        saveto.close()
        saveto = open("last.ptr", "w")
        saveto.write(fileaddress)
        saveto.close()

    def EditReaction(self):
        currentreaction = self.currentWidget().GetReaction()
        dialog = ConditionsDialog(currentreaction)
        dialog.show()
        reaction = dialog.GetReaction()
        if reaction is not None:
            currentreaction = reaction
            if not dialog.GetCanShowFormulae():
                dialog.hide()
                self.parent().hide()
                BalanceWindow(reaction, self.parent()).exec_()
        copiedreaction = self.parent().GetComparingReaction()
        currentprofile = self.currentWidget()
        if currentreaction.GetEndothermic() == copiedreaction.GetEndothermic():
            oldt = copiedreaction.GetTemperature()
            newt = currentreaction.GetTemperature()
            currentprofile.SetKcDifference("Kc has "+currentreaction.GetKcChange(newt-oldt))
        else:
            currentprofile.SetKcDifference("")
        currentprofile.update()

    def RemoveReaction(self, index):
        self._CurrentFile.DeleteReaction(index)
        self.SetOpenReactionFile(self._CurrentFile)

    # GETTERS AND SETTERS
    def SetCurrentReaction(self):
        self._CurrentReaction = self._CurrentFile.GetReactions()[self.currentIndex()]
        self._CurrentFile.SetLastTabOpen(self.currentIndex())

    def GetCurrentReaction(self):
        return self._CurrentReaction

    def SetOpenReactionFile(self, file):
        self._CurrentFile = file
        self.clear()
        for x in range(len(self._CurrentFile.GetReactions())):
            self.addTab(ReactionProfile(self._CurrentFile.GetReactions()[x], False), "Reaction "+str(x+1))
        index = self._CurrentFile.GetLastTabOpen()
        self.setCurrentIndex(index)
        self._CurrentReaction = self._CurrentFile.GetReactions()[index]
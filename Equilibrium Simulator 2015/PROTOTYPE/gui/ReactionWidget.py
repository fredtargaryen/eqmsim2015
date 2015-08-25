import pickle
from PyQt4.QtGui import QPushButton, QTabWidget, QFileDialog
from ReactionFile import ReactionFile
from chem.Reaction import Reaction
from gui.ConditionsDialog import ConditionsDialog
from gui.ReactionProfile import ReactionProfile

class ReactionWidget(QTabWidget):
    def __init__(self):
        super(ReactionWidget, self).__init__()
        self._CurrentFile = ReactionFile()
        self.setTabsClosable(True)
        self.addTab(ReactionProfile(self._CurrentFile.GetReactions()[0]), "Reaction 1")
        self._CurrentReaction = self._CurrentFile.GetReactions()[0]
        self._plusbtn = QPushButton("+")
        self._plusbtn.setGeometry(780, 0, 20, 20)
        self._plusbtn.clicked.connect(self.newtab)
        self._plusbtn.setParent(self)
        self._plusbtn.show()
        self.currentChanged.connect(self.SetCurrentReaction)

    def newtab(self):
        length = len(self._CurrentFile.GetReactions())
        if length < 5:
            self._CurrentFile.addReaction(Reaction())
            self.addTab(ReactionProfile(self._CurrentFile.GetReactions()[length]), "Reaction "+str(length + 1))

    def SetCurrentReaction(self):
        self._CurrentReaction = self._CurrentFile.GetReactions()[self.currentIndex()]
        self._CurrentFile.SetLastTabOpen(self.currentIndex())

    def SetOpenReactionFile(self, file):
        self._CurrentFile = file
        self.clear()
        for x in range(len(self._CurrentFile.GetReactions())):
            self.addTab(ReactionProfile(self._CurrentFile.GetReactions()[x]), "Reaction "+str(x+1))
        index = self._CurrentFile.GetLastTabOpen()
        self.setCurrentIndex(index)
        self._CurrentReaction = self._CurrentFile.GetReactions()[index]

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
        currentreaction = self._CurrentFile.GetReactions()[self.currentIndex()]
        currentreaction = ConditionsDialog(currentreaction).GetReaction()
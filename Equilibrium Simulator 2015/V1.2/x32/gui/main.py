import sys
from PyQt4 import QtGui
from PyQt4.QtGui import QMessageBox
from ReactionFile import ReactionFile
from gui.MainWindow import MainWindow

class Main():
    def __init__(self):
        self._Application = QtGui.QApplication(sys.argv)
        self._CurrentFile = ReactionFile()
        self._Window = MainWindow()
        # Checks for last file opened using the last.ptr file, which
        # only contains (and should only contain) a filepath.
        try:
            self._PointerFileToLastFile = open("last.ptr", "r")
            self._LastFileAddress = self._PointerFileToLastFile.read()
            self._PointerFileToLastFile.close()
            if ".rctn" in self._LastFileAddress:
                self._newfilebox = QMessageBox()
                self._newfilebox.setModal(True)
                self._newfilebox.setWindowTitle("Open most recent file?")
                self._newfilebox.setText("The last file you opened was "+self._LastFileAddress+". Would you like to open it now?")
                self._newfilebox.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
                self._newfilebox.setDefaultButton(QMessageBox.Ok)
                if self._newfilebox.exec_() == QMessageBox.Ok:
                    self._Window.open(self._LastFileAddress)
        except:
            self._PointerFileToLastFile = open("last.ptr", "w")
            self._PointerFileToLastFile.write("")
            self._PointerFileToLastFile.close()
            self._Window = MainWindow()
        sys.exit(self._Application.exec_())

Main()
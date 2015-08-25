from PyQt4.QtGui import QMainWindow, QAction, QIcon, qApp, QFileDialog, QMessageBox, QPrintDialog, QDialog, QPrinter, \
    QPainter
import pickle
from ReactionFile import ReactionFile
from gui.ReactionProfile import ReactionProfile
from gui.ReactionWidget import ReactionWidget


class MainWindow(QMainWindow):
    def __init__(self):
        super(QMainWindow, self).__init__()
        self._TITLE = 'Equilibrium Simulator 2015'
        self.setGeometry (0, 22, 1200, 400)
        self.setWindowTitle(self._TITLE)
        self._showorhide = "Show "
        self._printbox = None
        self._printer = QPrinter()
        self._Squares = []

        # Menu bar
        self.MenuBar = self.menuBar()
        self.filemenu = self.MenuBar.addMenu('File')
        self.optionsmenu = self.MenuBar.addMenu('Options')
        self.aboutmenu = self.MenuBar.addMenu('About')

        # File - New
        newfile = QAction(QIcon('exit.png'), 'New', self)
        newfile.setStatusTip('Create a new file')
        self.filemenu.addAction(newfile)
        newfile.triggered.connect(self.shownew)

        # File - Open
        openfile = QAction(QIcon('open.png'), 'Open', self)
        openfile.setStatusTip('Open a file')
        self.filemenu.addAction(openfile)
        openfile.triggered.connect(self.showopen)

        # File - Save
        savefile = QAction(QIcon('save.png'), 'Save', self)
        savefile.setStatusTip('Save the current file')
        self.filemenu.addAction(savefile)
        savefile.triggered.connect(self.save)

        # File - Save as
        saveasfile = QAction(QIcon('save.png'), 'Save as', self)
        saveasfile.setStatusTip('Save the current file as a different file')
        self.filemenu.addAction(saveasfile)
        saveasfile.triggered.connect(self.showsaveas)

        # File - Print
        printfile = QAction(QIcon('save.png'), 'Print', self)
        printfile.setStatusTip('Print the displayed reactions')
        self.filemenu.addAction(printfile)
        printfile.triggered.connect(self.showprint)

        # File - Exit
        exitaction = QAction(QIcon('exit.png'), '&Exit', self)
        exitaction.setStatusTip('Exit the program')
        exitaction.triggered.connect(qApp.quit)
        self.filemenu.addAction(exitaction)

        # Options - Edit Conditions
        editconds = QAction(QIcon('exit.png'), 'Edit Conditions', self)
        editconds.setStatusTip('Edit the conditions of the current reaction')
        editconds.triggered.connect(self.editcd)
        self.optionsmenu.addAction(editconds)

        # About - Version
        version = QAction(QIcon('exit.png'), 'Version 1.1', self)
        version.setStatusTip('The version of this program you are using')

        # Widget of editable reactions
        self._ReactionsWindow = ReactionWidget()
        self._ReactionsWindow.setGeometry(0, 20, 600, 380)
        self._ReactionsWindow.setParent(self)

        # Widget of non-editable reaction, for comparison
        self._ComparingProfile = ReactionProfile(self._ReactionsWindow.GetCurrentReaction(), True)
        self._ComparingProfile.setGeometry(600, 40, 600, 380)
        self._ComparingProfile.setParent(self)
        self.aboutmenu.addAction(version)
        self.show()

    # You should call the shownew(), showopen() etc. methods,
    # not the new(), open() etc. methods, as a) they do not provide user options;
    # b) it may lead to errors; c) the showing methods call them anyway
    def editcd(self):
        self._ReactionsWindow.EditReaction()

    def showopen(self):
        fileaddress = QFileDialog.getOpenFileName(self, "Open...", "", "Simulator Files (*.rctn)")
        if fileaddress != "":
            self.open(fileaddress)
            self.setWindowTitle(fileaddress+" - "+self._TITLE)

    def open(self, fileaddress):
        openfrom = open(fileaddress, "rb")
        loadedfile = pickle.load(openfrom)
        openfrom.close()
        file = open("last.ptr", "w")
        file.write(fileaddress)
        file.close()
        self._ReactionsWindow.SetOpenReactionFile(loadedfile)
        self.setWindowTitle(fileaddress+" - "+self._TITLE)

    def save(self):
        self._ReactionsWindow.save()

    def showsaveas(self):
        self._ReactionsWindow.showsaveas()

    def shownew(self):
        self._newfilebox = QMessageBox()
        self._newfilebox.setWindowTitle("Save?")
        self._newfilebox.setText("Would you like to save this file before opening a new one?")
        self._newfilebox.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        self._newfilebox.setDefaultButton(QMessageBox.Yes)
        if self._newfilebox.exec_() == QMessageBox.Yes:
            file = open("last.ptr", "w")
            file.write("")
            file.close()
            self.save()
        self.setWindowTitle(self._TITLE)
        self._ReactionsWindow.SetOpenReactionFile(ReactionFile())

    def showprint(self):
        self._printbox = QPrintDialog(self)
        if self._printbox.exec_() == QDialog.Accepted:
            self.printout()

    def printout(self):
        # Page width, page height, widget width
        pw = self._printer.pageRect().width()
        ph = self._printer.pageRect().height()
        ww = self._ComparingProfile.width()
        painter = QPainter(self._printer)
        scale = (ww / pw) * 1.5
        painter.scale(scale, scale)
        self._ReactionsWindow.currentWidget().render(painter)
        painter.translate(0, ph/2)
        self._ComparingProfile.render(painter)
        painter.translate(pw * 0.6, -ph/2)
        painter.scale(0.8, 0.8)
        self._ReactionsWindow.currentWidget().PrintGraph(painter, "Concentration")
        painter.translate(0, ph*0.25)
        self._ReactionsWindow.currentWidget().PrintGraph(painter, "Rate")
        painter.translate(0, ph * 0.4)
        self._ComparingProfile.PrintGraph(painter, "Concentration")
        painter.translate(0, ph * 0.25)
        self._ComparingProfile.PrintGraph(painter, "Rate")
        painter.end()

    # GETTERS AND SETTERS
    def GetWindowTitle(self):
        return self._TITLE

    def SetComparingReaction(self, reaction):
        self._ComparingProfile.SetReaction(reaction)
        self._ComparingProfile.update()

    def GetComparingReaction(self):
        return self._ComparingProfile.GetReaction()
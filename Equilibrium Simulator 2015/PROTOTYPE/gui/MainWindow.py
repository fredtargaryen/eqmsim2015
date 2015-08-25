from PyQt4.QtGui import QMainWindow, QAction, QIcon, qApp, QFileDialog, QMessageBox
import pickle
from ReactionFile import ReactionFile
from gui.ReactionWidget import ReactionWidget


class MainWindow(QMainWindow):
    def __init__(self):
        super(QMainWindow, self).__init__()
        self._TITLE = 'Equilibrium Simulator 2014 (PROTOTYPE)'
        self.setGeometry (200, 200, 800, 400)
        self.setWindowTitle(self._TITLE)
        self._buttonpressed = 0
        self._showorhide = "Show "
        self._filedialog = None
        self._GraphWindow = None
        # Menu bar
        self.MenuBar = self.menuBar()
        self.filemenu = self.MenuBar.addMenu('File')
        self.optionsmenu = self.MenuBar.addMenu('Options')
        self.aboutmenu = self.MenuBar.addMenu('About')
        # File - New. Will later create a new set of reactions
        newfile = QAction(QIcon('exit.png'), 'New', self)
        newfile.setShortcut('Ctrl+N')
        newfile.setStatusTip('Create a new file')
        self.filemenu.addAction(newfile)
        newfile.triggered.connect(self.shownew)
        # File - Open
        openfile = QAction(QIcon('open.png'), 'Open', self)
        openfile.setShortcut('Ctrl+O')
        openfile.setStatusTip('Open a file')
        self.filemenu.addAction(openfile)
        openfile.triggered.connect(self.showopen)
        # File - Save
        savefile = QAction(QIcon('save.png'), 'Save', self)
        savefile.setShortcut('Ctrl+S')
        savefile.setStatusTip('Save the current file')
        self.filemenu.addAction(savefile)
        savefile.triggered.connect(self.save)
        # File - Save as
        saveasfile = QAction(QIcon('save.png'), 'Save as', self)
        saveasfile.setShortcut('Ctrl+Shift+S')
        saveasfile.setStatusTip('Save the current file as a different file')
        self.filemenu.addAction(saveasfile)
        saveasfile.triggered.connect(self.showsaveas)
        # File - Exit
        exitaction = QAction(QIcon('exit.png'), '&Exit', self)
        exitaction.setShortcut('Ctrl+Q')
        exitaction.setStatusTip('Exit the program')
        exitaction.triggered.connect(qApp.quit)
        self.filemenu.addAction(exitaction)
        # Options - Edit Conditions
        editconds = QAction(QIcon('exit.png'), '&Edit Conditions', self)
        editconds.setShortcut('Ctrl+E')
        editconds.setStatusTip('Edit the conditions of the current reaction')
        editconds.triggered.connect(self.editcd)
        self.optionsmenu.addAction(editconds)
        # About - User Guide
        ug = QAction(QIcon('exit.png'), '&User Guide', self)
        ug.setStatusTip('View a digital copy of the user manual')
        self.aboutmenu.addAction(ug)
        # About - Version
        version = QAction(QIcon('exit.png'), '&Version 0.1 (Alpha)', self)
        version.setStatusTip('The version of this program you are using')
        # Reactions window
        self._ReactionsWindow = ReactionWidget()
        self._ReactionsWindow.setGeometry(0, 40, 800, 380)
        self._ReactionsWindow.setParent(self)
        self.setCentralWidget(self._ReactionsWindow)
        self.aboutmenu.addAction(version)
        self.show()

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
        self._buttonpressed = self._newfilebox.exec_()
        if self._buttonpressed == QMessageBox.Yes:
            self.save()
        self.setWindowTitle(self._TITLE)
        self._ReactionsWindow.SetOpenReactionFile(ReactionFile())

    def GetWindowTitle(self):
        return self._TITLE
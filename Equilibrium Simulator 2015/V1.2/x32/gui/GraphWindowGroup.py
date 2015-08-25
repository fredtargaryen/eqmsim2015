from PyQt4.QtGui import QWidget, QPushButton, QGridLayout


class GraphWindowGroup(QWidget):
    def __init__(self, leftwindow, rightwindow, parentwindow):
        super(GraphWindowGroup, self).__init__()
        self.setWindowTitle("Compare Graphs")
        self._Left = leftwindow
        self._Left.setParent(self)
        self._Left.show()
        self._Right = rightwindow
        self._Right.setParent(self)
        self._Right.show()
        self._closebtn = QPushButton("Close", self)
        self._closebtn.clicked.connect(self.close)
        self._grid = QGridLayout()
        self._grid.addWidget(self._Left, 0, 0)
        self._grid.addWidget(self._Right, 0, 2)
        self._grid.addWidget(self._closebtn, 1, 1)
        self._parent = parentwindow
        self.setLayout(self._grid)

    def update(self):
        self._Left.update()
        self._Right.update()
        super(GraphWindowGroup, self).update()

    def GetAnimUpdates(self):
        return self._parent.GetAnimUpdates()
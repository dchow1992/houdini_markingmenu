import hou

from PySide2 import QtWidgets


class LabelComboBox(QtWidgets.QWidget):
    def __init__(self, name, minxsize):
        super(LabelComboBox, self).__init__()
        self.name = name
        self.minxsize = minxsize
        self.initUI()

    def initUI(self):
        self.layout = QtWidgets.QHBoxLayout()
        self.label = QtWidgets.QLabel(self.name)

        self.comboBox = hou.qt.createComboBox()
        self.comboBox.setMinimumSize(self.minxsize, 0)
        self.comboBox.setStyleSheet(hou.qt.styleSheet())

        self.layout.addWidget(self.label)
        self.layout.addSpacing(5)
        self.layout.addWidget(self.comboBox)
        self.layout.addStretch(1)

import hou

from PySide2 import QtWidgets


class EditorTaskbar(QtWidgets.QWidget):
    def __init__(self):
        super(EditorTaskbar, self).__init__()
        self.initUI()

    def initUI(self):
        self.layout = QtWidgets.QHBoxLayout()
        self.layout.addStretch(1)

        self.saveTextWidget = QtWidgets.QLabel()
        self.saveTextWidget.setStyleSheet('font: 18pt;')

        self.layout.addWidget(self.saveTextWidget)
        self.layout.addStretch(1)

        self.saveButton = QtWidgets.QPushButton('Save Collection')
        self.closeButton = QtWidgets.QPushButton('Close')

        self.saveButton.setMinimumSize(220, 70)
        self.closeButton.setMinimumSize(220, 70)

        self.saveButton.setStyleSheet(hou.qt.styleSheet())
        self.closeButton.setStyleSheet(hou.qt.styleSheet())

        self.layout.addWidget(self.saveButton)
        self.layout.addWidget(self.closeButton)

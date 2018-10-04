import hou

from PySide2 import QtWidgets


class ManageCollectionsToolbar(QtWidgets.QWidget):
    def __init__(self):
        super(ManageCollectionsToolbar, self).__init__()
        self.initUI()

    def initUI(self):
        self.unlinkedStyle = '''
            QComboBox
            {
                background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                            stop: 0.0 rgb(86, 86, 86),
                            stop: 1.0 rgb(58, 58, 58));

                border-top: 1px solid rgba(0, 0, 0, 40%);
                border-right: 1px solid rgba(0, 0, 0, 40%);
                border-bottom: 1px solid rgba(0, 0, 0, 62%);
                border-left: 1px solid rgba(0, 0, 0, 40%);

                border-radius: 1px;
                padding: 2px 10px 2px 10px;
            }

            QComboBox:disabled
            {
                background: rgba(58, 58, 58, 40%);

                border-top: 1px solid rgba(0, 0, 0, 16%);
                border-right: 1px solid rgba(0, 0, 0, 16%);
                border-bottom: 1px solid rgba(0, 0, 0, 25%);
                border-left: 1px solid rgba(0, 0, 0, 16%);

                color: rgb(131, 131, 131);
            }

            QComboBox::down-arrow
            {
                width: 0;
                height: 0;
                border-left: 3px solid rgba(63, 63, 63, 0);
                border-right: 3px solid rgba(63, 63, 63, 0);
                border-top: 5px solid rgb(131, 131, 131);
            }

            QComboBox::drop-down
            {
                background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                            stop: 0.0 rgb(63, 63, 63),
                            stop: 1.0 rgb(38, 38, 38));
                width: 22px;
            }

            QComboBox QAbstractItemView
            {
                background-color: rgb(58, 58, 58);
                color: rgb(203, 203, 203);
                margin: 0px;

                border-top: 1px solid rgb(147, 147, 147);
                border-right: 1px solid rgb(38, 38, 38);
                border-bottom: 1px solid rgb(38, 38, 38);
                border-left: 1px solid rgb(147, 147, 147);
                padding: 0px;
            }

            QComboBox QAbstractItemView::item
            {
                padding: 5px 10px 5px 10px;
            }

            QComboBox QAbstractItemView::item:selected
            {
                background-color: rgb(178, 101, 0);
                color: rgb(255, 255, 255);
            }
            '''

        # collections combo box
        self.layout = QtWidgets.QHBoxLayout()
        self.layout.setSpacing(0)

        self.reloadBtn = QtWidgets.QPushButton('Reload Collection')
        self.reloadBtn.setIcon(hou.qt.createIcon('BUTTONS_cook'))

        self.contextComboBox = hou.qt.createComboBox()
        self.contextComboBox.setMinimumContentsLength(5)

        self.contextComboBox.setStyleSheet(self.unlinkedStyle)

        self.collectionComboBox = hou.qt.createComboBox()
        self.collectionComboBox.setMinimumContentsLength(35)

        self.collectionComboBox.setStyleSheet(self.unlinkedStyle)

        # new / delete / rename collection buttons
        self.newBtn = QtWidgets.QPushButton('New Collection')
        self.delBtn = QtWidgets.QPushButton('Delete Collection')
        self.renameBtn = QtWidgets.QPushButton('Rename Collection')

        self.reloadBtn.setStyleSheet(hou.qt.styleSheet())
        self.newBtn.setStyleSheet(hou.qt.styleSheet())
        self.delBtn.setStyleSheet(hou.qt.styleSheet())
        self.renameBtn.setStyleSheet(hou.qt.styleSheet())

        # local layout
        self.layout.addWidget(self.reloadBtn)
        self.layout.addSpacing(10)
        self.layout.addWidget(self.contextComboBox)
        self.layout.addSpacing(10)
        self.layout.addWidget(self.collectionComboBox)
        self.layout.addSpacing(10)
        self.layout.addWidget(self.newBtn)
        self.layout.addSpacing(10)
        self.layout.addWidget(self.delBtn)
        self.layout.addSpacing(10)
        self.layout.addWidget(self.renameBtn)
        self.layout.addStretch(1)

import os

import hou

from PySide2 import QtWidgets, QtGui, QtCore

from houdini_markingmenu import utils


class DetailsPane(QtWidgets.QWidget):
    def __init__(self, rootpath):
        super(DetailsPane, self).__init__()

        # self.iconCompleter = utils.buildCompleter(
        #     os.path.join(os.environ['REZ_HOUDINI_MARKINGMENU_ROOT'],
        #                  'python',
        #                  'houdini_markingmenu',
        #                  'json',
        #                  'icons.json')
        #     )

        # build icon completer
        categories = hou.nodeTypeCategories()
        strlist = []
        for category in categories.keys():
            node_types = categories[category].nodeTypes()
            for node_type in node_types.keys():
                strlist.append(node_types[node_type].icon())

        comp = QtWidgets.QCompleter(list(set(strlist)))
        comp.popup().setStyleSheet(hou.qt.styleSheet())
        comp.setCompletionMode(QtWidgets.QCompleter.PopupCompletion)
        self.iconCompleter = comp

        self.initUI()

    def initUI(self):
        self.layout = QtWidgets.QGridLayout()
        self.layout.setSpacing(10)

        # widget arrays
        self.indexComboBoxes = []
        self.activeToggles = []
        self.menuToggles = []
        self.labelEdits = []
        self.iconEdits = []
        self.menuComboBoxes = []
        self.cmdLabels = []
        self.cmdComboBoxes = []
        self.cmdEdits = []
        self.wireToggles = []

        # widget arrays by row and split by menu or button
        self.menuWidgets = []
        self.buttonWidgets = []

        # all enabled checkbox
        self.allActiveToggle = hou.qt.createCheckBox()
        self.layout.addWidget(self.allActiveToggle, 0, 1, 1, 1)
        # self.allActiveToggle.stateChanged.connect(self.allEnabled)

        # all menu checkbox
        self.allMenuToggle = hou.qt.createCheckBox()
        self.layout.addWidget(self.allMenuToggle, 0, 2, 1, 1)
        # self.allMenuToggle.stateChanged.connect(self.allMenus)

        # all active wire on create checkbox
        self.allWireToggle = hou.qt.createCheckBox()
        self.layout.addWidget(self.allWireToggle, 0, 9, 1, 1)
        # self.allWireToggle.stateChanged.connect(self.allActiveWires)

        # separator
        self.detailSeparatorWidget = hou.qt.createSeparator()
        self.detailSeparatorWidget.setStyleSheet(hou.qt.styleSheet())
        self.layout.addWidget(self.detailSeparatorWidget, 1, 0, 1, 10)

        # header labels
        labels = ['  INDEX', 'LABEL', 'ICON', '  LINKED MENU',
                  '  FUNCTION TYPE', '  ACTION']

        labelcolumns = [0, 3, 4, 5, 7, 8]
        for label, col in zip(labels, labelcolumns):
            label = QtWidgets.QLabel(label)
            font = QtGui.QFont()
            font.setBold(True)
            label.setFont(font)
            self.layout.addWidget(label, 0, col, 1, 1)

        comboStyle = '''
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
        lineEditStyle = '''
            QLineEdit
            {
                background-color: rgb(46, 46, 46);
                border: 1px solid rgb(35, 35, 35);
                border-radius: 1px;
                padding: 1px 1px;
                selection-color: rgb(0, 0, 0);
                selection-background-color: rgb(184, 133, 32);
            }

            QLineEdit:disabled
            {
                background-color: rgba(58, 58, 58, 40%);

                border-top: 1px solid rgba(0, 0, 0, 16%);
                border-right: 1px solid rgba(0, 0, 0, 16%);
                border-bottom: 1px solid rgba(0, 0, 0, 25%);
                border-left: 1px solid rgba(0, 0, 0, 16%);
            }
            '''

        # for each button (8 max per collection) 10 = 8 + 2
        for i in range(2, 10):
            rowMenuWidgets = []
            rowButtonWidgets = []

            # index comboboxes
            a = hou.qt.createComboBox()
            a.setStyleSheet(comboStyle)
            a.setMaximumSize(70, 200)
            self.indexComboBoxes.append(a)
            self.layout.addWidget(a, i, 0, 1, 1)

            # enabled checkboxes
            h = hou.qt.createCheckBox()
            h.setText('Item %d' % (i-2))
            h.setCheckState(QtCore.Qt.CheckState.Checked)
            self.activeToggles.append(h)
            self.layout.addWidget(h, i, 1, 1, 1)

            # is menu checkboxes
            a = hou.qt.createCheckBox()
            a.setText('Menu')
            self.menuToggles.append(a)
            self.layout.addWidget(a, i, 2, 1, 1)

            # label line edits
            a = QtWidgets.QLineEdit()
            a.setStyleSheet(lineEditStyle)
            a.setPlaceholderText('Label')
            a.setFixedSize(140, a.sizeHint().height())
            self.labelEdits.append(a)
            self.layout.addWidget(a, i, 3, 1, 1)

            # icon line edits
            a = QtWidgets.QLineEdit()
            a.setStyleSheet(lineEditStyle)
            a.setPlaceholderText('Icon - ex: MISC_python')
            a.setFixedSize(150, a.sizeHint().height())
            a.setCompleter(self.iconCompleter)
            self.iconEdits.append(a)
            self.layout.addWidget(a, i, 4, 1, 1)

            # menu combo boxes
            a = hou.qt.createComboBox()
            a.setStyleSheet(comboStyle)
            a.setFixedSize(160, a.sizeHint().height())
            self.menuComboBoxes.append(a)
            self.layout.addWidget(a, i, 5, 1, 1)
            rowMenuWidgets.append(a)

            # command labels
            a = QtWidgets.QLabel('Mode: ')
            self.cmdLabels.append(a)
            self.layout.addWidget(a, i, 6, 1, 1)
            rowButtonWidgets.append(a)

            # command type combo boxes
            a = hou.qt.createComboBox()
            a.setStyleSheet(comboStyle)
            a.setFixedSize(130, a.sizeHint().height())
            self.cmdComboBoxes.append(a)
            self.layout.addWidget(a, i, 7, 1, 1)
            rowButtonWidgets.append(a)

            # nodename or custom command function line edits
            a = QtWidgets.QLineEdit()
            a.setStyleSheet(lineEditStyle)
            a.setPlaceholderText('nodename')
            self.cmdEdits.append(a)
            self.layout.addWidget(a, i, 8, 1, 1)
            rowButtonWidgets.append(a)

            # active wire checkboxes
            a = hou.qt.createCheckBox()
            a.setText('Active Wire')
            self.wireToggles.append(a)
            self.layout.addWidget(a, i, 9, 1, 1)
            rowButtonWidgets.append(a)

            self.menuWidgets.append(rowMenuWidgets)
            self.buttonWidgets.append(rowButtonWidgets)

import hou

from PySide2 import QtWidgets

from subwidgets import referencebuttons

reload(referencebuttons)


class ReferenceView(QtWidgets.QWidget):
    def __init__(self, *args, **kwargs):
        super(ReferenceView, self).__init__()
        self.HIGH_DPI = kwargs['highdpi']
        self.modifierlen = 29 if kwargs['highdpi'] else 7
        self.dpifactor = 1.2 if kwargs['highdpi'] else 1
        self.minsize = 495
        if self.HIGH_DPI:
            self.minsize = 12*(len('SHIFT: Base Collection')-1) + (self.modifierlen) + 350*self.dpifactor

        self.initUI()

    def initUI(self):
        self.layout = QtWidgets.QHBoxLayout()

        self.tree = QtWidgets.QTreeWidget(self)
        self.tree.setColumnCount(1)
        self.tree.setHeaderLabel('Marking Menu Collection Overview')
        self.tree.setItemsExpandable(False)
        self.tree.setMinimumSize(self.minsize, 0) # this is the same length as the modifier comboboxes
        # self.tree.setStyleSheet('''QTreeView::branch:open {
        #      image: url(none.png); } ''')
        self.tree.setStyleSheet(hou.qt.styleSheet())

        self.layout.addWidget(self.tree)
        self.layout.addStretch(1)

        self.refBtns = referencebuttons.ReferenceButtons(highdpi=self.HIGH_DPI)
        self.btns = self.refBtns.btns
        self.backbtn = self.refBtns.backbtn
        self.homebtn = self.refBtns.homebtn

        self.legend_menus = range(8)
        self.legend_collections = range(8)
        self.legend_actions = range(8)
        for idx, btn in enumerate(self.btns):            
            menu = QtWidgets.QMenu()
            goto_action = menu.addAction('Go to..')
            self.legend_actions[idx] = goto_action
            self.legend_menus[idx] = menu
            self.legend_collections[idx] = 'None'
            btn.setMenu(menu)

        self.layout.addLayout(self.refBtns.layout)
        self.layout.addStretch(1)

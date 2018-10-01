from Qt_py.Qt import QtWidgets
 
from subwidgets import referencebuttons
 
reload(referencebuttons)
 
 
class ReferenceView(QtWidgets.QWidget):
    def __init__(self):
        super(ReferenceView, self).__init__()
        self.initUI()
 
    def initUI(self):
        self.layout = QtWidgets.QHBoxLayout()
 
        self.tree = QtWidgets.QTreeWidget(self)
        self.tree.setColumnCount(1)
        self.tree.setHeaderLabel('Marking Menu Collection Overview')
        self.tree.setItemsExpandable(False)
        self.tree.setMinimumSize(500, 0)
        self.tree.setStyleSheet('''QTreeView::branch:open {
             image: url(none.png); } ''')
 
        self.layout.addWidget(self.tree)
        self.layout.addStretch(1)
 
        self.refBtns = referencebuttons.ReferenceButtons()
        self.btns = self.refBtns.btns
 
        self.layout.addLayout(self.refBtns.layout)
        self.layout.addStretch(1)

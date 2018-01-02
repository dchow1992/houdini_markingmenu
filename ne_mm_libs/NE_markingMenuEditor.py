import sys, hou, os
#on work machines use this line
from PySide2 import QtWidgets, QtGui, QtCore, QtTest

class NE_MarkingMenuEditor(QtWidgets.QWidget):    
    def __init__(self):
        super(NE_MarkingMenuEditor, self).__init__()
        
        self.initUI()
        
    def initUI(self):    
        self.setParent(hou.qt.mainWindow(), QtCore.Qt.Window)
        #self.setWindowFlags(self.windowFlags() | QtCore.Qt.FramelessWindowHint)
        #self.setAttribute(QtCore.Qt.WA_TranslucentBackground)        
        self.setWindowTitle('Marking Menu Editor')
        self.setGeometry(300,300, 900, 700)
        self.setStyleSheet('background-color: rgb(58,58,58);')
        self.setMinimumSize(900, 700)

        self.vlayout0 = QtWidgets.QVBoxLayout()
        self.setLayout(self.vlayout0)

        self.treeWidget = QtWidgets.QTreeWidget(self)
        self.treeWidget.setColumnCount(1)
        self.treeWidget.setHeaderLabel('Marking Menu Overview')
        self.vlayout0.addWidget(self.treeWidget)
        items = []
        for i in range(10):
            x = QtWidgets.QTreeWidgetItem(self.treeWidget)
            x.setText(0, 'item: %d' % i)

        #print items
        #self.treeWidget.addTopLevelItems(items)
        self.run()

    def loadCollections(self):        
        dirpath = hou.getenv('HOUDINI_USER_PREF_DIR')+'/python2.7libs/ne_mm_libs/collections'
        self.collections = [a for a in os.listdir(dirpath) if a.endswith('.collection')]

    def closeEvent(self, e):
        self.setParent(None)
        self.deleteLater()        
             
    def run(self):
        self.show()        
        

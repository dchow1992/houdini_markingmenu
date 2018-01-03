import sys, hou, os, json
#on work machines use this line
from PySide import QtGui, QtCore, QtTest
#from PySide2 import QtGui, QtGui, QtCore, QtTest

class cbStatus(QtCore.QObject):
    checked = QtCore.Signal()
    unchecked = QtCore.Signal()

class NE_MarkingMenuEditor(QtGui.QWidget):    
    def __init__(self):
        super(NE_MarkingMenuEditor, self).__init__()
        
        self.collections = []
        self.collectionsDir = hou.getenv('HOUDINI_USER_PREF_DIR')+'/python2.7libs/ne_mm_libs/collections/'
        
        #get names of collections on disk
        self.updateCollections()
        self.initUI()
        
    def initUI(self):    
        self.setParent(hou.qt.mainWindow(), QtCore.Qt.Window)
        #self.setWindowFlags(self.windowFlags() | QtCore.Qt.FramelessWindowHint)
        #self.setAttribute(QtCore.Qt.WA_TranslucentBackground)        
        self.setWindowTitle('Marking Menu Editor')
        self.setGeometry(300,300, 900, 700)
        self.setStyleSheet('background-color: rgb(58,58,58);')
        self.setMinimumSize(1200, 700)
        
        #root layout
        self.vlayout0 = QtGui.QVBoxLayout()
        self.setLayout(self.vlayout0)

        #collection combo box
        self.collectComboUI()
        
        #separator
        self.vlayout0.addSpacing(10)
        
        #collection tree widget
        self.treeWidgetUI()
        
        #separator
        self.vlayout0.addSpacing(10)
        
        #collection buttons
        self.glayout0 = QtGui.QGridLayout()
        self.glayout0.setSpacing(10)
        self.vlayout0.addLayout(self.glayout0)
        
        #row labels
        self.activeCheckWidgets = []
        self.menuCheckWidgets = []
        self.labelInputWidgets = []
        self.iconInputWidgets = []
        self.collectComboWidgets = []
        self.commandComboWidgets = []
        self.nodeInputWidgets = []
        self.activeWireCheckWidgets = []
        
        #all enabled checkbox
        self.allEnabledWidget = hou.qt.createCheckBox()
        self.glayout0.addWidget(self.allEnabledWidget, 0, 0, 1, 1)
        self.allEnabledWidget.stateChanged.connect(self.allEnabled)
        
        #all menu checkbox
        self.allMenuWidget = hou.qt.createCheckBox()
        self.glayout0.addWidget(self.allMenuWidget, 0, 1, 1, 1)
        self.allMenuWidget.stateChanged.connect(self.allMenus)
        
        #all active wire on create checkbox
        self.allActiveWireWidget = hou.qt.createCheckBox()
        self.glayout0.addWidget(self.allActiveWireWidget, 0, 8, 1, 1)
        self.allActiveWireWidget.stateChanged.connect(self.allActiveWires)
        
        #for each button (8 max per collection)
        for i in range(8):       
            #enabled checkboxes
            h = hou.qt.createCheckBox()
            h.setText('Item %d' % i)    
            h.setCheckState(QtCore.Qt.CheckState.Checked)
            self.activeCheckWidgets.append(h)           
            self.glayout0.addWidget(h, i+1, 0, 1, 1)            
            
            #is menu checkboxes
            a = hou.qt.createCheckBox()            
            a.setText('Menu')
            self.menuCheckWidgets.append(a)
            self.glayout0.addWidget(a, i+1, 1, 1, 1)
            #a.stateChanged.connect(self.hideCollectCombo)
            
            #label line edits
            a = QtGui.QLineEdit()
            a.setPlaceholderText('Label')
            self.labelInputWidgets.append(a)
            self.glayout0.addWidget(a, i+1, 2, 1, 1)
            
            #icon line edits
            a = QtGui.QLineEdit()
            a.setPlaceholderText('Icon - for example: MISC_python')
            self.iconInputWidgets.append(a)
            self.glayout0.addWidget(a, i+1, 3, 1, 1)
            
            #point to collection if menu combo boxes
            a = QtGui.QComboBox()
            a.insertItem(0, 'Set Collection')
            a.insertItems(1, [x for x in self.collections if x != self.collectCombo.currentText()])
            self.collectComboWidgets.append(a)
            self.glayout0.addWidget(a, i+1, 4, 1, 1)
            
            #command labels
            a = QtGui.QLabel('Command: ')
            self.glayout0.addWidget(a, i+1, 5, 1, 1)
            
            #command type combo boxes
            a = QtGui.QComboBox()
            a.insertItem(0, 'Command Type')
            a.insertItems(1, ['Create Node', 'Custom Function'])
            self.commandComboWidgets.append(a)
            self.glayout0.addWidget(a, i+1, 6, 1, 1)
            
            #nodename or custom command function line edits
            a = QtGui.QLineEdit()
            a.setPlaceholderText('nodename')
            self.nodeInputWidgets.append(a)
            self.glayout0.addWidget(a, i+1, 7, 1, 1)
            
            #active wire checkboxes
            a = hou.qt.createCheckBox()            
            a.setText('Active Wire On Create')
            self.activeWireCheckWidgets.append(a)
            self.glayout0.addWidget(a, i+1, 8, 1, 1)
            h.stateChanged.connect(a.setDisabled)
            
        self.run()
        
    def collectComboUI(self):
        #collections combo box
        self.hlayout0 = QtGui.QHBoxLayout()
        self.hlayout0.setSpacing(0)
        self.vlayout0.addLayout(self.hlayout0)
        
        self.collectComboLabel = QtGui.QLabel('Active Collection: ', self)
        self.collectComboLabel.setAlignment(QtCore.Qt.AlignLeft)
        self.collectCombo = QtGui.QComboBox(self)
        self.collectCombo.setMinimumContentsLength(35)
        
        defaultCollection = 'SOP_baseCollection.collection'
        
        #move baseCollections to top of list and brighten
        self.collections.insert(0, self.collections.pop(self.collections.index('SOP_baseCollection.collection'))) 
        self.collectCombo.insertItems(0, self.collections)
        self.collectCombo.setCurrentIndex(self.collections.index(defaultCollection))        
        brush = QtGui.QBrush()
        brush.setColor(QtGui.QColor(255, 255, 255))
        self.collectCombo.setItemData(0, brush, QtCore.Qt.ForegroundRole)
        
        #connect functions
        self.collectCombo.currentIndexChanged.connect(self.selectCollection)
        
        self.hlayout0.addWidget(self.collectComboLabel)
        self.hlayout0.addSpacing(10)
        self.hlayout0.addWidget(self.collectCombo)
        self.hlayout0.addStretch(1)
        
    def treeWidgetUI(self):
        #tree view init
        self.treeWidget = QtGui.QTreeWidget(self)
        self.treeWidget.setColumnCount(1)
        self.treeWidget.setHeaderLabel('Marking Menu Collection Overview')   
        self.treeWidget.setItemsExpandable(False)
        self.treeWidget.setStyleSheet('QTreeView::branch:open { image: url(none.png); } ')        
        self.vlayout0.addWidget(self.treeWidget)               
        
        self.updateTree(self.treeWidget, 'SOP_baseCollection.collection') 
        
        
        
    def selectCollection(self):        
        self.updateTree(self.treeWidget, self.collectCombo.currentText())
        
    def allEnabled(self):
        for cb in self.activeCheckWidgets:            
            cb.setCheckState(self.allEnabledWidget.checkState())
            
    def allMenus(self):
        for cb in self.menuCheckWidgets:
            if cb.isEnabled():
                cb.setCheckState(self.allMenuWidget.checkState())
            
    def allActiveWires(self):
        for cb in self.activeWireCheckWidgets:            
            if cb.isEnabled():
                cb.setCheckState(self.allActiveWireWidget.checkState())
    
    def updateTree(self, parentItem, collectionFile):
        #load collection from disk, build parent item, populate item
        loaded = self.loadCollection(collectionFile)
        
        self.treeWidget.clear()
        
        collectionHeader = QtGui.QTreeWidgetItem(parentItem) 
        collectionHeader.setText(0, collectionFile.split('.collection')[0]) 
        collectionHeader.setExpanded(True)
        collectionHeader.setIcon(0, hou.qt.createIcon('SOP_object_merge'))

        brush = QtGui.QBrush()
        brush.setColor(QtGui.QColor(255, 178, 45))
        collectionHeader.setForeground(0, brush)
        
        for i in range(len(loaded)):
            item = loaded['menuItem%d'%i]
            idx = item['index']    
            
            x = QtGui.QTreeWidgetItem(collectionHeader)
            
            x.setIcon(0, hou.qt.createIcon(item['icon']))
            
            x.setText(0, item['label'])            
            x.setExpanded(True)
            
            brush.setColor(QtGui.QColor(203, 203, 203))            
            x.setForeground(0, brush)
            
            if item['isMenu']:
                brush.setColor(QtGui.QColor(153, 255, 45))
                x.setForeground(0, brush)                
                
                if item['menuCollection'] == '':
                    y = QtGui.QTreeWidgetItem(x)
                    y.setText(0, 'Empty Menu')
                    y.setIcon(0, hou.qt.createIcon('SOP_delete'))
    
                    brush.setColor(QtGui.QColor(153, 153, 153))
                    y.setForeground(0, brush)
                    y.setExpanded(True)

        
    def updateCollections(self):
        #set class variable to a list of .collection files found in collectionsDir
        self.collections = [a for a in os.listdir(self.collectionsDir) if a.endswith('.collection')]
        
    def loadCollection(self, collection):
        #return dictionary from json collection
        with open(self.collectionsDir + collection, 'r') as f:
            return json.load(f)

    def closeEvent(self, e):
        self.setParent(None)
        self.deleteLater()        
             
    def run(self):
        self.show()
        
        
        
        
        
        
        
        
        
        
        
        
        
print hou.qt.styleSheet()
for entry in QtGui.qApp.allWidgets():
    if type(entry).__name__ == 'NE_MarkingMenuEditor':
        entry.close()
        
ex = NE_MarkingMenuEditor()

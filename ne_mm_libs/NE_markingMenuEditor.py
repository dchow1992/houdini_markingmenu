import sys, hou, os, json
#on work machines use this line
from PySide2 import QtWidgets, QtGui, QtCore, QtTest
#from PySide2 import QtWidgets, QtWidgets, QtCore, QtTest

class NE_MarkingMenuEditor(QtWidgets.QWidget):    
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
        self.setMinimumSize(1400, 700)
        
        #root layout
        self.vlayout0 = QtWidgets.QVBoxLayout()
        self.setLayout(self.vlayout0)

        #collection combo box
        self.collectComboUI()
        
        #spacer
        self.vlayout0.addSpacing(10)
        
        #collection tree widget
        self.treeWidgetUI()
        
        #spacer
        self.vlayout0.addSpacing(10)
        
        #details pane
        self.detailsUI()

        #draw default collection, SOP_baseCollection.collection in this case
        self.updateTree(self.treeWidget, 'SOP_baseCollection.collection')

        self.run()
        
    def detailsUI(self):
        #collection buttons
        self.glayout0 = QtWidgets.QGridLayout()
        self.glayout0.setSpacing(10)
        self.vlayout0.addLayout(self.glayout0)

        #row labels
        self.activeCheckWidgets = []
        self.menuCheckWidgets = []
        self.labelInputWidgets = []
        self.iconInputWidgets = []
        self.collectComboWidgets = []
        self.commandLabelWidgets = []
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

        #separator
        self.detailSeparatorWidget = hou.qt.createSeparator()
        self.detailSeparatorWidget.setStyleSheet(hou.qt.styleSheet())
        self.glayout0.addWidget(self.detailSeparatorWidget,1,0, 1, 10)

        #header labels
        labels = ['ITEM LABEL', 'ICON', 'MENU COLLECTION', 'BUTTON FUNC','BUTTON ARG']
        labelcolumns = [2, 3, 4, 6, 7]
        for x in labels:
            label = QtWidgets.QLabel(x)
            font = QtGui.QFont()
            font.setBold(True)
            label.setFont(font)        
            self.glayout0.addWidget(label, 0, labelcolumns[labels.index(x)], 1, 1)

        #for each button (8 max per collection)
        for i in range(2, 8+2):       
            #enabled checkboxes
            h = hou.qt.createCheckBox()
            h.setText('Item %d' % (i-2))    
            h.setCheckState(QtCore.Qt.CheckState.Checked)
            self.activeCheckWidgets.append(h)           
            self.glayout0.addWidget(h, i, 0, 1, 1)            
            h.stateChanged.connect(self.updateDetailsUI)

            #is menu checkboxes
            a = hou.qt.createCheckBox()            
            a.setText('Menu')
            self.menuCheckWidgets.append(a)
            self.glayout0.addWidget(a, i, 1, 1, 1)            
            a.stateChanged.connect(self.updateMenuDetailWidgets)

            #label line edits
            a = QtWidgets.QLineEdit()
            a.setPlaceholderText('Label')
            self.labelInputWidgets.append(a)
            self.glayout0.addWidget(a, i, 2, 1, 1)
            
            #icon line edits
            a = QtWidgets.QLineEdit()
            a.setPlaceholderText('Icon - ex: MISC_python')
            self.iconInputWidgets.append(a)
            self.glayout0.addWidget(a, i, 3, 1, 1)
            
            #point to collection if menu combo boxes
            a = QtWidgets.QComboBox()
            a.insertItem(0, 'Link Collection')
            a.insertItems(1, [x for x in self.collections if x != self.collectCombo.currentText()])
            a.setDisabled(True)
            self.collectComboWidgets.append(a)
            self.glayout0.addWidget(a, i, 4, 1, 1)
            
            #command labels
            a = QtWidgets.QLabel('Command: ')
            self.commandLabelWidgets.append(a)
            self.glayout0.addWidget(a, i, 5, 1, 1)
            
            #command type combo boxes
            a = QtWidgets.QComboBox()
            a.insertItem(0, 'Command Type')
            a.insertItems(1, ['Create Node', 'Custom Function'])
            self.commandComboWidgets.append(a)
            self.glayout0.addWidget(a, i, 6, 1, 1)
            a.currentIndexChanged.connect(self.toggleTextHint)
            a.currentIndexChanged.connect(self.disableActiveWire)

            #nodename or custom command function line edits
            a = QtWidgets.QLineEdit()
            a.setPlaceholderText('nodename')
            self.nodeInputWidgets.append(a)
            self.glayout0.addWidget(a, i, 7, 1, 1)
            
            #active wire checkboxes
            a = hou.qt.createCheckBox()            
            a.setText('Active Wire On Create')
            self.activeWireCheckWidgets.append(a)
            self.glayout0.addWidget(a, i, 8, 1, 1)
            
    def collectComboUI(self):
        #collections combo box
        self.hlayout0 = QtWidgets.QHBoxLayout()
        self.hlayout0.setSpacing(0)
        self.vlayout0.addLayout(self.hlayout0)
        
        self.collectComboLabel = QtWidgets.QLabel('Active Collection: ', self)
        self.collectComboLabel.setAlignment(QtCore.Qt.AlignLeft)
        self.collectCombo = QtWidgets.QComboBox(self)
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
        self.treeWidget = QtWidgets.QTreeWidget(self)
        self.treeWidget.setColumnCount(1)
        self.treeWidget.setHeaderLabel('Marking Menu Collection Overview')   
        self.treeWidget.setItemsExpandable(False)
        self.treeWidget.setStyleSheet('QTreeView::branch:open { image: url(none.png); } ')        
        self.vlayout0.addWidget(self.treeWidget) 

    def clearDetailRow(self, idx):
        #set a row to default values
        self.activeCheckWidgets[idx].setCheckState(QtCore.Qt.Unchecked)
        self.menuCheckWidgets[idx].setCheckState(QtCore.Qt.Unchecked)        
        self.labelInputWidgets[idx].clear()
        self.iconInputWidgets[idx].clear()
        self.collectComboWidgets[idx].setCurrentIndex(0)
        self.collectComboWidgets[idx].setDisabled(True)
        self.commandComboWidgets[idx].setCurrentIndex(0)
        self.nodeInputWidgets[idx].clear()
        self.activeWireCheckWidgets[idx].setCheckState(QtCore.Qt.Unchecked)

    def loadDetailsFromCollection(self, collection, idx):
        self.clearDetailRow(idx)        
        self.activeCheckWidgets[idx].setCheckState(QtCore.Qt.Checked)
        self.labelInputWidgets[idx].setText(collection['label'])
        self.iconInputWidgets[idx].setText(collection['icon'])

        if collection['isMenu']:
            self.menuCheckWidgets[idx].setCheckState(QtCore.Qt.Checked)

            0 if collection['menuCollection'] == '' else \
                 self.collectComboWidgets[idx].setCurrentText(self.collectComboWidgets[idx].findText(collection['menuCollection']))
        
        else:
            if collection['commandType'] == 'createnode':
                self.commandComboWidgets[idx].setCurrentIndex(1)
                self.nodeInputWidgets[idx].setText(collection['nodetype'])

            if collection['activeWire']:
                self.activeWireCheckWidgets[idx].setCheckState(QtCore.Qt.Checked)

            elif collection['command'] == '' and collection['commandType'] != 'createnode':
                self.commandComboWidgets[idx].setCurrentIndex(0)

            elif collection['command'] != '' and collection['commandType'] != 'createnode':
                self.commandComboWidgets[idx].setCurrentIndex(2)
                self.nodeInputWidgets[idx].setText(collection['command'])

    
    def updateDetailsUI(self):
        for cb in self.activeCheckWidgets:
            idx = self.activeCheckWidgets.index(cb)
            if cb.checkState() != QtCore.Qt.Checked:
                cb.setTextColor(QtGui.QColor(131, 131, 131))
                self.menuCheckWidgets[idx].setDisabled(True)
                self.labelInputWidgets[idx].setDisabled(True)
                self.iconInputWidgets[idx].setDisabled(True)
                self.collectComboWidgets[idx].setDisabled(True)
                self.commandLabelWidgets[idx].setDisabled(True)
                self.commandComboWidgets[idx].setDisabled(True)
                self.nodeInputWidgets[idx].setDisabled(True)
                self.activeWireCheckWidgets[idx].setDisabled(True)
            else:
                cb.setTextColor(QtGui.QColor(203, 203, 203))
                self.menuCheckWidgets[idx].setDisabled(False)
                self.labelInputWidgets[idx].setDisabled(False)
                self.iconInputWidgets[idx].setDisabled(False)                
                self.collectComboWidgets[idx].setDisabled(False)
                self.commandLabelWidgets[idx].setDisabled(False)
                self.commandComboWidgets[idx].setDisabled(False)
                self.nodeInputWidgets[idx].setDisabled(False)
                self.activeWireCheckWidgets[idx].setDisabled(False)
        self.updateMenuDetailWidgets()

    def updateMenuDetailWidgets(self):
        for cb in self.menuCheckWidgets:
            idx = self.menuCheckWidgets.index(cb)            
            if cb.checkState() != QtCore.Qt.Checked and cb.isEnabled():
                self.collectComboWidgets[idx].setDisabled(True)
                self.commandLabelWidgets[idx].setDisabled(False)
                self.commandComboWidgets[idx].setDisabled(False)
                self.nodeInputWidgets[idx].setDisabled(False)
                self.activeWireCheckWidgets[idx].setDisabled(False)

            elif cb.isEnabled() and cb.checkState() == QtCore.Qt.Checked:
                self.collectComboWidgets[idx].setDisabled(False)
                self.commandLabelWidgets[idx].setDisabled(True)
                self.commandComboWidgets[idx].setDisabled(True)
                self.nodeInputWidgets[idx].setDisabled(True)
                self.activeWireCheckWidgets[idx].setDisabled(True)

    def toggleTextHint(self):
        for cb in self.commandComboWidgets:
            idx = self.commandComboWidgets.index(cb)
            if cb.currentIndex() == 2:
                self.nodeInputWidgets[idx].setPlaceholderText('function()')
            else:
                self.nodeInputWidgets[idx].setPlaceholderText('nodename')

    def disableActiveWire(self):
        for cb in self.commandComboWidgets:
            idx = self.commandComboWidgets.index(cb)
            if cb.isEnabled() and cb.currentIndex() == 1:
                self.activeWireCheckWidgets[idx].setDisabled(False) 
            else:
                self.activeWireCheckWidgets[idx].setDisabled(True)

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
        
        #parent collection item
        collectionHeader = QtWidgets.QTreeWidgetItem(parentItem) 
        collectionHeader.setText(0, collectionFile.split('.collection')[0]) 
        collectionHeader.setExpanded(True)
        collectionHeader.setIcon(0, hou.qt.createIcon('SOP_object_merge'))

        brush = QtGui.QBrush()
        brush.setColor(QtGui.QColor(255, 178, 45))
        collectionHeader.setForeground(0, brush)
        
        #for each dict in current collection
        for i in range(len(loaded)):            
            item = loaded['menuItem%d'%i]
            
            #if item isn't empty
            if item != None:
                idx = item['index']
            
                #tree display button label
                x = QtWidgets.QTreeWidgetItem(collectionHeader)                
                x.setIcon(0, hou.qt.createIcon(item['icon']))                
                x.setText(0, '%d'%i + '. ' + item['label'])            
                x.setExpanded(True)                
                brush.setColor(QtGui.QColor(203, 203, 203))            
                x.setForeground(0, brush)

                self.loadDetailsFromCollection(item, idx)

                if item['isMenu']:
                    brush.setColor(QtGui.QColor(153, 255, 45))
                    x.setForeground(0, brush)                
                    
                    if item['menuCollection'] == '':
                        y = QtWidgets.QTreeWidgetItem(x)
                        y.setText(0, 'No Collection Linked')
                        y.setIcon(0, hou.qt.createIcon('SOP_delete'))
        
                        brush.setColor(QtGui.QColor(153, 153, 153))
                        y.setForeground(0, brush)
                        y.setExpanded(True)

            else:
                #add empty tree item
                x = QtWidgets.QTreeWidgetItem(collectionHeader)                
                x.setText(0, '%d'%i + '. ' + 'empty')            
                x.setExpanded(True)                
                brush.setColor(QtGui.QColor(120, 120, 120))            
                x.setForeground(0, brush)

                #empty detail row
                self.clearDetailRow(i)

        
      
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
        
        
        
        
        
        
        
        
        
        
        
        
        
#print hou.qt.styleSheet()
for entry in QtWidgets.qApp.allWidgets():
    if type(entry).__name__ == 'NE_MarkingMenuEditor':
        entry.close()
        
#ex = NE_MarkingMenuEditor()
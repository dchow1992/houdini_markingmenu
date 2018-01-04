import sys, hou, os, json
#on work machines use this line
from PySide2 import QtWidgets, QtGui, QtCore, QtTest
#from PySide2 import QtWidgets, QtWidgets, QtCore, QtTest
class itemConfig:
    def __init__(self, context, isMenu, nodetype, label, icon, index, activeWire, collection, commandType, command):
        self.nodetype = nodetype
        self.label = label
        self.icon = icon
        self.index = index
        self.activeWire = activeWire
        self.defaultcommand = 'cmds.createNode("%s", %s)' % (self.nodetype, self.activeWire)
        self.config = {
            'context':context,
            'isMenu': isMenu,
            'label': self.label,
            'icon': self.icon,
            'index': self.index,
            'menuCollection': collection,
            'nodetype': self.nodetype,
            'commandType': commandType,
            'activeWire': self.activeWire,
            'command': self.defaultcommand if commandType == 'createnode' else command
        }

class NE_MarkingMenuEditor(QtWidgets.QWidget):
    def __init__(self):
        super(NE_MarkingMenuEditor, self).__init__()

        self.collections = []
        self.collectionsDir = hou.getenv('HOUDINI_USER_PREF_DIR')+'/python2.7libs/ne_mm_libs/collections/'

        for entry in QtWidgets.qApp.allWidgets():
            if type(entry).__name__ == 'NE_MarkingMenuEditor':
                print 'found an editor'

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
        self.setMinimumSize(1200, 850)

        #root layout
        self.vlayout0 = QtWidgets.QVBoxLayout()
        self.setLayout(self.vlayout0)

        #collection combo box
        self.collectComboUI()

        #spacer
        self.vlayout0.addSpacing(10)
        
        #collection tree widget
        self.hlayout0 = QtWidgets.QHBoxLayout()
        self.vlayout0.addLayout(self.hlayout0)

        self.treeWidgetUI()
        self.hlayout0.addWidget(self.treeWidget)
        self.hlayout0.addStretch(1)
        
        self.glayout1 = QtWidgets.QGridLayout()
        self.glayout1.setSpacing(10)
        self.hlayout0.addLayout(self.glayout1)

        self.btn0 = QtWidgets.QPushButton('Item Slot 0', self)
        self.btn0.setStyleSheet(hou.qt.styleSheet())
        self.btn0.setFixedSize(110,24)
        self.glayout1.addWidget(self.btn0, 0, 4, 1, 1)

        self.btn1 = QtWidgets.QPushButton('Item Slot 1', self)
        self.btn1.setStyleSheet(hou.qt.styleSheet())
        self.btn1.setFixedSize(110,24)
        self.glayout1.addWidget(self.btn1, 1, 4, 1, 1)

        self.btn2 = QtWidgets.QPushButton('Item Slot 2', self)
        self.btn2.setStyleSheet(hou.qt.styleSheet())
        self.btn2.setFixedSize(110,24)
        self.glayout1.addWidget(self.btn2, 2, 4, 1, 1)

        self.btn3 = QtWidgets.QPushButton('Item Slot 3', self)
        self.btn3.setStyleSheet(hou.qt.styleSheet())
        self.btn3.setFixedSize(110,24)
        self.glayout1.addWidget(self.btn3, 3, 4, 1, 1)

        self.btn4 = QtWidgets.QPushButton('Item Slot 4', self)
        self.btn4.setStyleSheet(hou.qt.styleSheet())
        self.btn4.setFixedSize(110,24)
        self.glayout1.addWidget(self.btn4, 4, 4, 1, 1)

        self.hlayout0.addStretch(1)

        #spacer
        self.vlayout0.addSpacing(10)

        #details pane
        self.detailsUI()

        #separator
        self.saveSeparatorWidget = hou.qt.createSeparator()
        self.vlayout0.addWidget(self.saveSeparatorWidget)

        #save close buttons
        self.saveCloseUI()

        #draw default collection, SOP_baseCollection.collection in this case
        self.updateTree(self.treeWidget, 'SOP_baseCollection.collection')

        self.run()

    def saveCloseUI(self):
        self.hlayout2 = QtWidgets.QHBoxLayout()
        self.vlayout0.addLayout(self.hlayout2)

        self.hlayout2.addStretch(1)

        self.saveTextWidget = QtWidgets.QLabel()
        #font = QtGui.QFont()
        #font.setBold(True)
        #self.saveTextWidget.setFont(font)
        self.saveTextWidget.setStyleSheet('font: 18pt;')

        self.hlayout2.addWidget(self.saveTextWidget)
        self.hlayout2.addStretch(1)

        self.saveButtonWidget = QtWidgets.QPushButton('Save Collection')
        self.closeButtonWidget = QtWidgets.QPushButton('Close')

        self.saveButtonWidget.setMinimumSize(220, 70)
        self.closeButtonWidget.setMinimumSize(220, 70)

        self.saveButtonWidget.setStyleSheet(hou.qt.styleSheet())
        self.closeButtonWidget.setStyleSheet(hou.qt.styleSheet())

        self.saveButtonWidget.clicked.connect(lambda: self.alertText('Successfully Saved %s...' % self.collectCombo.currentText()))
        self.saveButtonWidget.clicked.connect(lambda: self.jsonFromDetails(self.collectCombo.currentText()))

        self.closeButtonWidget.clicked.connect(self.close)

        self.hlayout2.addWidget(self.saveButtonWidget)
        self.hlayout2.addWidget(self.closeButtonWidget)

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
        labels = ['ITEM LABEL', 'ICON', '  MENU COLLECTION', '  FUNCTION TYPE','  BUTTON ARG']
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
            #a.setStyleSheet('selection-background-color: rgb(25,25,25);')
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
        self.hlayout1 = QtWidgets.QHBoxLayout()
        self.hlayout1.setSpacing(0)
        self.vlayout0.addLayout(self.hlayout1)

        #reload current collection widget
        self.reloadCollectionWidget = QtWidgets.QPushButton('Reload Collection')
        self.reloadCollectionWidget.setIcon(hou.qt.createIcon('BUTTONS_cook'))

        self.collectCombo = QtWidgets.QComboBox(self)
        self.collectCombo.setMinimumContentsLength(35)

        self.defaultCollection = 'SOP_baseCollection.collection'
        self.loadCollectionComboUI()
        
        #new / delete / rename collection buttons
        self.newCollectionWidget = QtWidgets.QPushButton('New Collection')
        self.delCollectionWidget = QtWidgets.QPushButton('Delete Collection')
        self.renameCollectionWidget = QtWidgets.QPushButton('Rename Collection')

        self.newCollectionWidget.setStyleSheet(hou.qt.styleSheet())
        self.delCollectionWidget.setStyleSheet(hou.qt.styleSheet())
        self.renameCollectionWidget.setStyleSheet(hou.qt.styleSheet())

        #connect functions
        self.collectCombo.currentIndexChanged.connect(self.drawCurrentCollection)
        self.reloadCollectionWidget.clicked.connect(self.drawCurrentCollection)
        self.newCollectionWidget.clicked.connect(self.newCollection)
        self.delCollectionWidget.clicked.connect(self.deleteCollection)
        self.renameCollectionWidget.clicked.connect(self.renameCollection)

        #layout widgets        
        self.hlayout1.addWidget(self.reloadCollectionWidget)

        self.hlayout1.addSpacing(10)

        self.hlayout1.addWidget(self.collectCombo)

        self.hlayout1.addSpacing(10)
        
        self.hlayout1.addWidget(self.newCollectionWidget)

        self.hlayout1.addSpacing(10)

        self.hlayout1.addWidget(self.delCollectionWidget)

        self.hlayout1.addSpacing(10)

        self.hlayout1.addWidget(self.renameCollectionWidget)

        self.hlayout1.addStretch(1)

    def loadCollectionComboUI(self):
        #move baseCollections to top of list
        self.collections.insert(0, self.collections.pop(self.collections.index(self.defaultCollection)))

        #get list of current items
        currentMenuStrings = []
        for i in range(self.collectCombo.count()):
            currentMenuStrings.append(self.collectCombo.itemText(i).encode('utf-8'))

        #find new items to add
        newitems = list(set(self.collections) - set(currentMenuStrings))

        #delete items that don't appear on disk
        for i in range(self.collectCombo.count()):
            if self.collectCombo.itemText(i).encode('utf-8') not in self.collections:
                self.collectCombo.removeItem(i)

        #add new items
        for item in newitems:
            self.collectCombo.insertItem(self.collectCombo.count()-1, item)


        self.collectCombo.setCurrentIndex(self.collectCombo.findText((self.defaultCollection)))
        self.collectCombo.setStyleSheet('''
                                        color: white;
                                    ''')
        abr = QtGui.QBrush()
        abr.setColor(QtGui.QColor(255, 0, 0, 255))

        for i in range(self.collectCombo.count()):
            None
            #self.collectCombo.setItemData(i, abr, QtCore.Qt.ForegroundRole)
            #self.collectCombo.setItemData(i,QtGui.QColor(25,25,25),QtCore.Qt.BackgroundColorRole)
            #self.collectCombo.setStyleSheet('selection-background-color: rgb(25,25,25); color: rgb(255,255,255);')

    def treeWidgetUI(self):
        #tree view init
        self.treeWidget = QtWidgets.QTreeWidget(self)
        self.treeWidget.setColumnCount(1)
        self.treeWidget.setHeaderLabel('Marking Menu Collection Overview')
        self.treeWidget.setItemsExpandable(False)
        self.treeWidget.setMinimumSize(500,0)
        self.treeWidget.setMaximumSize(500, 99999)
        self.treeWidget.setStyleSheet('QTreeView::branch:open { image: url(none.png); } ')

    def refreshLinkMenus(self, widgets):
        for a in widgets:
            a.clear()
            a.insertItem(0, 'Link Collection')
            a.insertItems(1, [x for x in self.collections if x != a.currentText()])

    def newCollection(self):
        x = self.collectCombo.currentText()
        diag = hou.ui.readInput('New Collection', buttons=('Create', 'Cancel'), close_choice=1, \
                                help='Context will be added as prefix', title='Create Collection', initial_contents='newCollectionName')
        if diag[1] != '' and diag[0] == 0:
            a = diag[1]
            if a.endswith('.collection'):
                a = a.split('.collection')[0]

            newname = x.split('_')[0] + '_' + a + '.collection'
            newname = newname.encode('utf-8')

            for i in range(8):
                self.clearDetailRow(i)

            self.jsonFromDetails(newname)
            self.collections.append(newname)
            self.loadCollectionComboUI()
            self.collectCombo.setCurrentIndex(self.collectCombo.findText(newname))
            self.refreshLinkMenus(self.collectComboWidgets)
            self.alertText('Created: %s'%newname)

    def deleteCollection(self):
        x = self.collectCombo.currentText()
        if not x.split('.collection')[0].endswith('baseCollection'):
            a = hou.ui.displayMessage('Delete Collection: %s\nAre you sure?'%x, buttons=('Yes', 'No'), close_choice=1)
            if a == 0:
                os.remove(self.collectionsDir+x)
                self.updateCollections()
                self.loadCollectionComboUI()
                self.drawCurrentCollection()
                self.refreshLinkMenus(self.collectComboWidgets)
                self.alertText('Deleted: %s'%x)
        else:
            hou.ui.displayMessage('Base Collections cannot be deleted', severity=hou.severityType.Warning, buttons=('OK',))

    def renameCollection(self):
        x = self.collectCombo.currentText()
        if not x.split('.collection')[0].endswith('baseCollection'):
            diag = hou.ui.readInput('Rename Collection', buttons=('Save', 'Cancel'), close_choice=1, \
                                    help='Context will be added as prefix', title='Rename', initial_contents='newCollectionName')

            if diag[1] != '' and diag[0] == 0:
                a = diag[1]
                if a.endswith('.collection'):
                    a = a.split('.collection')[0]

                newname = x.split('_')[0] + '_' + a + '.collection'
                contexts = ['SOP', 'OBJ', 'DOP', 'VOP', 'SHOP', 'MAT', 'CHOP', 'COP']
                doRename = True
                for c in contexts:
                    if newname == c+'_baseCollection.collection':
                        hou.ui.displayMessage('Base Collections cannot be overwritten', severity=hou.severityType.Warning, buttons=('OK',))
                        doRename = False
                        break                
                if doRename:
                    for c in self.collections:
                        if newname == c:
                            doRename = not hou.ui.displayMessage('A Collection already exists with this name\n' + \
                                                            'Do you want to overwrite it?', buttons=('Yes', 'No'), close_choice=1)
                if doRename:
                    os.remove(self.collectionsDir + newname)
                    os.rename(self.collectionsDir+x, self.collectionsDir + newname)
                    self.collectCombo.removeItem(self.collectCombo.currentIndex())
                    self.updateCollections()
                    self.loadCollectionComboUI()
                    self.drawCurrentCollection()
                    self.collectCombo.setCurrentIndex(self.collectCombo.findText(newname))
                    self.refreshLinkMenus(self.collectComboWidgets)
                    self.alertText('Renamed %s to: %s...'%(x.split('.collection')[0], newname.split('collection')[0]))

        else:
            hou.ui.displayMessage('Base Collections cannot be renamed', severity=hou.severityType.Warning, buttons=('OK',))

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

    def alertText(self, displayText):
        #fade the save text alert
        self.timer = QtCore.QTimer()
        self.textOpac = 1.25
        self.timer.timeout.connect(self.fadeText)
        self.timer.start(50)
        self.saveTextWidget.setText(displayText)

    def jsonFromDetails(self, filename):
        #filename = self.collectCombo.currentText()
        jsonDict = {}
        for i in range(8):
            active = True if self.activeCheckWidgets[i].checkState() == QtCore.Qt.Checked else False
            x = None
            if active:
                context = self.collectCombo.currentText().split('_')[0]
                isMenu = True if self.menuCheckWidgets[i].checkState() == QtCore.Qt.Checked else False
                nodetype = 'null' if self.nodeInputWidgets[i].text() == '' else self.nodeInputWidgets[i].text()
                label = self.labelInputWidgets[i].text()
                icon = 'MISC_python' if self.iconInputWidgets[i].text() == '' else self.iconInputWidgets[i].text()
                index = i
                activeWire = True if self.activeWireCheckWidgets[i].checkState() == QtCore.Qt.Checked else False
                menuCollection = self.collectComboWidgets[i].currentText() if self.collectComboWidgets[i].currentIndex() != 0 else ''
                command = self.nodeInputWidgets[i].text()
                commandType = 'createnode'

                #check for valid json
                iconsjson = self.collectionsDir.split('collections/')[0] + 'houdini_icons.json'
                iconsDict = {}
                validIcon = False

                with open(iconsjson, 'r') as f:
                    iconsDict = json.load(f)
                for a in iconsDict.values():                    
                    if icon in a:
                        validIcon = True
                        break

                icon = 'MISC_python' if validIcon == False else icon

                if self.commandComboWidgets[i].currentIndex() == 0:
                    commandType = 'None'                    

                if self.commandComboWidgets[i].currentIndex() == 2:
                    commandType = 'customFunction'
                    command = 'cmds.' + self.nodeInputWidgets[i].text()

                #itemConfig(context, isMenu, nodetype, label, icon, index, activeWire, collection, commandType, command)
                x = itemConfig(context, isMenu, nodetype, label, icon, index, activeWire, menuCollection, commandType, command).config

            jsonDict['collectionItem%d'%i] = x

        with open(self.collectionsDir + filename, 'w') as f:
            json.dump(jsonDict, f, indent=4, sort_keys=True)

        #reload saved collection and display
        self.drawCurrentCollection()        

    def fadeText(self):
        self.textOpac -= .015
        if self.textOpac <= 0:
            self.timer.stop()

        animval = min(max(255 * self.textOpac, 58), 255)
        self.saveTextWidget.setStyleSheet('''color: rgb(%d, %d, %d);
                                                font: 18pt;
                                            ''' % (animval, animval, animval))

    def loadDetailsFromCollection(self, collection, idx):
        self.clearDetailRow(idx)

        self.activeCheckWidgets[idx].setCheckState(QtCore.Qt.Checked)
        self.labelInputWidgets[idx].setText(collection['label'])
        self.iconInputWidgets[idx].setText(collection['icon'])

        if collection['isMenu']:
            self.menuCheckWidgets[idx].setCheckState(QtCore.Qt.Checked)

            if collection['menuCollection'] == '':
                self.collectComboWidgets[idx].setCurrentIndex(0)
            else:
                self.collectComboWidgets[idx].setCurrentIndex(self.collectComboWidgets[idx].findText(collection['menuCollection']))

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
                self.nodeInputWidgets[idx].setText(collection['command'].split('cmds.')[-1])

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

    def drawCurrentCollection(self):
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
            item = loaded['collectionItem%d'%i]

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

                    if item['menuCollection'] == '' or item['menuCollection'] not in self.collections:
                        y = QtWidgets.QTreeWidgetItem(x)
                        y.setText(0, 'No Collection Linked')
                        y.setIcon(0, hou.qt.createIcon('SOP_delete'))

                        brush.setColor(QtGui.QColor(153, 153, 153))
                        y.setForeground(0, brush)
                        y.setExpanded(True)
                    else:
                        z = QtWidgets.QTreeWidgetItem(x)
                        z.setText(0, item['menuCollection'])
                        z.setIcon(0, hou.qt.createIcon('SOP_object_merge'))
                        brush.setColor(QtGui.QColor(255, 178, 45))
                        z.setForeground(0, brush)
                        z.setExpanded(True)
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
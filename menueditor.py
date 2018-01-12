from PySide2 import QtWidgets, QtGui, QtCore, QtTest
import utils
reload(utils)
import hou
import os

class markingMenuEditor(QtWidgets.QWidget):
    def __init__(self):
        super(markingMenuEditor, self).__init__()
        self.setParent(hou.qt.mainWindow(), QtCore.Qt.Window)
        self.setWindowTitle('Marking Menu Editor')
        self.setGeometry(300,300, 900, 700)
        self.setStyleSheet('background-color: rgb(58,58,58);')
        self.setMinimumSize(1200, 850)
        
        self.rootpath = hou.getenv('HOUDINI_USER_PREF_DIR')+'/python2.7libs/nemarkingmenu/'        
        self.contexts = ['SOP', 'OBJ', 'DOP', 'VOP', 'ROP', 'SHOP', 'MAT', 'CHOP', 'COP']
        self.collections = []
        self.currentContext = 'SOP'
        self.collectionDir = self.rootpath + 'json/' + self.currentContext + '/'
        self.fullcpath = '' # full path to the current collection on disk
        self.menuPrefs = utils.loadMenuPreferences(self.rootpath + '/json/')
        self.detailIndices = []
        self.loadedCollection = []
        self.virtualCollection = []

        self.initUI()

    def initUI(self):        
        self.rootLayout = QtWidgets.QVBoxLayout()
        self.setLayout(self.rootLayout)

        self.manageCollectionsUI()

        self.rootLayout.addSpacing(10)

        self.modifierBaseCollectionsUI()

        self.mainUI = self.overviewUI()

        self.rootLayout.addSpacing(10)

        self.detailsUI = self.detailsUI()

        self.saveSeparatorWidget = hou.qt.createSeparator()
        self.rootLayout.addWidget(self.saveSeparatorWidget)

        self.saveCloseUI = self.saveCloseUI()

        # self.comboBoxDefaults()

        self.connectWidgetActions()

        # context combo box
        self.contextComboBox.insertItems(0, self.contexts)
        self.currentContext = self.contextComboBox.currentText()
        self.show()

    def manageCollectionsUI(self):
        #collections combo box
        primaryLayout = QtWidgets.QHBoxLayout()
        primaryLayout.setSpacing(0)
        self.rootLayout.addLayout(primaryLayout)
        
        self.reloadBtn = QtWidgets.QPushButton('Reload Collection')
        self.reloadBtn.setIcon(hou.qt.createIcon('BUTTONS_cook'))

        self.contextComboBox = QtWidgets.QComboBox(self)
        self.contextComboBox.setMinimumContentsLength(5)

        self.collectionComboBox = QtWidgets.QComboBox(self)
        self.collectionComboBox.setMinimumContentsLength(35)

        #new / delete / rename collection buttons
        self.newBtn = QtWidgets.QPushButton('New Collection')
        self.delBtn = QtWidgets.QPushButton('Delete Collection')
        self.renameBtn = QtWidgets.QPushButton('Rename Collection')

        self.newBtn.setStyleSheet(hou.qt.styleSheet())
        self.delBtn.setStyleSheet(hou.qt.styleSheet())
        self.renameBtn.setStyleSheet(hou.qt.styleSheet())

        '''
        #connect functions
        self.collectionComboBox.currentIndexChanged.connect(self.drawCurrentCollection)
        self.reloadBtn.clicked.connect(self.drawCurrentCollection)
        self.newBtn.clicked.connect(self.newCollection)
        self.delBtn.clicked.connect(self.deleteCollection)
        self.renameBtn.clicked.connect(self.renameCollection)'''

        #local layout
        primaryLayout.addWidget(self.reloadBtn)
        primaryLayout.addSpacing(10)
        primaryLayout.addWidget(self.contextComboBox)
        primaryLayout.addSpacing(10)
        primaryLayout.addWidget(self.collectionComboBox)
        primaryLayout.addSpacing(10)
        primaryLayout.addWidget(self.newBtn)
        primaryLayout.addSpacing(10)
        primaryLayout.addWidget(self.delBtn)
        primaryLayout.addSpacing(10)
        primaryLayout.addWidget(self.renameBtn)
        primaryLayout.addStretch(1)

    def modifierBaseCollectionsUI(self):
        h5 = QtWidgets.QHBoxLayout()
        h6 = QtWidgets.QHBoxLayout()
        primaryLayouts = [h5,h6]
        for layout in primaryLayouts:
            self.rootLayout.addLayout(layout)
        #self.vlayout0.addLayout(h5)
        #self.vlayout0.addLayout(h6)

        self.shiftLabel = QtWidgets.QLabel('SHIFT: Base Collection       ')
        self.shiftComboBox = QtWidgets.QComboBox()
        self.shiftComboBox.setMinimumSize(350, 0)
        h5.addWidget(self.shiftLabel)
        h5.addSpacing(5)
        h5.addWidget(self.shiftComboBox)
        h5.addStretch(1)

        self.ctrlLabel = QtWidgets.QLabel('CONTROL: Base Collection')
        self.ctrlComboBox = QtWidgets.QComboBox()
        self.ctrlComboBox.setMinimumSize(349, 0)
        h6.addWidget(self.ctrlLabel)
        h6.addSpacing(5)
        h6.addWidget(self.ctrlComboBox)
        h6.addStretch(1)

        #self.shiftComboBox.activated.connect(self.updatePreferences)
        #self.ctrlComboBox.activated.connect(self.updatePreferences)
        #self.reloadModifierMenus()  

    def overviewUI(self):
        primaryLayout = QtWidgets.QHBoxLayout()
        self.rootLayout.addLayout(primaryLayout)

        self.treeWidget = QtWidgets.QTreeWidget(self)
        self.treeWidget.setColumnCount(1)
        self.treeWidget.setHeaderLabel('Marking Menu Collection Overview')
        self.treeWidget.setItemsExpandable(False)
        self.treeWidget.setMinimumSize(500,0)
        self.treeWidget.setStyleSheet('QTreeView::branch:open { image: url(none.png); } ')

        primaryLayout.addWidget(self.treeWidget)
        primaryLayout.addStretch(1)

        refVLayout = QtWidgets.QVBoxLayout()
        primaryLayout.addLayout(refVLayout)

        refVLayout.addSpacing(80)

        refBtns = []
        
        h0 = QtWidgets.QHBoxLayout()
        refVLayout.addLayout(h0)
        btn0 = QtWidgets.QPushButton('Item Slot 0', self)        
        h0.addWidget(btn0)

        h1 = QtWidgets.QHBoxLayout()
        refVLayout.addLayout(h1)
        btn1 = QtWidgets.QPushButton('Item Slot 7', self)
        h1.addWidget(btn1)
        h1.addSpacing(60)

        h2 = QtWidgets.QHBoxLayout()
        refVLayout.addLayout(h2)
        btn2 = QtWidgets.QPushButton('Item Slot 6', self)
        h2.addWidget(btn2)
        
        h2.addSpacing(35)
        ref = QtWidgets.QLabel('REFERENCE')
        font = QtGui.QFont()
        font.setBold(True)
        ref.setFont(font)
        h2.addWidget(ref)
        h2.addSpacing(35)        

        h3 = QtWidgets.QHBoxLayout()
        refVLayout.addLayout(h3)
        btn3 = QtWidgets.QPushButton('Item Slot 5', self)
        h3.addWidget(btn3)
        h3.addSpacing(60)

        h4 = QtWidgets.QHBoxLayout()
        refVLayout.addLayout(h4)
        btn4 = QtWidgets.QPushButton('Item Slot 4', self)
        h4.addWidget(btn4)

        btn5 = QtWidgets.QPushButton('Item Slot 3', self)
        h3.addWidget(btn5)

        btn6 = QtWidgets.QPushButton('Item Slot 2', self)
        h2.addWidget(btn6)

        btn7 = QtWidgets.QPushButton('Item Slot 1', self)
        h1.addWidget(btn7)

        btns = [btn0, btn1, btn2, btn3, btn4, btn5, btn6, btn7]
        for b in btns:
            b.setStyleSheet("""
                   QPushButton {                
                                background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                                                            stop: 0.0 rgb(86, 86, 86), 
                                                            stop: 1.0 rgb(58, 58, 58));
                                border-top: 1px solid rgba(0, 0, 0, 40%);
                                border-right: 1px solid rgba(0, 0, 0, 40%);
                                border-bottom: 1px solid rgba(0, 0, 0, 62%);
                                border-left: 1px solid rgba(0, 0, 0, 40%);
                                border-radius: 1px;
                                color: rgb(203, 203, 203);
                                padding-top: 3px;
                                padding-right: 15px;
                                padding-bottom: 3px;
                                padding-left: 15px;
                                }
                    """) 
            b.setFixedSize(110,24)

        refVLayout.addSpacing(80)
        primaryLayout.addStretch(1)

    def detailsUI(self):
        primaryLayout = QtWidgets.QGridLayout()
        primaryLayout.setSpacing(10)        
        self.rootLayout.addLayout(primaryLayout)

        # arrays by widget
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
        primaryLayout.addWidget(self.allActiveToggle, 0, 1, 1, 1)
        #self.allActiveToggle.stateChanged.connect(self.allEnabled)

        # all menu checkbox
        self.allMenuToggle = hou.qt.createCheckBox()
        primaryLayout.addWidget(self.allMenuToggle, 0, 2, 1, 1)
        #self.allMenuToggle.stateChanged.connect(self.allMenus)

        # all active wire on create checkbox
        self.allWireToggle = hou.qt.createCheckBox()
        primaryLayout.addWidget(self.allWireToggle, 0, 9, 1, 1)
        #self.allWireToggle.stateChanged.connect(self.allActiveWires)

        # separator
        self.detailSeparatorWidget = hou.qt.createSeparator()
        self.detailSeparatorWidget.setStyleSheet(hou.qt.styleSheet())
        primaryLayout.addWidget(self.detailSeparatorWidget,1,0, 1, 10)

        # header labels
        labels = ['  INDEX', 'ITEM LABEL', 'ICON', '  MENU COLLECTION',
                  '  FUNCTION TYPE','  BUTTON ARG']

        labelcolumns = [0, 3, 4, 5, 7, 8]
        for label, col in zip(labels, labelcolumns):
            label = QtWidgets.QLabel(label)
            font = QtGui.QFont()
            font.setBold(True)
            label.setFont(font)
            primaryLayout.addWidget(label, 0, col, 1, 1)

        # for each button (8 max per collection)
        for i in range(2, 8+2):
            rowMenuWidgets = []
            rowButtonWidgets = []

            # index comboboxes
            a = QtWidgets.QComboBox()
            a.setMaximumSize(70,200)
            self.indexComboBoxes.append(a)
            primaryLayout.addWidget(a, i, 0, 1, 1)

            # enabled checkboxes
            h = hou.qt.createCheckBox()
            h.setText('Item %d' % (i-2))
            h.setCheckState(QtCore.Qt.CheckState.Checked)
            self.activeToggles.append(h)
            primaryLayout.addWidget(h, i, 1, 1, 1)
            #h.stateChanged.connect(self.updateDetailsUI)

            # is menu checkboxes
            a = hou.qt.createCheckBox()
            a.setText('Menu')
            self.menuToggles.append(a)
            primaryLayout.addWidget(a, i, 2, 1, 1)
            #a.stateChanged.connect(self.updateMenuDetailWidgets)

            # label line edits
            a = QtWidgets.QLineEdit()
            a.setPlaceholderText('Label')
            self.labelEdits.append(a)
            primaryLayout.addWidget(a, i, 3, 1, 1)

            # icon line edits
            a = QtWidgets.QLineEdit()
            a.setPlaceholderText('Icon - ex: MISC_python')
            self.iconEdits.append(a)
            primaryLayout.addWidget(a, i, 4, 1, 1)

            # point to collection if menu combo boxes
            a = QtWidgets.QComboBox()
            #a.insertItem(0, 'Link Collection')
            #a.insertItems(1, [treeItem for treeItem in self.collections if treeItem != self.collectCombo.currentText()])
            #a.setDisabled(True)
            #a.setStyleSheet('selection-background-color: rgb(25,25,25);')
            self.menuComboBoxes.append(a)
            primaryLayout.addWidget(a, i, 5, 1, 1)
            rowMenuWidgets.append(a)

            # command labels
            a = QtWidgets.QLabel('Command: ')
            self.cmdLabels.append(a)
            primaryLayout.addWidget(a, i, 6, 1, 1)
            rowButtonWidgets.append(a)

            # command type combo boxes
            a = QtWidgets.QComboBox()
            #a.insertItem(0, 'Command Type')
            #a.insertItems(1, ['Create Node', 'Custom Function'])
            self.cmdComboBoxes.append(a)
            primaryLayout.addWidget(a, i, 7, 1, 1)
            #a.currentIndexChanged.connect(self.toggleTextHint)
            #a.currentIndexChanged.connect(self.disableActiveWire)
            rowButtonWidgets.append(a)

            # nodename or custom command function line edits
            a = QtWidgets.QLineEdit()
            a.setPlaceholderText('nodename')
            self.cmdEdits.append(a)
            primaryLayout.addWidget(a, i, 8, 1, 1)
            rowButtonWidgets.append(a)

            # active wire checkboxes
            a = hou.qt.createCheckBox()
            a.setText('Active Wire On Create')
            self.wireToggles.append(a)
            primaryLayout.addWidget(a, i, 9, 1, 1)
            rowButtonWidgets.append(a)

            self.menuWidgets.append(rowMenuWidgets)
            self.buttonWidgets.append(rowButtonWidgets)

    def saveCloseUI(self):
        primaryLayout = QtWidgets.QHBoxLayout()
        self.rootLayout.addLayout(primaryLayout)
        primaryLayout.addStretch(1)

        self.saveTextWidget = QtWidgets.QLabel()
        self.saveTextWidget.setStyleSheet('font: 18pt;')

        primaryLayout.addWidget(self.saveTextWidget)
        primaryLayout.addStretch(1)

        self.saveButtonWidget = QtWidgets.QPushButton('Save Collection')
        self.closeButtonWidget = QtWidgets.QPushButton('Close')

        self.saveButtonWidget.setMinimumSize(220, 70)
        self.closeButtonWidget.setMinimumSize(220, 70)

        self.saveButtonWidget.setStyleSheet(hou.qt.styleSheet())
        self.closeButtonWidget.setStyleSheet(hou.qt.styleSheet())

        #self.saveButtonWidget.clicked.connect(lambda: self.alertText('Successfully Saved %s...' % self.collectCombo.currentText()))
        #self.saveButtonWidget.clicked.connect(lambda: self.jsonFromDetails(self.collectCombo.currentText()))
        #self.closeButtonWidget.clicked.connect(self.close)

        primaryLayout.addWidget(self.saveButtonWidget)
        primaryLayout.addWidget(self.closeButtonWidget)

    def detailDefaults(self):
        self.detailIndices = []
        for idx, c in enumerate((self.indexComboBoxes)):
            c.clear()            
            for i in range(8):                
                c.insertItem(i, '%d' % i)
                c.setCurrentIndex(c.findText('%d' % idx))
            self.detailIndices.append(idx) 
            self.menuToggles[idx].setCheckState(QtCore.Qt.Unchecked)
            self.menuComboBoxes[idx].setDisabled(True)
            self.labelEdits[idx].clear()
            self.iconEdits[idx].setText('MISC_python')
            self.cmdEdits[idx].setText('null')
            self.activeToggles[idx].setCheckState(QtCore.Qt.Unchecked)

        for menu, cmd in zip(self.menuComboBoxes, self.cmdComboBoxes):
            menu.clear()
            menu.insertItem(0, '< Not Linked >')            
            cmd.clear()
            cmd.insertItems(0, ('Create Node', 'Custom Function'))

    def connectWidgetActions(self):
        self.contextComboBox.currentIndexChanged.connect(self.contextAction)
        self.collectionComboBox.currentIndexChanged.connect(self.collectionAction)
        
        for idx, item in enumerate(self.activeToggles):
            # connect active toggles and menu toggles
            item.stateChanged.connect(self.toggleDetailRows)
            self.menuToggles[idx].stateChanged.connect(self.toggleMenuRows)

            # connect index combo boxes
            self.indexComboBoxes[idx].activated.connect(self.swapDetailRows)

            # connect all detail widgets to update virtual collection
            self.indexComboBoxes[idx].currentIndexChanged.connect(self.updateVirtualCollection)
            self.activeToggles[idx].stateChanged.connect(self.updateVirtualCollection)
            self.menuToggles[idx].stateChanged.connect(self.updateVirtualCollection)
            self.labelEdits[idx].textChanged.connect(self.updateVirtualCollection)
            self.iconEdits[idx].textChanged.connect(self.updateVirtualCollection)
            self.menuComboBoxes[idx].currentIndexChanged.connect(self.updateVirtualCollection)
            self.cmdComboBoxes[idx].currentIndexChanged.connect(self.updateVirtualCollection)
            self.cmdEdits[idx].textChanged.connect(self.updateVirtualCollection)
            self.wireToggles[idx].stateChanged.connect(self.updateVirtualCollection)            

    def contextAction(self):
        print 'context changed'
        # if the context is changed, update collectionComboBox and ModifierComboBoxes
        self.currentContext = self.contextComboBox.currentText()        
        self.collectionDir = self.rootpath + 'json/' + self.currentContext + '/'
        self.collections = utils.filterCollections(self.collectionDir, self.currentContext)
        self.collectionComboBox.clear()
        self.collectionComboBox.insertItems(0, self.collections)
        
        # modifier combo boxes
        shiftItem = self.menuPrefs[self.currentContext]['Shift']
        self.shiftComboBox.clear()
        self.shiftComboBox.insertItems(0, self.collections)
        self.shiftComboBox.setCurrentIndex(self.collections.index(shiftItem))
        
        controlItem = self.menuPrefs[self.currentContext]['Control']
        self.ctrlComboBox.clear()
        self.ctrlComboBox.insertItems(0, self.collections)
        self.ctrlComboBox.setCurrentIndex(self.collections.index(controlItem))

    def collectionAction(self):
        print 'collection changed'
        # if the collection is changed, update the details 
        if self.collectionComboBox.currentText():
            self.fullcpath = self.collectionDir + self.collectionComboBox.currentText()            
            self.loadedCollection = utils.loadCollection(self.fullcpath)
            #self.updateTree(self.treeWidget)

            # populate detail widgets
            self.updateDetails()

    def updateTree(self, parentItem):
        self.treeWidget.clear()
        
        # parent collection item
        rootItem = QtWidgets.QTreeWidgetItem(parentItem)
        rootItem.setText(0, os.path.split(self.fullcpath)[-1].split('.json')[0])
        rootItem.setExpanded(True)
        rootItem.setIcon(0, hou.qt.createIcon('SOP_object_merge'))

        brush = QtGui.QBrush()
        brush.setColor(QtGui.QColor(255, 178, 45))
        rootItem.setForeground(0, brush)

        # for each item dict in current collection        
        for idx, item in enumerate(self.virtualCollection):
            if item is not None:
                # tree display button label
                treeItem = QtWidgets.QTreeWidgetItem(rootItem)
                treeItem.setIcon(0, hou.qt.createIcon(item['icon']))
                treeItem.setText(0, '%d'%idx + '. ' + item['label'])
                treeItem.setExpanded(True)                
                brush.setColor(QtGui.QColor(203, 203, 203))
                treeItem.setForeground(0, brush)

                #self.loadDetailsFromCollection(item, idx)

                if item['isMenu']:
                    brush.setColor(QtGui.QColor(153, 255, 45))
                    treeItem.setForeground(0, brush)

                    if not item['menuCollection'] or item['menuCollection'] not in self.collections:
                        treeItemChild = QtWidgets.QTreeWidgetItem(treeItem)
                        treeItemChild.setText(0, 'No Collection Linked')
                        treeItemChild.setIcon(0, hou.qt.createIcon('SOP_delete'))

                        brush.setColor(QtGui.QColor(153, 153, 153))
                        treeItemChild.setForeground(0, brush)
                        treeItemChild.setExpanded(True)
                    else:
                        treeItemNull = QtWidgets.QTreeWidgetItem(treeItem)
                        treeItemNull.setText(0, item['menuCollection'])
                        treeItemNull.setIcon(0, hou.qt.createIcon('SOP_object_merge'))
                        brush.setColor(QtGui.QColor(255, 178, 45))
                        treeItemNull.setForeground(0, brush)
                        treeItemNull.setExpanded(True)
            else:
                # add empty tree item if empty dict
                treeItem = QtWidgets.QTreeWidgetItem(rootItem)
                treeItem.setText(0, '%d'%idx + '. ' + 'empty')
                treeItem.setExpanded(True)
                brush.setColor(QtGui.QColor(120, 120, 120))
                treeItem.setForeground(0, brush)

    def updateDetails(self):
        self.detailDefaults()
        # fill in combo boxes with current linkable collections
        linkToThese = [a for a in self.collections if self.collectionComboBox.currentText() != a]                 
        for h in self.menuComboBoxes:
            h.insertItems(1, linkToThese)
        
        for idx, item in enumerate(self.loadedCollection):
            if item is not None:                
                self.activeToggles[idx].setCheckState(QtCore.Qt.Checked)
                self.indexComboBoxes[idx].setCurrentIndex(item['index'])

                if item['isMenu']:
                    self.menuToggles[idx].setCheckState(QtCore.Qt.Checked)
                    if item['menuCollection']:

                        linkCollection = self.menuComboBoxes[idx].findText(item['menuCollection'])
                        self.menuComboBoxes[idx].setCurrentIndex(linkCollection)
                    else:
                        self.menuComboBoxes[idx].setCurrentIndex(0)
                else:
                    self.menuToggles[idx].setCheckState(QtCore.Qt.Unchecked)
                    cmdIndex = item['commandType'] == 'createnode'
                    self.cmdComboBoxes[idx].setCurrentIndex(cmdIndex)
                    cmdTxt = ''
                    if item['commandType'] == 'createnode':
                        cmdTxt = item['nodetype']  
                    else:
                        cmdTxt = item['command'].split('.')[1]
                    self.cmdEdits[idx].setText(cmdTxt)

                self.labelEdits[idx].setText(item['label'])
                self.iconEdits[idx].setText(item['icon'])
            else:
                self.activeToggles[idx].setCheckState(QtCore.Qt.Unchecked)

    def toggleDetailRows(self):
        for idx, item in enumerate(self.activeToggles):        
            self.menuToggles[idx].setDisabled(not item.isChecked())
            self.labelEdits[idx].setDisabled(not item.isChecked())
            self.iconEdits[idx].setDisabled(not item.isChecked())
            self.menuComboBoxes[idx].setDisabled(not item.isChecked())
            self.cmdLabels[idx].setDisabled(not item.isChecked())
            self.cmdComboBoxes[idx].setDisabled(not item.isChecked())
            self.cmdEdits[idx].setDisabled(not item.isChecked())
            self.wireToggles[idx].setDisabled(not item.isChecked())
            self.toggleMenuRows()

    def swapDetailRows(self):
        if len(self.detailIndices) == 8:
            currentOrder = []
            for item in self.indexComboBoxes:
                currentOrder.append(item.currentIndex())
            changedIndex = -1
            for current, prev in zip(currentOrder, self.detailIndices):
                if current != prev:
                    val0 = current
                    val1 = prev             
                    changedIndex = currentOrder.index(current)
            if changedIndex != -1:
                idx0 = self.detailIndices.index(val0)
                idx1 = self.detailIndices.index(val1)                

                self.detailIndices[idx0], self.detailIndices[idx1] = self.detailIndices[idx1], self.detailIndices[idx0]

                for idx, thing in enumerate(self.indexComboBoxes):
                    thing.setCurrentIndex(self.detailIndices[idx])

    def toggleMenuRows(self):
        for idx, item in enumerate(self.menuToggles):
            if item.isEnabled():
                self.menuComboBoxes[idx].setDisabled(not item.isChecked())
                self.cmdLabels[idx].setDisabled(item.isChecked())
                self.cmdComboBoxes[idx].setDisabled(item.isChecked())
                self.cmdEdits[idx].setDisabled(item.isChecked())
                self.wireToggles[idx].setDisabled(item.isChecked())

    def updateVirtualCollection(self):
        temp = []
        for idx in range(8):
            if not self.activeToggles[idx].isChecked():
                temp.append(None)
            else:
                newEntry = {}
                index = self.indexComboBoxes[idx].currentIndex()
                isMenu = self.menuToggles[idx].isChecked()
                if not len(self.labelEdits[idx].text()):
                    label = 'Label'
                else:
                    label = self.labelEdits[idx].text()
                if not len(self.iconEdits[idx].text()):
                    icon = 'MISC_python'
                else:
                    icon = self.iconEdits[idx].text()
                if not self.menuComboBoxes[idx].currentIndex():
                    menuCollection = ''
                else:
                    menuCollection = self.menuComboBoxes[idx].currentText()
                if not self.cmdComboBoxes[idx].currentIndex():
                    commandType = 'createnode'
                    command = self.cmdEdits[idx].text()
                    nodetype = self.cmdEdits[idx].text()
                else:
                    commandType = 'customfunction'
                    command = 'cmds.' + self.cmdEdits[idx].text()
                    nodetype = 'null'
                wire = self.wireToggles[idx].isChecked()

                newEntry = utils.ButtonConfig(
                    self.currentContext,
                    index,
                    isMenu,
                    label,
                    icon,
                    menuCollection,
                    commandType,
                    command,
                    nodetype,
                    wire
                    )
                temp.append(newEntry.config)
        self.virtualCollection = temp
        self.updateTree(self.treeWidget)


    def closeEvent(self, e):
        self.setParent(None)
        self.deleteLater()
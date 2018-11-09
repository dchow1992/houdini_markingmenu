import sys

import os

import json

import hou

from PySide2 import QtWidgets, QtGui, QtCore, QtTest

from editor.widgets import managecollectionstoolbar

from editor.widgets import modifiercomboboxes

from editor.widgets import referenceview

from editor.widgets import detailspane

from editor.widgets import editortaskbar

import utils

reload(detailspane)
reload(referenceview)
reload(managecollectionstoolbar)
reload(modifiercomboboxes)
reload(detailspane)


class MarkingMenuEditor(QtWidgets.QWidget):
    """Editor for creating, deleting, and editing marking menus."""
    def __init__(self):
        super(MarkingMenuEditor, self).__init__()
        self.setParent(hou.qt.mainWindow(), QtCore.Qt.Window)
        self.setWindowTitle('Marking Menu Editor')
        self.setGeometry(300, 250, 900, 700)
        self.setStyleSheet('background-color: rgb(58,58,58);')
        self.setFixedSize(1150, 850)

        self._rootpath = os.path.join(
                os.path.abspath(hou.getenv('HOUDINI_USER_PREF_DIR')),
                'python2.7libs',
                'houdini_markingmenu'
                )

        self._contexts = sorted([
            'SOP', 'OBJ', 'DOP', 'VOP', 'ROP',
            'SHOP', 'CHOP', 'COP'
            ])

        self._collections = []
        self._currentContext = 'SOP'

        self._collectionsDir = os.path.join(
            self._rootpath,
            'json',
            self._currentContext
            )

        self._fullcpath = ''  # full path to the current collection on disk
        self._menuPrefs = utils.loadMenuPreferences(os.path.join(
            self._rootpath, 'json', 'menuprefs.json'))
        self._detailIndices = []
        self._loadedCollection = []
        self._virtualCollection = []
        self._unfreezeVirtualUpdate = 0
        self._unsaved = 0
        self._prevCollection = ''

        self.legendmenus = []
        self.legendcollections = []
        self.legendactions = []
        self.legendHistory = 0


        # button functions auto completer
        readfile = []
        funcList = []
        with open(os.path.join(self._rootpath, 'buttonfunctions.py'), 'r') as f:
            readfile = f.readlines()

        for line in readfile:
            if '**kwargs' in line:
                funcList.append(line.split('def ')[-1].split('(')[0])
        funcList.append('launchEditor')
        funcList += hou.shelves.tools().keys()
        self._funcCompleter = QtWidgets.QCompleter(funcList)
        self._funcCompleter.popup().setStyleSheet(hou.qt.styleSheet())
        self._funcCompleter.setCompletionMode(QtWidgets.QCompleter.PopupCompletion)

        self.__initUI()

    def __initUI(self):
        self._layout = QtWidgets.QVBoxLayout()
        self.setLayout(self._layout)

        # collections menu toolbar
        self._menuToolbar = managecollectionstoolbar.ManageCollectionsToolbar()

        self._layout.addLayout(self._menuToolbar.layout)
        self._layout.addSpacing(10)

        # modifier collection combo boxes
        self._modifierComboBoxes = modifiercomboboxes.ModifierComboBoxes()
        self._layout.addLayout(self._modifierComboBoxes.layout)

        # reference view
        self._referenceView = referenceview.ReferenceView()
        self._layout.addLayout(self._referenceView.layout)

        self._layout.addSpacing(10)

        # details pane
        self._detailsPane = detailspane.DetailsPane(self._rootpath)
        self._layout.addLayout(self._detailsPane.layout)

        self._saveSeparatorWidget = hou.qt.createSeparator()
        self._layout.addWidget(self._saveSeparatorWidget)

        # taskbar
        self._taskbar = editortaskbar.EditorTaskbar()
        self._layout.addLayout(self._taskbar.layout)

        self.__connectWidgetActions()

        # context combobox default to current context
        self._menuToolbar.contextComboBox.insertItems(0, self._contexts)

        self._menuToolbar.contextComboBox.setCurrentIndex(
            self._menuToolbar.contextComboBox.findText(utils.getContext()))

        self._currentContext = self._menuToolbar.contextComboBox.currentText()
        self.show()

    def __detailDefaults(self):
        for idx, c in enumerate((self._detailsPane.indexComboBoxes)):
            c.clear()
            for i in range(8):
                c.insertItem(i, '%d' % i)
                c.setCurrentIndex(c.findText('%d' % idx))
            if len(self._detailIndices) < 8:
                self._detailIndices.append(idx)
            self._detailsPane.menuToggles[idx].setCheckState(QtCore.Qt.Unchecked)
            self._detailsPane.menuComboBoxes[idx].setDisabled(True)
            self._detailsPane.labelEdits[idx].clear()
            self._detailsPane.iconEdits[idx].setText('MISC_python')
            self._detailsPane.cmdEdits[idx].setText('null')
            self._detailsPane.activeToggles[idx].setCheckState(QtCore.Qt.Unchecked)

        for menu, cmd in zip(self._detailsPane.menuComboBoxes, self._detailsPane.cmdComboBoxes):
            menu.clear()
            menu.insertItem(0, '< Not Linked >')
            cmd.clear()
            cmd.insertItems(0, ('Create Node', 'User Function'))

    def __connectWidgetActions(self):
        self._menuToolbar.contextComboBox.currentIndexChanged.connect(
            self.__contextAction)

        self._menuToolbar.collectionComboBox.currentIndexChanged.connect(
            self.__collectionAction)
        self._menuToolbar.collectionComboBox.view().pressed.connect(self.__updateLegendHistory)

        self._referenceView.homebtn.clicked.connect(self.__homeContext)
        self._referenceView.backbtn.clicked.connect(self.__backContext)
        self._menuToolbar.reloadBtn.clicked.connect(self.__contextAction)
        self._taskbar.closeButton.clicked.connect(self.__closeAction)

        self._taskbar.saveButton.clicked.connect(
            lambda: self.__saveAction(
                self._menuToolbar.collectionComboBox.currentText()))

        self._menuToolbar.newBtn.clicked.connect(self.__newAction)
        self._menuToolbar.delBtn.clicked.connect(self.__deleteAction)
        self._menuToolbar.renameBtn.clicked.connect(self.__renameAction)

        self._modifierComboBoxes.shift.comboBox.currentIndexChanged.connect(
            self.__updateMenuPrefs)
        self._modifierComboBoxes.ctrl.comboBox.currentIndexChanged.connect(
            self.__updateMenuPrefs)

        self._detailsPane.allActiveToggle.stateChanged.connect(self.__allActiveAction)
        self._detailsPane.allMenuToggle.stateChanged.connect(self.__allMenuAction)
        self._detailsPane.allWireToggle.stateChanged.connect(self.__allWireAction)

        for idx, item in enumerate(self._detailsPane.activeToggles):
            # connect active toggles and menu toggles
            item.stateChanged.connect(self.__toggleDetailRows)
            self._detailsPane.menuToggles[idx].stateChanged.connect(self.__toggleMenuRows)

            # connect index combo boxes
            self._detailsPane.indexComboBoxes[idx].activated.connect(self.__swapDetailRows)

            # connect all detail widgets to update virtual collection
            self._detailsPane.activeToggles[idx].stateChanged.connect(
                self.__updateVirtualCollection)

            self._detailsPane.menuToggles[idx].stateChanged.connect(
                self.__updateVirtualCollection)

            self._detailsPane.labelEdits[idx].textChanged.connect(
                self.__updateVirtualCollection)

            self._detailsPane.iconEdits[idx].textChanged.connect(
                self.__updateVirtualCollection)

            self._detailsPane.menuComboBoxes[idx].currentIndexChanged.connect(
                self.__updateVirtualCollection)

            self._detailsPane.cmdComboBoxes[idx].currentIndexChanged.connect(
                self.__updateVirtualCollection)

            self._detailsPane.cmdEdits[idx].textChanged.connect(
                self.__updateVirtualCollection)

            self._detailsPane.wireToggles[idx].stateChanged.connect(
                self.__updateVirtualCollection)

    def __allActiveAction(self):
        for box in self._detailsPane.activeToggles:
            if box.isEnabled():
                box.setCheckState(self._detailsPane.allActiveToggle.checkState())

    def __allMenuAction(self):
        for box in self._detailsPane.menuToggles:
            if box.isEnabled():
                box.setCheckState(self._detailsPane.allMenuToggle.checkState())

    def __allWireAction(self):
        for box in self._detailsPane.wireToggles:
            if box.isEnabled():
                box.setCheckState(self._detailsPane.allWireToggle.checkState())

    def __contextAction(self):
        # self._prevCollection = self._menuToolbar.collectionComboBox.currentText()
        self.__updateLegendHistory()
        if self._unsaved:
            self.__unsavedPrompt(self._menuToolbar.collectionComboBox.currentText())
        # if context is changed, update collectionComboBox and ModifierComboBoxes
        self._currentContext = self._menuToolbar.contextComboBox.currentText()
        self._collectionsDir = os.path.join(self._rootpath, 'json', self._currentContext)

        if self._currentContext in ['SOP', 'VOP', 'DOP', 'COP', 'CHOP', 'OBJ', 'ROP']:
            # build completer based on current context
            strlist = []
            jsondict = {}

            # add HDAs to strlist
            context2 = self._currentContext[0] + self._currentContext[1:].lower()
            all_types = []

            categories = hou.nodeTypeCategories()
            for category in categories.keys():
                node_types = categories[category].nodeTypes()
                for node_type in node_types.keys():
                    all_types.append(node_types[node_type].nameWithCategory())

            # split off version and namespace
            temp = []
            for a in all_types:
                asplit = a.split('::')
                if len(asplit) == 1:
                    temp.append(asplit[0])
                elif len(asplit) == 2:
                    if len(asplit[0]) > len(asplit[1]):
                        temp.append(asplit[0])
                    else:
                        temp.append(asplit[1])
                elif len(asplit) == 3:
                    temp.append(asplit[1])

            all_types = temp
            alltypeset = set(all_types)
            contextHDAs = [a.split('/')[-1] for a in alltypeset]
            strlist = strlist + list(set(contextHDAs) - set(strlist))

            # assign completer
            self.nodeCompleter = QtWidgets.QCompleter(strlist)
            self.nodeCompleter.popup().setStyleSheet(hou.qt.styleSheet())
            self.nodeCompleter.setCompletionMode(QtWidgets.QCompleter.PopupCompletion)

        # refilter collections by context
        self._collections = utils.filterCollections(
            self._collectionsDir,
            self._currentContext
            )

        self.collectionsLabels = [os.path.splitext(a)[0] for a in self._collections]

        self._menuToolbar.collectionComboBox.clear()
        self._menuToolbar.collectionComboBox.insertItems(0, self.collectionsLabels)

        # modifier combo boxes
        self._menuPrefs = utils.loadMenuPreferences(os.path.join(
            self._rootpath, 'json', 'menuprefs.json'))
        try:
            shiftItem = self._menuPrefs[self._currentContext]['Shift']
            self._modifierComboBoxes.shift.comboBox.clear()
            self._modifierComboBoxes.shift.comboBox.insertItems(0, self.collectionsLabels)
            self._modifierComboBoxes.shift.comboBox.setCurrentIndex(self._collections.index(shiftItem))

            controlItem = self._menuPrefs[self._currentContext]['Control']
            self._modifierComboBoxes.ctrl.comboBox.clear()
            self._modifierComboBoxes.ctrl.comboBox.insertItems(0, self.collectionsLabels)
            self._modifierComboBoxes.ctrl.comboBox.setCurrentIndex(self._collections.index(controlItem))
        except ValueError:
            pass

    def __collectionAction(self):
        if self._unsaved:
            self.__unsavedPrompt(self._prevCollection)
        # self._prevCollection = self._menuToolbar.collectionComboBox.currentText()
        # if the collection is changed, update the details
        if self._menuToolbar.collectionComboBox.currentText():
            self._fullcpath = os.path.join(
                self._collectionsDir,
                self._menuToolbar.collectionComboBox.currentText() + '.json')

            self._loadedCollection = utils.loadCollection(self._fullcpath)
            self._virtualCollection = self._loadedCollection
            self._taskbar.saveTextWidget.setStyleSheet(
                '''
                color: rgb(58, 58, 58);
                font: 18pt;
                '''
                )
            # initialize details and tree
            # after this, changing indices and virtual collection will
            # drive updates
            self._unfreezeVirtualUpdate = 0
            self.__updateDetails()
            self.__updateTree(self._referenceView.tree)
            self.__updateLegend()

    def __saveAction(self, name):
        self.__alertText(
            "Saved ' %s '" % name
            )
        self._unsaved = 0

        utils.saveCollection(self._fullcpath, self._virtualCollection)

    def __newAction(self):
        diag = hou.ui.readInput(
                'Create New Collection',
                buttons=('OK', 'Cancel'),
                close_choice=1,
                help='"namestr", not "SOP_newname.json"',
                title='New',
                initial_contents='newcollection'
                )
        # if text entered and OK selected
        if diag[1] and not diag[0]:
            self._unsaved = 0
            self.__updateLegendHistory()
            # self._prevCollection = self._menuToolbar.collectionComboBox.currentText()

            namestr = diag[1]
            namestr = namestr.strip(' ').replace(' ', '_')
            # strip context and extension from name if they are there
            if namestr.startswith(self._currentContext + '_'):
                namestr = namestr[len(self._currentContext) + 1:len(namestr)]
            if namestr.endswith('.json'):
                namestr = namestr[0:len(namestr)-len('.json')]
            namestr = '_'.join([self._currentContext, namestr]) + '.json'

            if namestr in self._collections:
                hou.ui.displayMessage(
                        'This collection already exists',
                        severity=hou.severityType.Warning,
                        buttons=('OK',)
                        )
            else:
                self.__detailDefaults()
                utils.saveCollection(
                    os.path.join(self._collectionsDir, namestr),
                    self._virtualCollection
                    )
                self._unsaved = 0
                self.__contextAction()
                self._menuToolbar.collectionComboBox.setCurrentIndex(
                    self._menuToolbar.collectionComboBox.findText(os.path.splitext(namestr)[0])
                    )

        elif not diag[1]:
            hou.ui.displayMessage(
                        'Invalid name',
                        severity=hou.severityType.Warning,
                        buttons=('OK',)
                        )

    def __deleteAction(self):
        col = self._menuToolbar.collectionComboBox.currentText() + '.json'
        if col == ('{}_baseCollection.json'.format(self._currentContext)):
            hou.ui.displayMessage(
                'Base Collections cannot be deleted',
                severity=hou.severityType.Warning,
                buttons=('OK',)
                )
        else:
            verify = hou.ui.displayMessage(
                'Delete Collection: {}\nAre you sure?'.format(col),
                buttons=('Yes', 'No'),
                close_choice=1
                )
            if not verify:
                self._unsaved = 0
                # need to replace modifier collections if they are linked to
                # the collection that is going to be deleted
                shift = self._modifierComboBoxes.shift.comboBox.currentText()
                ctrl = self._modifierComboBoxes.ctrl.comboBox.currentText()
                if shift == col:
                    self._modifierComboBoxes.shift.comboBox.setCurrentIndex(
                        self._modifierComboBoxes.shift.comboBox.findText(
                            '{}_baseCollection.json'.format(self._currentContext)
                            )
                        )
                if ctrl == col:
                    self._modifierComboBoxes.ctrl.comboBox.setCurrentIndex(
                        self._modifierComboBoxes.ctrl.comboBox.findText(
                            '{}_baseCollection.json'.format(self._currentContext)
                            )
                        )
                os.remove(os.path.join(self._collectionsDir, col))
                self.__contextAction()
                self.__alertText('Deleted: %s' % col)

    def __renameAction(self):
        col = self._menuToolbar.collectionComboBox.currentText() + '.json'
        if col == (self._currentContext + '_baseCollection.json'):
            hou.ui.displayMessage(
                'Base Collections cannot be renamed',
                severity=hou.severityType.Warning,
                buttons=('OK',)
                )
        else:
            diag = hou.ui.readInput(
                'Rename Collection',
                buttons=('Save', 'Cancel'),
                close_choice=1,
                help='"namestr", not "SOP_newname.json"',
                title='Rename',
                initial_contents='newname'
                )

            if diag[1] and not diag[0]:
                namestr = diag[1]
                namestr = namestr.strip(' ').replace(' ', '_')
                # strip context and extension from name if they are there
                if namestr.startswith(self._currentContext + '_'):
                    namestr = namestr[len(self._currentContext) + 1:len(namestr)]
                if namestr.endswith('.json'):
                    namestr = namestr[0:len(namestr)-len('.json')]
                namestr = '_'.join([self._currentContext, namestr]) + '.json'

                # prevent writing over base collection of current context
                if namestr == ('{}_baseCollection.json'.format(self._currentContext)):
                    hou.ui.displayMessage(
                        'Invalid name',
                        severity=hou.severityType.Warning,
                        buttons=('OK',)
                        )
                else:
                    # warn if overwrite operation
                    overwrite = 0
                    if namestr in self._collections:
                        overwrite = not hou.ui.displayMessage(
                            '''%s already exists. \n
                            Are you sure you want to overwrite it?''' %
                            (namestr),
                            severity=hou.severityType.Warning,
                            buttons=('Yes', 'No')
                            )

                    if namestr not in self._collections or overwrite:
                        oldpath = os.path.join(self._collectionsDir, col)
                        newpath = os.path.join(self._collectionsDir, namestr)
                        if os.path.isfile(oldpath) and overwrite:
                            # remove newpath to make space for oldpath to be renamed
                            os.remove(newpath)
                            os.rename(oldpath, newpath)
                        else:
                            os.rename(oldpath, newpath)

                        self.__alertText('{} renamed to {}'.format(
                            self._menuToolbar.collectionComboBox.currentText(),
                            os.path.splitext(namestr)[0])
                            )
                        self.__contextAction()
                        self._menuToolbar.collectionComboBox.setCurrentIndex(
                            self._menuToolbar.collectionComboBox.findText(os.path.splitext(namestr)[0])
                            )
            elif not diag[1]:
                hou.ui.displayMessage(
                        'Invalid name',
                        severity=hou.severityType.Warning,
                        buttons=('OK',)
                        )

    def __updateMenuPrefs(self):
        prefs = {}
        path = os.path.join(self._rootpath, 'json', 'menuprefs.json')
        with open(path, 'r') as f:
            prefs = json.load(f)
        prefs[self._currentContext]['Shift'] = self._modifierComboBoxes.shift.comboBox.currentText() + '.json'
        prefs[self._currentContext]['Control'] = self._modifierComboBoxes.ctrl.comboBox.currentText() + '.json'

        self._menuPrefs[self._currentContext]['Shift'] = self._modifierComboBoxes.shift.comboBox.currentText() + '.json'
        self._menuPrefs[self._currentContext]['Control'] = self._modifierComboBoxes.ctrl.comboBox.currentText() + '.json'

        with open(path, 'w') as f:
            json.dump(prefs, f, indent=4, sort_keys=True)

    def __updateTree(self, parentItem):
        self._referenceView.tree.clear()
        # parent collection item
        rootItem = QtWidgets.QTreeWidgetItem(parentItem)
        rootItem.setText(0, os.path.split(self._fullcpath)[-1].split('.json')[0])
        rootItem.setExpanded(True)
        rootItem.setIcon(0, hou.qt.createIcon('SOP_object_merge'))

        brush = QtGui.QBrush()
        brush.setColor(QtGui.QColor(255, 178, 45))
        rootItem.setForeground(0, brush)

        # for each item dict in current collection
        # for idx, item in enumerate(self._virtualCollection):
        for item in self._virtualCollection:
            idx = item['index']
            if item['active']:
                # tree display button label
                treeItem = QtWidgets.QTreeWidgetItem(rootItem)
                try:
                    treeItem.setIcon(0, hou.qt.createIcon(item['icon']))
                except hou.OperationFailed:
                    treeItem.setIcon(0, hou.qt.createIcon('MISC_python'))

                treeItem.setText(0, '%d' % idx + '. ' + item['label'])
                treeItem.setExpanded(True)
                brush.setColor(QtGui.QColor(203, 203, 203))
                treeItem.setForeground(0, brush)

                if item['isMenu']:
                    brush.setColor(QtGui.QColor(153, 255, 45))
                    treeItem.setForeground(0, brush)

                    if (not item['menuCollection'] or
                            item['menuCollection'] not in self._collections):
                        treeItemChild = QtWidgets.QTreeWidgetItem(treeItem)
                        treeItemChild.setText(0, 'No Collection Linked')
                        treeItemChild.setIcon(0, hou.qt.createIcon('SOP_delete'))

                        brush.setColor(QtGui.QColor(153, 153, 153))
                        treeItemChild.setForeground(0, brush)
                        treeItemChild.setExpanded(True)
                    else:
                        treeItemNull = QtWidgets.QTreeWidgetItem(treeItem)
                        treeItemNull.setText(0, os.path.splitext(item['menuCollection'])[0])
                        treeItemNull.setIcon(0, hou.qt.createIcon('SOP_object_merge'))
                        brush.setColor(QtGui.QColor(255, 178, 45))
                        treeItemNull.setForeground(0, brush)
                        treeItemNull.setExpanded(True)
            else:
                # add empty tree item if empty dict
                treeItem = QtWidgets.QTreeWidgetItem(rootItem)
                treeItem.setText(0, '%d' % idx + '. ' + 'empty')
                treeItem.setExpanded(True)
                brush.setColor(QtGui.QColor(120, 120, 120))
                treeItem.setForeground(0, brush)

    def __updateDetails(self):
        self.__detailDefaults()
        # fill in combo boxes with current linkable collections
        linkToThese = [
            os.path.splitext(a)[0] for a in self._collections if
            self._menuToolbar.collectionComboBox.currentText() != os.path.splitext(a)[0]
            ]

        for h in self._detailsPane.menuComboBoxes:
            h.insertItems(1, linkToThese)

        # for idx, item in enumerate(self._virtualCollection):
        for item in self._virtualCollection:
            idx = item['index']
            isActive = item['active']
            if isActive:
                self._detailsPane.activeToggles[idx].setCheckState(QtCore.Qt.Checked)
            else:
                self._detailsPane.activeToggles[idx].setCheckState(QtCore.Qt.Unchecked)
            # self._detailsPane.indexComboBoxes[idx].setCurrentIndex(item['index'])
            if item['isMenu']:
                self._detailsPane.menuToggles[idx].setCheckState(QtCore.Qt.Checked)

                if item['menuCollection'] and \
                        item['menuCollection'] in self._collections:

                    linkCollection = self._detailsPane.menuComboBoxes[idx].findText(
                        os.path.splitext(item['menuCollection'])[0])
                    self._detailsPane.menuComboBoxes[idx].setCurrentIndex(linkCollection)
                else:
                    self._detailsPane.menuComboBoxes[idx].setCurrentIndex(0)
            else:
                self._detailsPane.menuToggles[idx].setCheckState(QtCore.Qt.Unchecked)

                cmdIndex = item['commandType'] != 'createnode'

                self._detailsPane.cmdComboBoxes[idx].setCurrentIndex(cmdIndex)

                cmdTxt = ''

                if item['commandType'] == 'createnode':
                    cmdTxt = item['nodetype']
                else:
                    if item['command']:
                        cmdTxt = item['command']

                self._detailsPane.cmdEdits[idx].setText(cmdTxt)

            self._detailsPane.labelEdits[idx].setText(item['label'])
            self._detailsPane.labelEdits[0].setFocus()
            self._detailsPane.iconEdits[idx].setText(item['icon'])

            if item['activeWire']:
                self._detailsPane.wireToggles[idx].setCheckState(QtCore.Qt.Checked)
            else:
                self._detailsPane.wireToggles[idx].setCheckState(QtCore.Qt.Unchecked)

        # toggle self._unfreezeVirtualUpdate if 0
        if not self._unfreezeVirtualUpdate:
            self._unfreezeVirtualUpdate = 1
        self.__updateCollectionIcons()

    def __toggleDetailRows(self):
        for idx, item in enumerate(self._detailsPane.activeToggles):
            self._detailsPane.indexComboBoxes[idx].setDisabled(not item.isChecked())
            self._detailsPane.menuToggles[idx].setDisabled(not item.isChecked())
            self._detailsPane.labelEdits[idx].setDisabled(not item.isChecked())
            self._detailsPane.iconEdits[idx].setDisabled(not item.isChecked())
            self._detailsPane.menuComboBoxes[idx].setDisabled(not item.isChecked())
            self._detailsPane.cmdLabels[idx].setDisabled(not item.isChecked())
            self._detailsPane.cmdComboBoxes[idx].setDisabled(not item.isChecked())
            self._detailsPane.cmdEdits[idx].setDisabled(not item.isChecked())
            self._detailsPane.wireToggles[idx].setDisabled(not item.isChecked())
            self.__toggleMenuRows()

    def __toggleMenuRows(self):
        for idx, item in enumerate(self._detailsPane.menuToggles):
            if item.isEnabled():
                self._detailsPane.menuComboBoxes[idx].setDisabled(not item.isChecked())
                self._detailsPane.cmdLabels[idx].setDisabled(item.isChecked())
                self._detailsPane.cmdComboBoxes[idx].setDisabled(item.isChecked())
                self._detailsPane.cmdEdits[idx].setDisabled(item.isChecked())
                self._detailsPane.wireToggles[idx].setDisabled(item.isChecked())

    def __swapDetailRows(self):
        self._detailIndices = range(8)
        if len(self._detailIndices) == 8:
            currentOrder = []
            for item in self._detailsPane.indexComboBoxes:
                currentOrder.append(item.currentIndex())
            changedIndex = -1
            for current, prev in zip(currentOrder, self._detailIndices):
                if current != prev:
                    val0 = current
                    val1 = prev
                    changedIndex = currentOrder.index(current)
            if changedIndex != -1:
                idx0 = self._detailIndices.index(val0)
                idx1 = self._detailIndices.index(val1)

                self._detailIndices[idx0], self._detailIndices[idx1] = \
                    self._detailIndices[idx1], self._detailIndices[idx0]

                # this is a[idx0][key],a[idx1][key] = a[idx1][key], a[idx][key]
                # first swap dict items, then swap back indices
                self._virtualCollection[idx0], \
                    self._virtualCollection[idx1] = \
                    self._virtualCollection[idx1], \
                    self._virtualCollection[idx0]

                self._virtualCollection[idx0]['index'], \
                    self._virtualCollection[idx1]['index'] = \
                    self._virtualCollection[idx1]['index'], \
                    self._virtualCollection[idx0]['index']

                self._unfreezeVirtualUpdate = 0
                self.__unsavedChangesAlert()
                self.__updateDetails()
                self.__updateTree(self._referenceView.tree)
                self.__updateLegend()

    def __updateVirtualCollection(self):
        if self._unfreezeVirtualUpdate:
            temp = []
            for idx in range(8):
                index = idx
                if not self._detailsPane.activeToggles[idx].isChecked():
                    defEntry = utils.ButtonConfig(
                        self._currentContext,
                        index,
                        0,
                        '',
                        'MISC_python',
                        '',
                        'createnode',
                        '',
                        'null',
                        False
                        )
                    defEntry.config['active'] = 0
                    temp.append(defEntry.config)
                else:
                    newEntry = {}
                    isMenu = self._detailsPane.menuToggles[idx].isChecked()

                    if not len(self._detailsPane.labelEdits[idx].text()):
                        label = 'Label'
                    else:
                        label = self._detailsPane.labelEdits[idx].text()

                    if not len(self._detailsPane.iconEdits[idx].text()):
                        icon = 'MISC_python'
                    else:
                        icon = self._detailsPane.iconEdits[idx].text()

                    menuCollection = self._detailsPane.menuComboBoxes[idx].currentText() + '.json'
                    if not self._detailsPane.cmdComboBoxes[idx].currentIndex():
                        self._detailsPane.cmdEdits[idx].setCompleter(self.nodeCompleter)
                        commandType = 'createnode'
                        command = 'createNode'
                        nodetype = self._detailsPane.cmdEdits[idx].text().lstrip().rstrip()
                    else:
                        self._detailsPane.cmdEdits[idx].setCompleter(self._funcCompleter)
                        commandType = 'customfunction'
                        command = self._detailsPane.cmdEdits[idx].text().lstrip().rstrip()
                        nodetype = 'null'

                    wire = self._detailsPane.wireToggles[idx].isChecked()

                    newEntry = utils.ButtonConfig(
                        self._currentContext,
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
            temp = sorted(temp, key=lambda d: d['index'], reverse=False)
            self._virtualCollection = temp
            if self._menuToolbar.collectionComboBox.currentText() == self._prevCollection:
                self._unsaved = 1
            self.__unsavedChangesAlert()
            self.__updateTree(self._referenceView.tree)
            self.__updateCollectionIcons()
            self.__updateLegend()

    def __updateCollectionIcons(self):
        unlinkedBrush = QtGui.QBrush(QtCore.Qt.SolidPattern)
        unlinkedBrush.setColor(QtGui.QColor(203, 203, 203))

        linkedBrush = QtGui.QBrush(QtCore.Qt.SolidPattern)
        linkedBrush.setColor(QtGui.QColor(140, 140, 140))

        linkedMenus = []
        for item in self._virtualCollection:
            if item['isMenu']:
                idx = item['index']
                if self._detailsPane.menuComboBoxes[idx].currentText() != '<Not Linked>':
                    linkedMenus.append(self._detailsPane.menuComboBoxes[idx].currentText())

        for item in self._virtualCollection:
            if item['isMenu']:
                idx = item['index']
                for label in linkedMenus:
                    menuidx = self._detailsPane.menuComboBoxes[idx].findText(label)
                    if self._detailsPane.menuComboBoxes[idx].currentText() not in linkedMenus:
                        self._detailsPane.menuComboBoxes[idx].setItemData(
                            menuidx,
                            unlinkedBrush,
                            QtCore.Qt.ForegroundRole)

                    if label != self._detailsPane.menuComboBoxes[idx].currentText():
                        self._detailsPane.menuComboBoxes[idx].setItemData(menuidx, linkedBrush, QtCore.Qt.ForegroundRole)
                    else:
                        self._detailsPane.menuComboBoxes[idx].setItemData(menuidx, unlinkedBrush, QtCore.Qt.ForegroundRole)

    def __updateLegend(self):
        self.legendmenus = range(8)
        self.legendcollections = range(8)
        self.legendactions = range(8)
        for idx, btn in enumerate(self._referenceView.btns):
            item = self._virtualCollection[idx]

            dummyMenu = QtWidgets.QMenu()
            dummyCollection = item['menuCollection']
            self.legendmenus[idx] = dummyMenu
            self.legendcollections[idx] = dummyCollection

            if item['active']:
                btn.setDisabled(False)
                btn.setStyleSheet('')
                btn.setStyleSheet('''
                    QPushButton
                    {
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
                    ''')
                btn.setText(item['label'])

                try:
                    btn.setIcon(hou.qt.createIcon(item['icon'], 20, 20))
                    btn.setIconSize(QtCore.QSize(12, 12))
                except hou.OperationFailed:
                    btn.setIcon(hou.qt.createIcon('COMMON_null', 20, 20))
                    btn.setIconSize(QtCore.QSize(12, 12))

                if item['isMenu']:
                    btn.setStyleSheet(btn.styleSheet() +
                    '''
                    QPushButton:hover
                    {
                        border: 1px solid rgba(185, 134, 32, 100%);
                    }''')

                    btn.setMenu(dummyMenu)
                    x = btn.menu()
                    action = x.addAction('Go to..')
                    x.setStyleSheet('''
                        QMenu
                        {
                            background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                                        stop: 0.0 rgb(86, 86, 86),
                                        stop: 1.0 rgb(58, 58, 58));
                            color: rgb(203, 203, 203);
                        }
                        QMenu::item:selected
                        {
                            background: rgba(185, 134, 32, 100%);
                        }''')

                    self.legendactions[idx] = action
                    action.triggered.connect(lambda x=item['menuCollection']: self.__setCollection(x))
                else:
                    btn.setMenu(QtWidgets.QMenu())
                    try:
                        btn.clicked.disconnect()
                    except Exception:
                        pass

            elif not item['active']:
                btn.setDisabled(True)
                btn.setStyleSheet(' ')
                btn.setText('Item Slot {}'.format(idx))
                btn.setIcon(QtGui.QIcon())
                btn.setMenu(QtWidgets.QMenu())
                try:
                    btn.clicked.disconnect()
                except Exception:
                    pass

    def __setCollection(self, collection):
        idx = self._menuToolbar.collectionComboBox.findText(collection.split('.json')[0])
        if idx != -1:
            self.__updateLegendHistory()
            self._menuToolbar.collectionComboBox.setCurrentIndex(idx)

    def __homeContext(self):
        x = self._menuToolbar.collectionComboBox.currentIndex()
        if x != 0:
            self.__updateLegendHistory()
            self._menuToolbar.collectionComboBox.setCurrentIndex(0)

    def __backContext(self):
        x = self._menuToolbar.collectionComboBox.currentIndex()
        if self.legendHistory != x:
            tmp = self.legendHistory
            self.__updateLegendHistory()
            self._menuToolbar.collectionComboBox.setCurrentIndex(tmp)

    def __updateLegendHistory(self):
        self._prevCollection = self._menuToolbar.collectionComboBox.currentText()
        self.legendHistory = self._menuToolbar.collectionComboBox.currentIndex()

    def __unsavedPrompt(self, name):
        verify = hou.ui.displayMessage(
            'Unsaved changes found, would you like to save changes?',
            buttons=('Yes', 'No'),
            close_choice=1
            )
        if not verify:
            self.__saveAction(name)
        else:
            self._unsaved = 0

    def __closeAction(self):
        if self._unsaved:
            self.__unsavedPrompt(self._menuToolbar.collectionComboBox.currentText())
        self.close()

    def __unsavedChangesAlert(self):
        self._unsaved = 1
        self._taskbar.saveTextWidget.setText(
            ' < unsaved changes > '
            )
        self._taskbar.saveTextWidget.setStyleSheet(
            '''
            color: rgb(255, 255, 255);
            font: 18pt;
            '''
            )

    def __alertText(self, displayText):
        # fade the save text alert
        self.timer = QtCore.QTimer()
        self.textOpac = 1.25
        self.timer.timeout.connect(self.__fadeText)
        self.timer.start(50)
        self._taskbar.saveTextWidget.setText(displayText)

    def __fadeText(self):
        self.textOpac -= .022
        if self.textOpac <= 0:
            self.timer.stop()

        animval = min(max(255 * self.textOpac, 58), 255)
        self._taskbar.saveTextWidget.setStyleSheet(
            '''
            color: rgb(%d, %d, %d);
            font: 18pt;
            ''' % (animval, animval, animval)
            )

    def __closeEvent(self, e):
        self.setParent(None)
        self.deleteLater()

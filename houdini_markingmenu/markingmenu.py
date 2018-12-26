import time

import json

import os

import sys

import hou

from PySide2 import QtWidgets, QtGui, QtCore, QtTest

import utils

sys.path.insert(0, os.path.join(hou.getenv('HOUDINI_USER_PREF_DIR'),
                                'python2.7libs',
                                'houdini_markingmenu'))

import buttonfunctions as cmds

from widgets import mousepath, menuitembutton

# reload(cmds)
# reload(utils)
# reload(mousepath)
# reload(menuitembutton)


class NEMarkingMenu(QtWidgets.QWidget):
    """Display the marking menu in the network editor and run chosen function.

    Methods:
    __initUI -- create initial window, set invisible, grab mouse
    drawUI -- center window on cursor, draw buttons, path, and anchors
    storeCollection -- check keyboard modifiers, store json collection in memory
    createMenuButtons -- position, connect, and draw menu buttons
    createMousePath -- create mouse path
    displayWindowInitial -- simulates short delay before marking menu appears
    updateTargetWidget -- set target widget to button closest to cursor
    rebuildMenu -- destroy, rebuild, and redisplay menu buttons
    propagateMenu -- control forward and backward traversals
    updateMousePathWidget -- update mousepath and anchors on screen
    executeCommand -- click target widget
    mouseMoveEvent -- trigger above methods on mouse move events
    mouseReleaseEvent -- close menu
    closeEvent -- delete from memory

    Instance variables:
    visible -- button visibility (boolean)
    startTime -- time at menu creation for simulating delays (float)
    origin -- menu origin (QPoint)
    windowSize -- max invisible window bounds (int)
    editor -- target houdini network editor (hou network editor)
    mouseAnchorPositions -- path anchor joint positions (QPoint list)
    mousePathGraphicsWidget -- mouse path object (MousePathGraphics)
    menuItemWidgets -- button objects (QPushbutton list)
    rectangles -- button bounds (QRect list)
    menuYOffsets -- hardcoded offsets for button positions
    menuXOffsets -- hardcoded offsets for button positions
    targetWidget -- current highlighted button (QPushbutton)
    currentContext -- target houdini network editor context
    baseCollection -- current context's json file on disk (string)
    rootpath -- project directory
    inputConfigFile -- modifier preferences (dictionary)
    collectionItemDescriptions -- current json file in memory (dictionary list)
    collectionsDir -- path to current json file on disk
    """
    def __init__(self, editor):
        super(NEMarkingMenu, self).__init__()

        # UI fixed sizes
        self.HIGH_DPI = False
        self.UISCALE = 2 if self.HIGH_DPI else 1  # scale factor for high DPI monitors, 2 should be enough.

        self.windowSize = 1300 * self.UISCALE # invisible bounds size, too big may impact performance
        self.pad = 1.18 * self.UISCALE # gap between buttons
        self.buttonWidth = 110 * self.UISCALE
        self.buttonHeight = 24 * self.UISCALE
        self.buttonIconSize = 12 * self.UISCALE

        # menu draw time offset
        self.visible = False
        self.startTime = time.time()
        self.origin = QtCore.QPoint(0, 0)
        
        self.editor = editor

        # storing widgets - mouse path
        self.mouseAnchorPositions = []
        self.mousePathGraphicsWidget = 0

        # storing widgets - menu widgets
        self.menuItemWidgets = []
        self.rectangles = []
        
        self.targetWidget = 0

        # relative positional offsets between buttons
        self.menuYOffsets = [
            70*self.pad, 35*self.pad, 0*self.pad, -35*self.pad,
            -70*self.pad, -35*self.pad, 0*self.pad, 35*self.pad
            ]

        self.menuXOffsets = [
            0*self.pad, 45*self.pad, 70*self.pad, 45*self.pad,
            0*self.pad, 45*self.pad, 70*self.pad, 45*self.pad
            ]        

        # setup initial config file
        self.currentContext = utils.getContext(self.editor)
        self.baseCollection = '{}_baseCollection.json'.format(self.currentContext)

        self.rootpath = os.path.join(
            os.path.abspath(hou.getenv('HOUDINI_USER_PREF_DIR')),
            'python2.7libs',
            'houdini_markingmenu'
            )

        self.inputConfigFile = {}
        self.collectionItemDescriptions = []

        self.collectionsDir = os.path.join(self.rootpath, 'json', self.currentContext)
        self.storeCollection(self.baseCollection)
        self.__initUI()

    def __initUI(self):
        self.setParent(hou.qt.mainWindow(), QtCore.Qt.Window)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)

        self.setWindowFlags(
            self.windowFlags() |
            QtCore.Qt.FramelessWindowHint |
            QtCore.Qt.X11BypassWindowManagerHint
            )

        self.setFixedWidth(self.windowSize)
        self.setFixedHeight(self.windowSize)
        self.grabMouse()
        self.setFocus()
        self.setMouseTracking(True)
        self.drawUI()

    def drawUI(self):
        # center on cursor
        self.move(
            QtGui.QCursor.pos().x() - self.size().width()/2,
            QtGui.QCursor.pos().y() - self.size().height()/2
            )

        # init mouse anchor list with menu center
        if not len(self.mouseAnchorPositions):
            self.mouseAnchorPositions.append(QtCore.QPoint(
                self.size().width()/2,
                self.size().height()/2
                )
            )

        self.createMenuButtons(0)
        self.createMousePath()

        # set mouse tracking for all child widgets
        for i in self.children():
            i.setMouseTracking(True)

    def storeCollection(self, collectionFile):
        # close if config file not found
        if not os.path.isfile(os.path.join(self.collectionsDir, collectionFile)):
            self.close()
        else:
            # open prefs
            prefs = {}
            with open(
                os.path.join(
                    self.rootpath,
                    'json',
                    'menuprefs.json'), 'r') as f:
                prefs = json.load(f)

            modifiers = QtWidgets.QApplication.keyboardModifiers()
            if modifiers == QtCore.Qt.ShiftModifier:
                collectionFile = prefs[self.currentContext]['Shift']
            elif modifiers == QtCore.Qt.ControlModifier:
                collectionFile = prefs[self.currentContext]['Control']

            self.inputConfigFile = utils.loadCollection(
                os.path.join(self.rootpath, 'json', self.currentContext, collectionFile)
                )

            for item in self.inputConfigFile:
                self.collectionItemDescriptions.append(item)

    def createMenuButtons(self, anchorIndex):
        dummyMenu = QtWidgets.QMenu()
        center = self.mouseAnchorPositions[anchorIndex]
        for item in self.collectionItemDescriptions:
            if item['active']:
                index = item['index']

                a = item['label'].ljust(14 if (self.HIGH_DPI and item['isMenu']) else 2)

                btn = menuitembutton.MenuItemButton(uiscale=self.UISCALE, text=a, parent=self)
                if item['isMenu']:
                    btn.setMenu(dummyMenu)
                    btn.menu()
                    btn.isMenu = True
                    if os.path.isfile(os.path.join(self.collectionsDir, item['menuCollection'])):
                        btn.menuObjects = utils.loadCollection(
                            os.path.join(self.collectionsDir, item['menuCollection']))

                # button size, icon, icon size, position
                minx = self.buttonWidth
                maxy = self.buttonHeight
                try:
                    btn.setIcon(hou.qt.createIcon(item['icon'], 20, 20))
                    btn.setIconSize(QtCore.QSize(self.buttonIconSize, self.buttonIconSize))
                except hou.OperationFailed:
                    btn.setIcon(hou.qt.createIcon('COMMON_null', 20, 20))
                    btn.setIconSize(QtCore.QSize(self.buttonIconSize, self.buttonIconSize))

                s = btn.sizeHint()
                if s.width() < minx:
                    s.setWidth(minx)

                if s.height() > maxy or s.height() < maxy:
                    s.setHeight(maxy)

                btn.setFixedSize(s)
                xoffset = btn.geometry().width()/2 + self.menuXOffsets[index]
                if self.menuXOffsets[index] == 0:
                    xoffset = 0

                btncenter = QtCore.QPoint(
                    btn.size().width()/2 - xoffset,
                    btn.size().height()/2 + self.menuYOffsets[index]
                    )

                # subtract offset on left side
                if index >= 4:
                    btncenter = QtCore.QPoint(
                        btn.size().width()/2 + xoffset,
                        btn.size().height()/2 + self.menuYOffsets[index]
                        )

                btn.move(center - btncenter)
                btn.command = item['command']
                btn.editor = self.editor
                btn.nodetype = item['nodetype']
                btn.commandType = item['commandType']
                btn.activeWire = item['activeWire']
                btn.clicked.connect(btn.runCommand)
                btn.show()
                self.menuItemWidgets.append(btn)
                self.rectangles.append(btn.geometry())

    def createMousePath(self):
        # draw and store mouse path
        mousePath = mousepath.MousePathGraphics(self, self.mouseAnchorPositions, self.UISCALE)
        mousePath.setGeometry(0, 0, self.windowSize, self.windowSize)
        self.mousePathGraphicsWidget = mousePath

    def displayWindowInitial(self, e):
        # display window if delay has elapsed
        if not self.visible:
            if self.origin.x() == 0 and self.origin.y() == 0:
                self.origin = e.pos()
            if time.time() - self.startTime > .05:
                self.visible = True
                QtTest.QTest.mousePress(self, QtCore.Qt.RightButton)
                self.show()

    def updateTargetWidget(self, e):
        # find closest widget and do shading
        closeWidget = 0
        if utils.qpDist(self.mouseAnchorPositions[-1], e.pos()) > 14:
            distance = 99999
            idx = -1
            for i in self.rectangles:
                prd = utils.pointRectDist(e.pos(), i)
                self.menuItemWidgets[self.rectangles.index(i)].isTarget = False
                if prd < distance:
                    distance = prd
                    idx = self.rectangles.index(i)
            if len(self.menuItemWidgets):
                self.menuItemWidgets[idx].isTarget = True
                self.targetWidget = self.menuItemWidgets[idx]
                self.targetWidget.isUnder(e.pos())
        else:
            for i in self.rectangles:
                self.menuItemWidgets[self.rectangles.index(i)].isTarget = False
            self.targetWidget = 0

    def rebuildMenu(self, descriptionList):
        # remove button references from array, delete current buttons
        # descriptionList is a list of dictionaries
        for i in self.menuItemWidgets:
            i.deleteLater()

        # reset targetWidget and prepare to draw new buttons
        self.targetWidget = 0
        self.menuItemWidgets = []
        self.rectangles = []
        self.collectionItemDescriptions = descriptionList
        time.sleep(.015)
        self.createMenuButtons(len(self.mouseAnchorPositions)-1)

    def propagateMenu(self, e):
        if (self.targetWidget != 0 and
                self.targetWidget.underMouse and
                self.targetWidget.isMenu):
            # if menu has items in it
            if len(self.targetWidget.menuObjects):
                # store current configuration in case user wants to go back
                self.mousePathGraphicsWidget.previousMenu.append(
                    self.collectionItemDescriptions)

                # add new position for mouse path
                self.mouseAnchorPositions.append(e.pos())

                # stash menuObjects dict
                submenuItems = self.targetWidget.menuObjects
                self.rebuildMenu(submenuItems)

    def updateMousePathWidget(self, e):
        # update mouse path widget
        self.mousePathGraphicsWidget.updateCursor(e.pos())
        self.mousePathGraphicsWidget.raise_()

        if len(self.mouseAnchorPositions) > 1:
            if utils.qpDist(self.mouseAnchorPositions[-2], e.pos()) < 10:
                del self.mouseAnchorPositions[-1]
                self.rebuildMenu(self.mousePathGraphicsWidget.previousMenu[-1])

        # remove last item from list to track which menu we need to return to
                self.mousePathGraphicsWidget.previousMenu = \
                    self.mousePathGraphicsWidget.previousMenu[:-1]

    def executeCommand(self):
        self.targetWidget.click()

    def mouseMoveEvent(self, e):
        self.updateMousePathWidget(e)
        self.updateTargetWidget(e)
        self.propagateMenu(e)
        self.displayWindowInitial(e)
        self.update()

    def mouseReleaseEvent(self, e):
        # if self.visible:
        self.close()

    def closeEvent(self, e):
        self.releaseMouse()
        self.setParent(None)
        self.deleteLater()

        if self.targetWidget != 0 and not self.targetWidget.isMenu:
            self.executeCommand()
import sys
import hou
import time
import json
import os
import utils
<<<<<<< HEAD:nemarkingmenu/markingmenu.py
from math import sqrt
=======
>>>>>>> a7a97274a979e752d3a9f885369fd7c2f0922b70:nemarkingmenu/markingmenu.py
from PySide2 import QtWidgets, QtGui, QtCore, QtTest
import buttonfunctions as cmds
reload(cmds)
reload(utils)


class MousePathGraphics(QtWidgets.QWidget):
    def __init__(self, parentWidget, anchors_QPointsList):
        super(MousePathGraphics, self).__init__()

        self.anchors = anchors_QPointsList
        self.radius = 8.0
        self.width = 4.0
        self.cursor = QtCore.QPointF(QtGui.QCursor.pos())
        self.previousMenu = []

        self.setParent(parentWidget)
        self.setAttribute(QtCore.Qt.WA_TransparentForMouseEvents)

    def mouseMoveEvent(self, e):
        e.ignore()
        self.cursor = QtCore.QPointF(e.pos())

    def updateCursor(self, pos):
        self.cursor = QtCore.QPointF(pos)

    def paintEvent(self, e):
        qp = QtGui.QPainter(self)
        qp.setRenderHint(QtGui.QPainter.Antialiasing, True)
        self.drawLines(qp, self.anchors)
        self.drawCircles(qp, self.anchors)
        qp.end()

    def drawCircles(self, painter, QPointsList):
        pen = QtGui.QPen()
        painter.setPen(pen)

        brush = QtGui.QBrush(QtCore.Qt.SolidPattern)
        brush.setColor(QtGui.QColor(225, 225, 225))
        painter.setBrush(brush)

        for i in QPointsList:
            painter.drawEllipse(i, self.radius, self.radius)

    def drawLines(self, painter, QPointsList):
        pen = QtGui.QPen(QtCore.Qt.black, self.width, QtCore.Qt.SolidLine)
        brush = QtGui.QBrush(QtCore.Qt.lightGray)
        brush.setColor(QtGui.QColor(13, 13, 13))
        pen.setBrush(brush)
        painter.setPen(pen)

        # draw static lines
        if len(QPointsList) > 1:
            for i in range(len(QPointsList)-1):
                painter.drawLine(
                    QtCore.QPointF(QPointsList[i]),
                    QtCore.QPointF(QPointsList[i + 1])
                    )

        # draw mouse line
        window_width = 500
        fade_dist = 250.0

        a = QtCore.QPointF(self.cursor - QtCore.QPointF(QPointsList[-1]))
        dist = sqrt(a.x() * a.x() + a.y() * a.y())
        norm_a = a / dist

        startP = QtCore.QPointF(QPointsList[-1]) + (norm_a)*fade_dist
        limitP = startP
        if dist > fade_dist:
            a = window_width - 380
            step = 5.0
            startval = 13
            endval = 50 - startval
            count = a / step
            for i in range(int(count)):
                val = startval + ((endval / count) * i)
                endP = startP + norm_a * step

                x = endP - QtCore.QPointF(QPointsList[-1])
                dist2 = sqrt(x.x()*x.x() + x.y()*x.y())
                if dist2 <= dist:
                    brush.setColor(QtGui.QColor(val, val, val))
                    pen.setBrush(brush)
                    painter.setPen(pen)
                    painter.drawLine(startP, endP)
                    startP = endP

            brush.setColor(QtGui.QColor(13, 13, 13))
            pen.setBrush(brush)
            painter.setPen(pen)

            painter.drawLine(
                QtCore.QPointF(QPointsList[-1]),
                QtCore.QPoint(limitP.x(), limitP.y())
                )

        else:
            painter.drawLine(QtCore.QPointF(QPointsList[-1]), self.cursor)


class MenuItemButton(QtWidgets.QPushButton):
    def __init__(self, *args, **kwargs):
        super(MenuItemButton, self).__init__(*args, **kwargs)
        self.style = hou.qt.styleSheet()
        self.underMouse = 0
        self.command = ''
        self.isMenu = False
        self.menuObjects = []
        self.isTarget = False

        # new variables to support passing the editor through
        self.editor = 0
        self.commandType = 'createnode'
        self.nodetype = 'nodetype'
        self.activeWire = False

    def isUnder(self, pos):
        if self.geometry().contains(pos):
            if not self.underMouse:
                self.underMouse = 1
        else:
            if self.underMouse:
                self.underMouse = 0

    def paintEvent(self, e):
        super(MenuItemButton, self).paintEvent(e)
        if self.isTarget:
            self.setStyleSheet('''background-color: rgb(255,149,0);
                                    color: rgb(25,25,25);''')
        else:
            self.setStyleSheet(hou.qt.styleSheet())

    def runCommand(self):
        exec(self.command)

<<<<<<< HEAD:nemarkingmenu/markingmenu.py

class NEMarkingMenu(QtWidgets.QWidget):
    def __init__(self, editor):
        super(NEMarkingMenu, self).__init__()

=======

class NEMarkingMenu(QtWidgets.QWidget):
    def __init__(self):
        super(NEMarkingMenu, self).__init__()

>>>>>>> a7a97274a979e752d3a9f885369fd7c2f0922b70:nemarkingmenu/markingmenu.py
        # for display offset
        self.visible = False
        self.startTime = time.time()
        self.origin = QtCore.QPoint(0, 0)
        self.windowSize = 1000
<<<<<<< HEAD:nemarkingmenu/markingmenu.py
        self.editor = editor
=======

>>>>>>> a7a97274a979e752d3a9f885369fd7c2f0922b70:nemarkingmenu/markingmenu.py
        # for storing widgets - mouse path
        self.mouseAnchorPositions = []
        self.mousePathGraphicsWidget = 0

        # for storing widgets - menu widgets
        self.menuItemWidgets = []
        self.rectangles = []
        pad = 1.18

        self.menuYOffsets = [
            70*pad, 35*pad, 0*pad, -35*pad,
            -70*pad, -35*pad, 0*pad, 35*pad
            ]

        self.menuXOffsets = [
            0*pad, 45*pad, 70*pad, 45*pad,
            0*pad, 45*pad, 70*pad, 45*pad
            ]

        self.targetWidget = 0

        # setup initial config file
<<<<<<< HEAD:nemarkingmenu/markingmenu.py
        self.currentContext = utils.getContext(self.editor)
=======
        self.currentContext = utils.getContext()
>>>>>>> a7a97274a979e752d3a9f885369fd7c2f0922b70:nemarkingmenu/markingmenu.py
        self.baseCollection = '{}_baseCollection.json'.format(self.currentContext)

        self.rootpath = os.path.join(
            os.path.abspath(hou.getenv('HOUDINI_USER_PREF_DIR')),
            'python2.7libs',
            'nemarkingmenu'
            )

        self.inputConfigFile = {}
        self.collectionItemDescriptions = []
        self.storeCollection(self.baseCollection)

        self.initUI()

    def initUI(self):
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
        self.collectionsDir = os.path.join(self.rootpath, 'json', self.currentContext)
        # close if config file not found
        if not os.path.isfile(os.path.join(self.collectionsDir, collectionFile)):
            print 'collections missing in this context'
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
        # generate initial menu
        dummyMenu = QtWidgets.QMenu()

        center = self.mouseAnchorPositions[anchorIndex]

        for item in self.collectionItemDescriptions:
            if item['active']:
                index = item['index']
                btn = MenuItemButton(item['label'] + '  ', self)

                if item['isMenu']:
                    btn.setMenu(dummyMenu)
                    btn.menu()
                    btn.isMenu = True
                    btn.menuObjects = utils.loadCollection(
                        os.path.join(self.collectionsDir, item['menuCollection']))

                # button size, icon, icon size, position
                minx = 110
                maxy = 24
<<<<<<< HEAD:nemarkingmenu/markingmenu.py
                try:
                    btn.setIcon(hou.qt.createIcon(item['icon'], 20, 20))
                    btn.setIconSize(QtCore.QSize(12, 12))
                except hou.OperationFailed:
                    btn.setIcon(hou.qt.createIcon('COMMON_null', 20, 20))
                    btn.setIconSize(QtCore.QSize(12, 12))

=======
                btn.setIcon(hou.qt.createIcon(item['icon'], 20, 20))
                btn.setIconSize(QtCore.QSize(12, 12))
>>>>>>> a7a97274a979e752d3a9f885369fd7c2f0922b70:nemarkingmenu/markingmenu.py
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

                # subtract offset if left side
                if index >= 4:
                    btncenter = QtCore.QPoint(
                        btn.size().width()/2 + xoffset,
                        btn.size().height()/2 + self.menuYOffsets[index]
                        )

                btn.move(center - btncenter)
                btn.command = item['command']
                # new lines for passing the editor through for cmds
                btn.nodetype = item['nodetype']
                btn.commandType = item['commandType']
                btn.activeWire = item['activeWire']
                if item['commandType'] == 'createnode':
                    btn.clicked.connect(self.testCmd)
                else:
                    # end new lines
                    btn.clicked.connect(btn.runCommand)
                btn.show()
                self.menuItemWidgets.append(btn)
                self.rectangles.append(btn.geometry())

    def createMousePath(self):
        # draw and store mouse path
        mousePath = MousePathGraphics(self, self.mouseAnchorPositions)
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
<<<<<<< HEAD:nemarkingmenu/markingmenu.py
        time.sleep(.015)
=======
        time.sleep(.032)
>>>>>>> a7a97274a979e752d3a9f885369fd7c2f0922b70:nemarkingmenu/markingmenu.py
        self.createMenuButtons(len(self.mouseAnchorPositions)-1)

    def propagateMenu(self, e):
        if (self.targetWidget != 0 and
                self.targetWidget.underMouse and
                self.targetWidget.isMenu):
            # store current configuration in case user wants to go back
<<<<<<< HEAD:nemarkingmenu/markingmenu.py
            self.mousePathGraphicsWidget.previousMenu.append(
                self.collectionItemDescriptions)
=======
            self.mousePathGraphicsWidget.previousMenu = self.collectionItemDescriptions
>>>>>>> a7a97274a979e752d3a9f885369fd7c2f0922b70:nemarkingmenu/markingmenu.py

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

    def testCmd(self):
        cmds.createNode(
            self.targetWidget.nodetype, self.editor, self.targetWidget.activeWire)

    def executeCommand(self):
<<<<<<< HEAD:nemarkingmenu/markingmenu.py
        self.targetWidget.click()
=======
        # run the targetWidget's command
        self.targetWidget.click()
        # None
>>>>>>> a7a97274a979e752d3a9f885369fd7c2f0922b70:nemarkingmenu/markingmenu.py

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

import sys, hou, time, json, os
from math import sqrt
from PySide2 import QtWidgets, QtGui, QtCore, QtTest
import NE_markingMenu_buttonFunctions as cmds
reload(cmds)

class MousePathGraphics(QtWidgets.QWidget):
    def __init__(self, parentWidget, anchors_QPointsList):
        super(MousePathGraphics, self).__init__()

        self.anchors = anchors_QPointsList
        self.radius = 8.0
        self.width = 5.0
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
        brush.setColor(QtGui.QColor(225,225,225))
        painter.setBrush(brush)

        for i in QPointsList:
            painter.drawEllipse(i, self.radius, self.radius)

    def drawLines(self, painter, QPointsList):
        pen = QtGui.QPen(QtCore.Qt.black, self.width, QtCore.Qt.SolidLine)
        brush = QtGui.QBrush(QtCore.Qt.lightGray)
        brush.setColor(QtGui.QColor(13,13,13))
        pen.setBrush(brush)
        painter.setPen(pen)

        #draw static lines
        if len(QPointsList) > 1:
            for i in range(len(QPointsList)-1):
                painter.drawLine(QtCore.QPointF(QPointsList[i]), QtCore.QPointF(QPointsList[i+1]))

        #draw mouse line
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
            endval = 51 - startval
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

            brush.setColor(QtGui.QColor(13,13,13))
            pen.setBrush(brush)
            painter.setPen(pen)

            painter.drawLine(QtCore.QPointF(QPointsList[-1]), QtCore.QPoint(limitP.x(), limitP.y()))

        else:
            painter.drawLine(QtCore.QPointF(QPointsList[-1]), self.cursor)

class MenuItemButton(QtWidgets.QPushButton):
    def __init__(self, *args, **kwargs):
        super(MenuItemButton, self).__init__(*args, **kwargs)
        self.style = hou.qt.styleSheet()
        self.underMouse = 0
        self.command = ''
        self.isMenu = False
        self.menuObjects = {}
        self.isTarget = False

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

class NE_MarkingMenu(QtWidgets.QWidget):
    def __init__(self):
        super(NE_MarkingMenu, self).__init__()

        #for display offset
        self.visible = False
        self.startTime = time.time()
        self.origin = QtCore.QPoint(0,0)
        self.windowSize = 1000

        #for storing widgets - mouse path
        self.mouseAnchorPositions = []
        self.mousePathGraphicsWidget = 0

        #for storing widgets - menu widgets
        self.menuItemWidgets = []
        self.rectangles = []
        pad = 1.18
        self.menuYOffsets = [70*pad, 35*pad, 0*pad, -35*pad, -70*pad, -35*pad, 0*pad, 35*pad]
        self.menuXOffsets = [0*pad, 45*pad, 70*pad, 45*pad, 0*pad, 45*pad, 70*pad, 45*pad]
        self.targetWidget = 0

        #setup initial config file
        self.context = self.getContext()
        self.inputFile = '%s_baseCollection.collection' % self.context
        self.inputConfigFile = {}
        self.collectionItemDescriptions = []
        self.loadCollection(self.inputFile)

        self.initUI()

    def initUI(self):
        self.setParent(hou.qt.mainWindow(), QtCore.Qt.Window)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        #self.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)
        self.setWindowFlags(self.windowFlags() | QtCore.Qt.FramelessWindowHint | QtCore.Qt.X11BypassWindowManagerHint)
        self.setFixedWidth(self.windowSize)
        self.setFixedHeight(self.windowSize)
        self.grabMouse()
        self.setFocus()
        self.setMouseTracking(True)
        self.drawUI()

    def drawUI(self):
        #center on cursor
        self.move(QtGui.QCursor.pos().x() - self.size().width()/2, QtGui.QCursor.pos().y() - self.size().height()/2)

        #init mouse anchor list with menu center
        if not len(self.mouseAnchorPositions):
            self.mouseAnchorPositions.append(QtCore.QPoint(self.size().width()/2, self.size().height()/2))

        self.createMenuButtons(0)
        self.createMousePath()

        #set mouse tracking for all child widgets
        for i in self.children():
            i.setMouseTracking(True)

    def getContext(self):
        hou_context = hou.ui.paneTabOfType(hou.paneTabType.NetworkEditor).pwd().childTypeCategory().name()
        if hou_context == 'Sop':
            return 'SOP'
        elif hou_context == 'Object':
            return 'OBJ'
        elif hou_context == 'Driver':
            return 'ROP'
        elif hou_context == 'ChopNet':
            return 'CHOP'
        elif hou_context == 'Vop':
            return 'VOP'
        elif hou_context == 'Shop':
            return 'SHOP'
        elif hou_context == 'CopNet':
            return 'COP'

    def loadCollection(self, collectionFile):
        self.collectionsDir = hou.getenv('HOUDINI_USER_PREF_DIR')+'/python2.7libs/ne_mm_libs/collections/'

        #close if config file not found
        if not os.path.isfile(self.collectionsDir+collectionFile):
            print 'collections missing in this context'
            self.close()
        else:
            #open prefs
            prefs = {}
            with open(self.collectionsDir.split('collections/')[0] + 'menuprefs.prefs', 'r') as f:
                prefs = json.load(f)

            modifiers = QtWidgets.QApplication.keyboardModifiers()
            if modifiers == QtCore.Qt.ShiftModifier:
                collectionFile = prefs[self.context]['Shift']
            elif modifiers == QtCore.Qt.ControlModifier:
                collectionFile = prefs[self.context]['Control']

            with open(self.collectionsDir+collectionFile, 'r') as f:
                self.inputConfigFile = json.load(f)

            for a in range(len(self.inputConfigFile)):
                self.collectionItemDescriptions.append(self.inputConfigFile['collectionItem%s'%a])

    def createMenuButtons(self, anchorIndex):
        #generate initial menu
        dummyMenu = QtWidgets.QMenu()

        #center = QtCore.QPoint(self.size().width()/2, self.size().height()/2)
        center = self.mouseAnchorPositions[anchorIndex]

        for i in range(len(self.collectionItemDescriptions)):
            item = self.collectionItemDescriptions[i]
            if item != None:
                index = item['index']
                btn = MenuItemButton(item['label'] + '  ', self)

                if item['isMenu']:
                    btn.setMenu(dummyMenu)
                    btn.menu()
                    btn.isMenu = True
                    with open(self.collectionsDir + item['menuCollection'], 'r') as f:
                        btn.menuObjects = json.load(f)

                #button size, icon, icon size, position
                minx = 110
                maxy = 24
                btn.setIcon(hou.qt.createIcon(item['icon'], 20, 20))
                btn.setIconSize(QtCore.QSize(12,12))
                s = btn.sizeHint()
                if s.width() < minx:
                    s.setWidth(minx)
                if s.height() > maxy or s.height() < maxy:
                    s.setHeight(maxy)
                btn.setFixedSize(s)

                xoffset = btn.geometry().width()/2 + self.menuXOffsets[index]
                if self.menuXOffsets[index] == 0:
                    xoffset = 0
                btncenter = QtCore.QPoint(btn.size().width()/2 - xoffset, btn.size().height()/2 + self.menuYOffsets[index])

                #subtract offset if left side
                if index >= 4:
                    btncenter = QtCore.QPoint(btn.size().width()/2 + xoffset, btn.size().height()/2 + self.menuYOffsets[index])

                btn.move(center - btncenter)
                btn.command = item['command']
                btn.clicked.connect(btn.runCommand)
                btn.show()
                self.menuItemWidgets.append(btn)
                self.rectangles.append(btn.geometry())

    def createMousePath(self):
        #draw and store mouse path
        mousePath = MousePathGraphics(self, self.mouseAnchorPositions)
        mousePath.setGeometry(0,0,self.windowSize,self.windowSize)
        self.mousePathGraphicsWidget = mousePath

    def displayWindowInitial(self, e):
        #display window if delay has elapsed
        if not self.visible:
            if self.origin.x() == 0 and self.origin.y() == 0:
                self.origin = e.pos()
            if time.time() - self.startTime > .1:
                self.visible = True
                QtTest.QTest.mousePress(self, QtCore.Qt.RightButton)
                self.show()

    def updateTargetWidget(self, e):
        #find closest widget and do shading
        closeWidget = 0
        if self.qpDist(self.mouseAnchorPositions[-1], e.pos()) > 14:
            distance = 99999
            idx = -1
            for i in self.rectangles:
                prd = self.pointRectDist(e.pos(), i)
                self.menuItemWidgets[self.rectangles.index(i)].isTarget = False
                if prd < distance:
                    distance = prd
                    idx = self.rectangles.index(i)
            self.menuItemWidgets[idx].isTarget = True
            self.targetWidget = self.menuItemWidgets[idx]
            self.targetWidget.isUnder(e.pos())
        else:
            for i in self.rectangles:
                self.menuItemWidgets[self.rectangles.index(i)].isTarget = False
            self.targetWidget = 0

    def rebuildMenu(self, descriptionList):
        #remove button references from array, delete current buttons
        #descriptionList is a list of dictionaries
        for i in self.menuItemWidgets:
            i.deleteLater()

        #reset targetWidget and prepare to draw new buttons
        self.targetWidget = 0
        self.menuItemWidgets = []
        self.rectangles = []
        self.collectionItemDescriptions = descriptionList
        time.sleep(.025)
        self.createMenuButtons(len(self.mouseAnchorPositions)-1)

    def propagateMenu(self, e):
        if self.targetWidget != 0 and self.targetWidget.underMouse and self.targetWidget.isMenu:
            #store current configuration in case user wants to go back
            self.mousePathGraphicsWidget.previousMenu = self.collectionItemDescriptions

            #add new position for mouse path
            self.mouseAnchorPositions.append(e.pos())

            #stash menuObjects dict
            submenuItems = self.targetWidget.menuObjects.values()
            self.rebuildMenu(submenuItems)

    def updateMousePathWidget(self, e):
        #update mouse path widget
        self.mousePathGraphicsWidget.updateCursor(e.pos())
        self.mousePathGraphicsWidget.raise_()

        if len(self.mouseAnchorPositions) > 1:
            if self.qpDist(self.mouseAnchorPositions[-2], e.pos()) < 10:
                del self.mouseAnchorPositions[-1]
                self.rebuildMenu(self.mousePathGraphicsWidget.previousMenu)

    def executeCommand(self):
        #run the targetWidget's command
        self.targetWidget.click()
        #None

    def mouseMoveEvent(self, e):
        self.updateMousePathWidget(e)
        self.updateTargetWidget(e)
        self.propagateMenu(e)
        self.displayWindowInitial(e)
        self.update()

    def mouseReleaseEvent(self, e):
        if self.visible:
            self.close()

    def closeEvent(self, e):
        self.releaseMouse()
        self.setParent(None)
        self.deleteLater()

        if self.targetWidget != 0 and not self.targetWidget.isMenu:
            self.executeCommand()

    def pointRectDist(self, pos, rect):
        #pos = QtCore.QPoint, rect= QtCore.QRect
        #return the distance from pos to rect
        x = pos.x()
        y = pos.y()
        rx = rect.topLeft().x()
        ry = rect.topLeft().y()
        width = rect.width()
        height = rect.height()
        cx = max(min(x, rx+width), rx)
        cy = max(min(y, ry+height), ry)
        return sqrt((x - cx)*(x - cx) + (y - cy)*(y - cy))

    def qpDist(self, pt0, pt1):
        #QtCore.QPoints
        a = hou.Vector2(pt0.x(), pt0.y())
        b = hou.Vector2(pt1.x(), pt1.y())
        return a.distanceTo(b)
import sys, hou
#on work machines use this line
from PySide import QtGui, QtCore, QtTest

#on home machine use this line
#from PySide2 import QtWidgets, QtGui, QtCore, QtTest
        
#QtGui to QWidgets if pyside2
class MousePathGraphics(QtGui.QWidget):
    def __init__(self, parentWidget, anchors_QPointsList):
        super(MousePathGraphics, self).__init__()

        self.anchors = anchors_QPointsList
        self.radius = 8.0
        self.width = 5.0
        self.cursor = QtGui.QCursor.pos()
        self.setParent(parentWidget) 
        
    def mouseMoveEvent(self, e):
        #ignore allows the event to travel to parent widget
        e.ignore()
        print 'mouseMoveEvent from inside widget'
        
        #update cursor position for trail
        self.cursor = e.pos()            
        self.update()
        
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
        brush.setColor(QtGui.QColor(35,37,40))        
        pen.setBrush(brush)
        
        painter.setPen(pen)        

        #draw static lines
        if len(QPointsList) > 1:
            for i in range(len(QPointsList)-1):
                painter.drawLine(QPointsList[i], QPointsList[i+1])

        #draw mouse line
        painter.drawLine(QPointsList[-1], self.cursor)

# replaced QtWidgets with QtGui
class MenuItemButton(QtGui.QPushButton):
    def __init__(self, *args, **kwargs):
        super(MenuItemButton, self).__init__(*args, **kwargs)
        self.style = hou.qt.styleSheet()
        
# replaced QtWidgets with QtGui
class TestWindow(QtGui.QWidget):    
    def __init__(self):
        super(TestWindow, self).__init__()
        
        # replaced QtWidgets with QtGui
        for entry in QtGui.qApp.allWidgets():
            if type(entry).__name__ == 'TestWindow':
                print 'found a test menu' 
        
        self.mouseAnchorPositions = []
        self.mousePathGraphicsWidget = 0
        
        #menuItems = list of dictionaries, each dict needs to hold enough info to create a button 
        temp0 = {'type': QtGui.QPushButton, 'isMenu': True, 'label': 'Null', 'icon': 'MISC_python', 'command': 'print command executed'}
        temp1 = {'type': QtGui.QPushButton, 'isMenu': False, 'label': 'Merge Selected', 'icon': 'MISC_python', 'command': 'print command executed'}
        temp2 = {'type': QtGui.QPushButton, 'isMenu': True, 'label': 'Wrangles', 'icon': 'MISC_python', 'command': 'print command executed'}
        
        self.menuItems = [temp0,temp2,temp2,temp1,temp1,temp2,temp2,temp0]
        self.menuWidgets = []
        pad = 0        
        self.menuYOffsets = [70+pad, 35+pad, 0+pad, -35+pad, -70+pad, -35+pad, 0+pad, 35+pad]
        self.menuXOffsets = [0, 45, 70, 45, 0, 45, 70, 45]
        
        self.setMouseTracking(True)
        #self.grabMouse()
        self.initUI()
        
    def initUI(self):    
        self.setParent(hou.qt.mainWindow(), QtCore.Qt.Window)
        self.setWindowFlags(self.windowFlags() | QtCore.Qt.FramelessWindowHint)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)        
              
        self.move(300, 350)
        #btn = QtGui.QPushButton("testButton", self)
        #print type(btn) == QtGui.QPushButton
        self.setFixedWidth(600)
        self.setFixedHeight(300)        
        
        self.drawUI()
        
    def drawUI(self):
        center = QtCore.QPoint(self.size().width()/2, self.size().height()/2)
        #init mouse anchor list with menu center
        if not len(self.mouseAnchorPositions):
            self.mouseAnchorPositions.append(QtCore.QPoint(self.size().width()/2, self.size().height()/2))

        #generate initial menu
        dummyMenu = QtGui.QMenu()
        for i in range(len(self.menuItems)):
            item = self.menuItems[i]            
            if item['type'] == QtGui.QPushButton:
                btn = MenuItemButton(item['label'] + '  ', self)
                
                if item['isMenu']:
                    btn.setMenu(dummyMenu)
                    btn.menu()

                self.menuWidgets.append(btn)                
                
                #button size, icon, icon size, position
                btn.setMinimumSize(120, 0)
                btn.setMaximumSize(5000, 30)
                btn.setIcon(hou.qt.createIcon(item['icon'], 20, 20))
                btn.setIconSize(QtCore.QSize(12,12))                   
                
                s = btn.sizeHint()
                
                if s.width() < 120: 
                    s.setWidth(120)
                if s.height() > 24 or s.height() < 24:
                    s.setHeight(24)
                    
                btn.setFixedSize(s)
                
                xoffset = btn.geometry().width()/2 + self.menuXOffsets[i]
                
                if self.menuXOffsets[i] == 0:
                    xoffset = 0 
                
                btncenter = QtCore.QPoint(btn.size().width()/2 - xoffset, btn.size().height()/2 + self.menuYOffsets[i])
                
                #mirror if left side
                if i >= 4:
                    btncenter = QtCore.QPoint(btn.size().width()/2 + xoffset, btn.size().height()/2 + self.menuYOffsets[i])
                
                btn.move(center - btncenter)                
        
        #draw and store mouse path
        mousePath = MousePathGraphics(self, self.mouseAnchorPositions)
        self.mousePathGraphicsWidget = mousePath
        
        #set mouse tracking for all child widgets
        for i in self.children():
            i.setMouseTracking(True)
        
        self.run()       
        
    def closeEvent(self, e):
        print 'closed a test window'
        self.setParent(None)
        self.deleteLater()
        
    def mousePressEvent(self, e):        
        self.close()       
        
    def mouseMoveEvent(self, e):
        print 'mouseMoveEvent from main widget'                
        self.update()
        
    def run(self):
        self.show()
        
        
for entry in QtGui.qApp.allWidgets():
    if type(entry).__name__ == 'TestWindow':
        entry.setParent(None)
        entry.close()
print hou.qt.styleSheet()    
ex = TestWindow()

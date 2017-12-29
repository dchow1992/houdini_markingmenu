import sys
from PySide2 import QtGui, QtCore
from PySide2 import QtWidgets

class LineWidget(QtWidgets.QWidget):
    def __init__(self, QPoint_start):
        super(LineWidget, self).__init__()
        
        self.start = QPoint_start
        self.end = QtGui.QCursor.pos()
        self.width = 5
        
    def paintEvent(self, e):
        qp = QtGui.QPainter(self)
        qp.setRenderHint(QtGui.QPainter.Antialiasing, True)
        
        pen = QtGui.QPen(QtCore.Qt.black, self.width, QtCore.Qt.SolidLine)
        
        brush = QtGui.QBrush(QtCore.Qt.lightGray)
        brush.setColor(QtGui.QColor(35,37,40))        
        pen.setBrush(brush)
        
        qp.setPen(pen)        
        qp.drawLine(self.start, self.end)
        
        qp.end()
        
class CircleWidget(QtWidgets.QWidget):
    def __init__(self, QPoint_origin, radius):
        super(CircleWidget, self).__init__()
        
        self.origin = QPoint_origin
        self.radius = radius
            
    def paintEvent(self, e):
        qp = QtGui.QPainter(self)
        qp.setRenderHint(QtGui.QPainter.Antialiasing, True)
        
        pen = QtGui.QPen()
        qp.setPen(pen)
        
        brush = QtGui.QBrush(QtCore.Qt.SolidPattern)
        brush.setColor(QtGui.QColor(225,225,225))
        
        qp.setBrush(brush)
        qp.drawEllipse(self.origin, self.radius, self.radius)
        
        qp.end()
       
       
class TestWindow(QtWidgets.QWidget):
    
    def __init__(self):
        super(TestWindow, self).__init__()
        
        for entry in QtWidgets.qApp.allWidgets():
            if type(entry).__name__ == 'TestWindow':
                print 'found a test menu' 
        
        self.mouseAnchorPositions = []
        self.mouseAnchorWidgets = []
        self.mouseLineWidget = 0
        
        self.initUI()
        
    def initUI(self):    
        self.setParent(hou.qt.mainWindow(), QtCore.Qt.Window)
        self.setWindowFlags(self.windowFlags() | QtCore.Qt.FramelessWindowHint)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)        
        self.setMouseTracking(True)
        self.grabMouse()
        
        #vlayout = QtWidgets.QVBoxLayout()
        grid = QtWidgets.QGridLayout()
        grid.setSpacing(10)
        self.setLayout(grid)
        
        self.move(200, 350)
        self.setFixedWidth(600)
        self.setFixedHeight(300)
        self.setWindowTitle('')
        self.drawUI()        
        
    def drawUI(self):
        if not len(self.mouseAnchorPositions):
            self.mouseAnchorPositions.append(QtCore.QPoint(self.size().width()/2, self.size().height()/2))
            
        btn = QtWidgets.QPushButton("testButton")
        #vlayout.addWidget(btn)
        self.mouseAnchorPositions.append(QtCore.QPoint(self.size().width()/4, self.size().height()/4))        
        
        cursorLine = LineWidget(self.mouseAnchorPositions[-1])
        self.mouseLineWidget = cursorLine
        self.layout().addWidget(cursorLine, 6, 3, 1, 1) 
        
        
        
        for i in range(len(self.mouseAnchorPositions)):
            c = CircleWidget(self.mouseAnchorPositions[0], 8)
            self.mouseAnchorWidgets.append(c)
            self.layout().addWidget(c, 6, 3, 1, 1)
         
        
        
        
        self.run()
        
    def closeEvent(self, e):
        print 'closed a test window'
        self.setParent(None)
        self.deleteLater()
        
    def mousePressEvent(self, e):        
        self.close()
        
    def mouseMoveEvent(self, e):
        self.mouseLineWidget.end = e.pos()
        self.update()
        
    def run(self):
        self.show()
        
ex = TestWindow()

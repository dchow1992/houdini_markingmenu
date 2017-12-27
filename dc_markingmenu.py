import hou
from PySide2 import QtWidgets, QtGui, QtCore, QtTest
import time

class NE_MarkingMenu(QtWidgets.QWidget):
    def __init__(self):
        super(NE_MarkingMenu, self).__init__()

        self.cursor = QtGui.QCursor.pos() 
        self.visible = False
        self.width = 700
        self.height = 700
        self.center = (self.cursor.x() - self.width/2, self.cursor.y() - self.height/2)
        self.startTime = time.time()
        
        for entry in QtWidgets.qApp.allWidgets():
            if type(entry).__name__ == 'NE_MarkingMenu':
                print 'found a marking menu' 

        #self.setMouseTracking(True)
        self.initUI()
        
    def initUI(self):
        #self.setWindowTitle("test")
        self.setGeometry(self.center[0], self.center[1], self.width, self.height)
        self.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)
        self.cursor = QtCore.QPoint(0,0)
        self.grabMouse()
        QtTest.QTest.mousePress(self, QtCore.Qt.RightButton)        

    def mouseMoveEvent(self, e):
        #how much delay before drawing the marking menu
        self.pos = e.pos()        
        if not self.visible:
            if self.cursor.x() == 0 and self.cursor.y() == 0:
                self.cursor = e.pos()    
            if time.time() - self.startTime > .1:        
                self.visible = True                    
                self.run()

        self.update()
        
    def paintEvent(self, e):
        qp = QtGui.QPainter(self)
        self.drawMouseLine(qp)
        self.drawCenterCircle(qp)
        qp.end()

    def mouseReleaseEvent(self, e):
        print 'mouseReleaseEvent'
        self.releaseMouse()
        self.close()

    def closeEvent(self, e):
        print 'close event detected'
        self.setParent(None)
        self.deleteLater()

        ne = hou.ui.curDesktop().paneTabOfType(hou.paneTabType.NetworkEditor)       
        #twice because...the first one auto clicks for some reason.....
        position = ne.selectPosition()
        position = ne.selectPosition() 
        node = ne.pwd().createNode('null')
        node.move(position)

    def drawMouseLine(self, painter):
        pen = QtGui.QPen(QtCore.Qt.black, 6, QtCore.Qt.SolidLine)
        brush = QtGui.QBrush(QtCore.Qt.lightGray)
        brush.setColor(QtGui.QColor(35,37,40))        
        pen.setBrush(brush)
        painter.setPen(pen)
        painter.drawLine(self.pos, self.cursor)

    def drawCenterCircle(self, painter):
        pen = QtGui.QPen()
        pen.setStyle(QtCore.Qt.PenStyle(0))
        painter.setPen(pen)
        brush = QtGui.QBrush(QtCore.Qt.SolidPattern)
        brush.setColor(QtGui.QColor(225,225,225))
        painter.setBrush(brush)
        painter.drawEllipse(self.cursor, 10, 10)

    def run(self):
        self.show()


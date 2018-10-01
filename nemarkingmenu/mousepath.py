from math import sqrt
 
from Qt_py.Qt import QtWidgets, QtGui, QtCore
 
 
class MousePathGraphics(QtWidgets.QWidget):
    """Draws marking menu path graphics in the network editor.
 
    Methods:
    mouseMoveEvent -- update cursor position on event
    updateCursor -- force update cursor position
    paintEvent -- draw path and anchors
    drawCircles -- instructions to draw anchor joints
    drawLines -- instructions to draw path
 
    Instance variables:
    anchors -- joints in the current path (list of QPoints)
    radius -- radius of each anchor (float)
    width -- width of path (float)
    cursor -- cursor position (QPointF)
    previousMenu -- previous menu for backtracking (dictionary list)
    """
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

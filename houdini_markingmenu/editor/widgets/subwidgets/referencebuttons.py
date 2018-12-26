import hou

from PySide2 import QtWidgets, QtGui


class ReferenceButtons(QtWidgets.QWidget):
    def __init__(self, *args, **kwargs):
        super(ReferenceButtons, self).__init__()
        self.dpifactor = 2 if kwargs['highdpi'] else 1
        self.initUI()

    def initUI(self):
        self.layout = QtWidgets.QVBoxLayout()
        self.layout.addSpacing(80*self.dpifactor)

        h0 = QtWidgets.QHBoxLayout()
        self.layout.addLayout(h0)
        btn0 = QtWidgets.QPushButton('Item Slot 0', self)
        h0.addWidget(btn0)

        h1 = QtWidgets.QHBoxLayout()
        self.layout.addLayout(h1)
        btn1 = QtWidgets.QPushButton('Item Slot 7', self)
        h1.addWidget(btn1)
        h1.addSpacing(60*self.dpifactor)

        h2 = QtWidgets.QHBoxLayout()
        self.layout.addLayout(h2)
        btn2 = QtWidgets.QPushButton('Item Slot 6', self)
        h2.addWidget(btn2)

        h2.addSpacing(35*self.dpifactor)
        ref = QtWidgets.QLabel('                        ')
        self.backbtn = QtWidgets.QPushButton('', self)
        self.backbtn.setFixedSize(40 * self.dpifactor, 24 * self.dpifactor)
        self.backbtn.setIcon(hou.qt.Icon('BUTTONS_back'))
        self.backbtn.setStyleSheet(hou.qt.styleSheet())

        self.homebtn = QtWidgets.QPushButton('', self)
        self.homebtn.setFixedSize(40 * self.dpifactor, 24 * self.dpifactor)
        self.homebtn.setIcon(hou.qt.Icon('IMAGE_home'))
        self.homebtn.setStyleSheet(hou.qt.styleSheet())

        h2.addWidget(self.backbtn)
        h2.addSpacing(3*self.dpifactor)
        h2.addWidget(self.homebtn)
        h2.addSpacing(35*self.dpifactor)

        h3 = QtWidgets.QHBoxLayout()
        self.layout.addLayout(h3)
        btn3 = QtWidgets.QPushButton('Item Slot 5', self)
        h3.addWidget(btn3)
        h3.addSpacing(60*self.dpifactor)

        h4 = QtWidgets.QHBoxLayout()
        self.layout.addLayout(h4)
        btn4 = QtWidgets.QPushButton('Item Slot 4', self)
        h4.addWidget(btn4)

        btn5 = QtWidgets.QPushButton('Item Slot 3', self)
        h3.addWidget(btn5)

        btn6 = QtWidgets.QPushButton('Item Slot 2', self)
        h2.addWidget(btn6)

        btn7 = QtWidgets.QPushButton('Item Slot 1', self)
        h1.addWidget(btn7)

        self.btns = [btn0, btn7, btn6, btn5, btn4, btn3, btn2, btn1]

        for b in self.btns:
            b.setStyleSheet('''QPushButton
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
                            }''')
            b.setFixedSize(140 * self.dpifactor, 24 * self.dpifactor)

        self.layout.addSpacing(80*self.dpifactor)

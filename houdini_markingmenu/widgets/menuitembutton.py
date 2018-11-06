from PySide2 import QtWidgets

import hou

import toolutils

import sys

import os

import buttonfunctions as cmds

import reservedfunctions as cmdsreserved


class MenuItemButton(QtWidgets.QPushButton):
    """Subclassed pushbutton for marking menu.

    Methods:
    isUnder -- determine if button is under cursor
    paintEvent -- color change if under cursor
    runCommand -- execute command

    Instance variables:
    style -- button stylesheet (qt stylesheet)
    underMouse -- is button is under cursor (boolean)
    command -- function name to run (string)
    isMenu -- should button be treated as a menu (boolean)
    menuObjects -- menu items (dictionary list)
    isTarget -- is button under path or cursor (boolean)
    editor -- target houdini network editor (hou network editor)
    commandType -- create a node or run a custom function (string)
    nodetype -- houdini nodetype (string)
    activeWire -- picking input wire after node creation (boolean)
    """
    def __init__(self, *args, **kwargs):
        super(MenuItemButton, self).__init__(*args, **kwargs)
        self.style = hou.qt.styleSheet()
        self.underMouse = 0
        self.command = ''
        self.isMenu = False
        self.menuObjects = []
        self.isTarget = False
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
        if not self.isMenu:
            if self.command != 'createNode' and self.command != 'launchEditor':
                # buttonfunctions take precedence over toolscripts
                if self.command in cmds.__dict__:
                    func = cmds.__dict__[self.command]
                    func(nodetype=self.nodetype,
                         editor=self.editor,
                         activeWire=self.activeWire)
                else:
                    cmdsreserved.runShelfTool(self.command, self.editor, self.activeWire)

            elif self.command == 'createNode' or self.command == 'launchEditor':
                func = cmdsreserved.__dict__[self.command]
                func(nodetype=self.nodetype,
                     editor=self.editor,
                     activeWire=self.activeWire)

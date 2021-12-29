from PySide2 import QtWidgets

import hou

import toolutils

import sys

import os

import re

from .. import buttonfunctions as cmds

from .. import reservedfunctions as cmdsreserved


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
    def __init__(self, uiscale, *args, **kwargs):
        super(MenuItemButton, self).__init__(*args, **kwargs)
        self.UISCALE = uiscale
        self.underMouse = 0
        self.command = ''
        self.isMenu = False
        self.menuObjects = []
        self.isTarget = False
        self.editor = 0
        self.commandType = 'createnode'
        self.nodetype = 'nodetype'
        self.activeWire = False
        self.fontSize = int(12 * self.UISCALE)
        self.defaultStyle ='''\
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
                font-size: 23px;
            }'''
        self.defaultStyle = self.defaultStyle.replace('               font-size: 23px;', '                font-size: %dpx;' % self.fontSize)

        self.targetStyle ='''\
            QPushButton
            {
                background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                            stop: 0.0 rgb(255, 149, 0),
                            stop: 1.0 rgb(255, 149, 0));
                border-top: 1px solid rgba(0, 0, 0, 40%);
                border-right: 1px solid rgba(0, 0, 0, 40%);
                border-bottom: 1px solid rgba(0, 0, 0, 62%);
                border-left: 1px solid rgba(0, 0, 0, 40%);
                border-radius: 1px;
                color: rgb(25, 25, 25);
                padding-top: 3px;
                padding-right: 15px;
                padding-bottom: 3px;
                padding-left: 15px;
                font-size: 23px;
            }'''
        self.targetStyle = self.targetStyle.replace('               font-size: 23px;', '                font-size: %dpx;' % self.fontSize)

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
            self.setStyleSheet(self.targetStyle)
        else:
            self.setStyleSheet(self.defaultStyle)

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

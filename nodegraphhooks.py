import hou

#pyside gui
from PySide2 import QtWidgets, QtCore, QtGui
import dc_markingmenu as mm

#for houdini event handling
import mynodegraph as nodegraph
from canvaseventtypes import *

class NE_MarkingMenuMouseHandler(nodegraph.NodeMouseHandler):
    def handleEvent(self, uievent, pending_actions):
        if isinstance(uievent, MouseEvent) and uievent.eventtype == 'mousedrag':
            #hou.ui.displayMessage("I ran! I ran so far away!")
            #delete if a marking menu already exists

            '''
            for entry in QtWidgets.qApp.allWidgets():
                if type(entry).__name__ == 'NE_MarkingMenu':
                    entry.close()'''

            #generate window, parent to houdini main window
            markingMenu = mm.NE_MarkingMenu()
            markingMenu.setParent(hou.qt.mainWindow(), QtCore.Qt.Window)

            #end custom event handling, return None, otherwise return traditional nodegraph rmb handling
            return None

        return nodegraph.NodeMouseHandler.handleEvent(
            self, uievent, pending_actions)

'''we catch the mousedown event and then further handling is done by our custom class
createEventHandler catches mouse events and either does stuff and/or returns an eventHandler class with
a handleEvent() method that handles the events until completion of the event or hands it off to a different
handler''' 
def createEventHandler(uievent, pending_actions):
    if isinstance(uievent, MouseEvent) and \
       uievent.eventtype == 'mousedown' and \
       uievent.mousestate.rmb:
        return NE_MarkingMenuMouseHandler(uievent), True

    
    if isinstance(uievent, MouseEvent) and uievent.eventtype == 'mousedown':
        print 'houdini mousedown detected'

    return None, False
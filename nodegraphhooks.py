import os

import sys

sys.dont_write_bytecode = True

import hou

from houdini_markingmenu import markingmenu as mm

from canvaseventtypes import *

import nodegraphbase as base

sys.path.insert(0, os.path.join(hou.getenv('HOUDINI_USER_PREF_DIR'),
                'python2.7libs',
                'houdini_markingmenu'))

import buttonfunctions as cmds

def buildHandler(uievent, pending_actions):
    import nodegraph # to avoid circular imports
    class MarkingMenuMouseHandler(nodegraph.NodeMouseHandler):
        def handleEvent(self, uievent, pending_actions):
            if isinstance(uievent, MouseEvent) and uievent.eventtype == 'mousedrag':
                reload(mm)
                for entry in QtWidgets.QApplication.instance().allWidgets():
                    if type(entry).__name__ == 'NEMarkingMenu':
                        entry.setParent(None)
                        entry.close()
                markingMenu = mm.NEMarkingMenu(uievent.editor)
                # return None if we handled event and launched a marking menu
                return None
            # Return traditional nodegraph rmb handling if we didn't launch a marking menu
            # If an input, output, or dependancy arrow was right clicked, for example.
            return nodegraph.NodeMouseHandler.handleEvent(
                self, uievent, pending_actions)
    return MarkingMenuMouseHandler(uievent)

# We catch the mousedown event and then further handling is done by our custom class
# createEventHandler catches mouse events and either does stuff
# and/or returns an eventHandler class with a handleEvent() method that
# handles the events until completion of the event or hands it off to a different handler

# createEventHandler catches events (see "Extending the Network Editor docs page")
# every time an event is registered, we check to see if it's a right mouse button being held down
# if it is, we check to see if our menu variable is set to 1
# if our menu is on, then we call our custom function that wil ultimately open our menu window


def createEventHandler(uievent, pending_actions):
    if isinstance(uievent, MouseEvent) and uievent.eventtype == 'mousedown' and uievent.mousestate.rmb:
        reload(cmds)
        if uievent.selected.item is None:
            if cmds.MENU_ACTIVATE:
                a = buildHandler(uievent, pending_actions)
                return a, True
            else:
                return None, False
    return None, False

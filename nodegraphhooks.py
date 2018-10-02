import os
 
import sys
 
import hou
 
from houdini_markingmenu import markingmenu as mm
 
from houdini_markingmenu import markingmenunodegraph as nodegraph
 
from canvaseventtypes import *
 
import nodegraphbase as base
 
sys.path.insert(0, os.path.join(hou.getenv('HOUDINI_USER_PREF_DIR'),
                                'python2.7libs',
                                'houdini_markingmenu'))
 
import buttonfunctions as cmds
 
 
class MarkingMenuMouseHandler(nodegraph.NodeMouseHandler):
    def handleEvent(self, uievent, pending_actions):
        if isinstance(uievent, MouseEvent) and uievent.eventtype == 'mousedrag':
            reload(mm)
            markingMenu = mm.NEMarkingMenu(uievent.editor)
            # end custom event handling, return None
            # Otherwise return traditional nodegraph rmb handling
            return None
 
        return nodegraph.NodeMouseHandler.handleEvent(
            self, uievent, pending_actions)
 
 
# We catch the mousedown event and then further handling is done by our custom class
# createEventHandler catches mouse events and either does stuff
# and/or returns an eventHandler class with a handleEvent() method that
# handles the events until completion of the event or hands it off to a different handler
 
 
def createEventHandler(uievent, pending_actions):
    if isinstance(uievent, MouseEvent) and uievent.eventtype == 'mousedown' and uievent.mousestate.rmb:
 
        reload(cmds)
        if uievent.selected.item is None:
           if cmds.menu_activate == 1:
               return MarkingMenuMouseHandler(uievent), True
           else:
               return None, False
    return None, False

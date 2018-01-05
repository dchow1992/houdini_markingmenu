import hou
from ne_mm_libs import NE_markingMenu_ui as mm, NE_markingMenu_nodegraph as nodegraph
from canvaseventtypes import *

class NE_MarkingMenuMouseHandler(nodegraph.NodeMouseHandler):
    def handleEvent(self, uievent, pending_actions):
        if isinstance(uievent, MouseEvent) and uievent.eventtype == 'mousedrag':
            reload(mm)
            markingMenu = mm.NE_MarkingMenu()
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
        None
        #print 'houdini mousedown detected'

    return None, False
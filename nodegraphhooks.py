import hou
from nemarkingmenu import markingmenu as mm, markingmenunodegraph as nodegraph
from canvaseventtypes import *


class MarkingMenuMouseHandler(nodegraph.NodeMouseHandler):
    def handleEvent(self, uievent, pending_actions):
        if isinstance(uievent, MouseEvent) and uievent.eventtype == 'mousedrag':
            reload(mm)
<<<<<<< HEAD
            markingMenu = mm.NEMarkingMenu(uievent.editor)
=======
            markingMenu = mm.NEMarkingMenu()
>>>>>>> a7a97274a979e752d3a9f885369fd7c2f0922b70
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
    if isinstance(uievent, MouseEvent) and \
       uievent.eventtype == 'mousedown' and \
       uievent.mousestate.rmb:
        return MarkingMenuMouseHandler(uievent), True
    if isinstance(uievent, MouseEvent) and uievent.eventtype == 'mousedown':
        None

    return None, False

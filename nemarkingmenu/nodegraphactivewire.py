import hou
import nodegraphbase as base
import nodegraphdisplay as display
import nodegraphprefs as prefs
import nodegraphsnap as snap
import nodegraphutils as utils
import nodegraphview as view
from canvaseventtypes import *

def handleEvent(uievent, last_handler_coroutine):
    """
        Very simple handler to wait for the user to click a location in the
        network view.
    """
    handler_coroutine = last_handler_coroutine
    if handler_coroutine is None:
        handler_coroutine = handleEventCoroutine()
        next(handler_coroutine)

    # If we are here recursively as a result of the handler running some
    # code already, we have to skip this event.
    if not handler_coroutine.gi_running:
        try:
            handler_coroutine.send(uievent)
        except StopIteration:
            handler_coroutine = None

    return handler_coroutine

def sendEventToHandler(handler, uievent, shapes):
    result = handler.handleEvent(uievent, [])
    if not isinstance(result, base.EventHandler):
        result = None
    uievent.editor.setOverlayShapes(shapes)
    return result

def setEventContextData(contextdata, locatedconn, locatedinput, locatedoutput):
    # If the mouse is over a wire, we want to set both end of the connection.
    # If the mouse is over an input or output, and that end of the connection
    # isn't already established, we want to connect to the input or output
    # under the mouse.
    if locatedconn is not None:
        if contextdata['outputitem'] is None and \
           contextdata['inputitem'] is None:
            contextdata['inputitem'] = locatedconn.item.inputItem()
            contextdata['outputitem'] = locatedconn.item.outputItem()
            contextdata['inputindex'] = locatedconn.item.inputIndex()
            contextdata['outputindex'] = locatedconn.item.outputIndex()

    elif locatedinput is not None:
        allow_change = (contextdata['outputitem'] is None)
        if allow_change and not contextdata['branch']:
            if contextdata['inputitem'] is not None and \
               contextdata['outputindex'] >= 0:
               outputconns = contextdata['inputitem'].outputConnectors()[
                    contextdata['outputindex']]
               if outputconns:
                   allow_change = False
        if allow_change:
            contextdata['branch'] = True
            contextdata['outputitem'] = locatedinput.item
            if locatedinput.index >= 0:
                contextdata['inputindex'] = locatedinput.index
            else:
                input_conns = locatedinput.item.inputConnections()
                if input_conns:
                    contextdata['inputindex'] = input_conns[-1].inputIndex() + 1
                else:
                    contextdata['inputindex'] = 0

    elif locatedoutput is not None:
        allow_change = (contextdata['inputitem'] is None)
        if allow_change and not contextdata['branch']:
            if contextdata['outputitem'] is not None and \
               contextdata['inputindex'] >= 0:
               inputconns = contextdata['outputitem'].inputConnectors()[
                    contextdata['inputindex']]
               if inputconns:
                   allow_change = False
        if allow_change:
            contextdata['branch'] = True
            contextdata['inputitem'] = locatedoutput.item
            contextdata['outputindex'] = locatedoutput.index

def handleEventCoroutine():
    visiblebounds = hou.BoundingRect()
    halfsize = utils.getNewNodeHalfSize()
    minsize = min(halfsize.x(), halfsize.y())
    maxsize = max(halfsize.x(), halfsize.y())
    inputnames = ('input', 'multiinput', 'dotinput')
    outputnames = ('output', 'indirectinputoutput', 'dotoutput')
    alignrects = []
    shapes = []
    nodecenter = None
    locatedconn = None
    locatedinput = None
    locatedoutput = None
    handler = None
    editor = None
    olddefaultcursor = None

    while True:
        uievent = yield
        if editor is None:
            editor = uievent.editor
            olddefaultcursor = editor.defaultCursor()

        if handler is not None:
            handler = sendEventToHandler(handler, uievent, shapes)
            if handler is None:
                editor.setDefaultCursor(olddefaultcursor)
            continue

        newvisiblebounds = editor.visibleBounds()
        if visiblebounds != newvisiblebounds:
            alignrects = editor.allVisibleRects([])
            visiblebounds = newvisiblebounds

        if (isinstance(uievent, KeyboardEvent) or \
            isinstance(uievent, MouseEvent)):
            if nodecenter is None:
                nodecenter = uievent.mousepos
                nodecenter = editor.posFromScreen(nodecenter)

            # Check for a wire to drop the node on, if that pref is enabled.
            # Don't update the target on a mouse up event. We want to keep
            # the located/selected target from the last mouse event, since the
            # selected value gets cleared on the mouseup event.
            if prefs.allowDropOnWire(editor) and uievent.eventtype != 'mouseup':
                target = None
                if isinstance(uievent, MouseEvent) and \
                   uievent.selected.item is not None:
                    target = uievent.selected
                elif uievent.located.item is not None:
                    target = uievent.located
                locatedconn = None
                locatedinput = None
                locatedoutput = None
                if target is not None:
                    if isinstance(target.item, hou.NodeConnection):
                        locatedconn = target
                    elif target.name in inputnames:
                        locatedinput = target
                    elif target.name in outputnames:
                        locatedoutput = target
                if locatedconn is None and \
                   locatedinput is None and \
                   locatedoutput is None:
                    editor.setDefaultCursor(None)
                else:
                    editor.setDefaultCursor(utils.theCursorDragDropOn)

        if isinstance(uievent, KeyboardEvent):
            if uievent.eventtype.endswith('keyhit') and \
               display.setKeyPrompt(editor, uievent.key,
                                    'h.pane.wsheet.cancel', uievent.eventtype):
                break

            if uievent.eventtype.endswith('keyhit') and \
               display.setKeyPrompt(editor, uievent.key,
                                    'h.pane.wsheet.add_op', uievent.eventtype):
                # Indicate that the keyboard event should be sent again, which
                # will allow it to be handled by the parent context (and open
                # up the tab menu).
                editor.handleCurrentKeyboardEvent(True)
                break

            elif uievent.eventtype == 'keyhit' and uievent.key == 'Enter':
                editor.eventContextData()['pos'] = nodecenter - halfsize
                setEventContextData(editor.eventContextData(),
                    locatedconn, locatedinput, locatedoutput)
                break

            elif uievent.eventtype == 'keyhit' and uievent.key == 'Shift+Enter':
                editor.eventContextData()['pos'] = None
                setEventContextData(editor.eventContextData(),
                    locatedconn, locatedinput, locatedoutput)
                break

        elif isinstance(uievent, MouseEvent):
            if uievent.eventtype == 'mousewheel':
                view.scaleWithMouseWheel(uievent)

            elif uievent.eventtype == 'mousedown':
                if uievent.selected.name.startswith('overview'):
                    handler = base.OverviewMouseHandler(uievent)
                elif base.isPanEvent(uievent):
                    handler = base.ViewPanHandler(uievent)
                elif base.isScaleEvent(uievent):
                    handler = base.ViewScaleHandler(uievent)
                if handler is not None:
                    editor.setDefaultCursor(olddefaultcursor)
                    handler = sendEventToHandler(handler, uievent, shapes)

            elif uievent.eventtype == 'mouseup':
                editor.eventContextData()['pos'] = nodecenter - halfsize
                setEventContextData(editor.eventContextData(),
                    locatedconn, locatedinput, locatedoutput)
                break

            else:
                nodecenter = uievent.mousepos
                nodecenter = editor.posFromScreen(nodecenter)
                category = editor.pwd().childTypeCategory()
                # If we are showing a preview of the node shape, we need to
                # pass a large square to ensure the shape draws at the
                # expected size.

                if prefs.showNodeShapes(editor) and \
                   category != hou.vopNodeTypeCategory():
                    halfmaxsize = hou.Vector2(maxsize, maxsize)
                    rect = hou.BoundingRect(nodecenter - halfmaxsize,
                                            nodecenter + halfmaxsize)
                else:
                    rect = hou.BoundingRect(nodecenter - halfsize,
                                            nodecenter + halfsize)
                snapresult = snap.snap(editor, None, rect, alignrects)
                if snapresult.isValid():
                    nodecenter += snapresult.delta()
                    rect.translate(snapresult.delta())
                '''
                if prefs.showNodeShapes(editor):
                    nodeshape = ''
                    nodetypename = editor.eventContextData()['nodetypename']
                    if category is not None:
                        nodetype = category.nodeType(nodetypename)
                        if nodetype is not None:
                            nodeshape = nodetype.defaultShape()
                    shapes = [hou.NetworkShapeNodeShape(rect, nodeshape,
                                    hou.ui.colorFromName('GraphPreSelection'),
                                    0.5, True, False)]
                else:
                shapes = [hou.NetworkShapeBox(rect,
                                hou.ui.colorFromName('GraphPreSelection'),
                                0.5, True, False)]'''
                shapes = snapresult.shapes(editor)
                shapes.extend(buildPendingWires(editor, nodecenter, locatedconn, locatedinput, locatedoutput))

            editor.setOverlayShapes(shapes)

    if editor is not None:
        editor.setDefaultCursor(olddefaultcursor)
        editor.setOverlayShapes([])
        editor.popEventContext()

def buildPendingWires(editor, nodecenter,
                      locatedconn, locatedinput, locatedoutput):
    shapes = []
    contextdata = dict(editor.eventContextData())
    setEventContextData(contextdata, locatedconn, locatedinput, locatedoutput)
    inputitem = contextdata['inputitem']
    inputindex = contextdata['inputindex']
    outputitem = contextdata['outputitem']
    outputindex = contextdata['outputindex']
    branch = contextdata['branch']
    clr = hou.ui.colorFromName('GraphPreSelection')
    alpha = 1.0

    if inputitem is not None and outputitem is not None:
        outpos = editor.itemOutputPos(inputitem, outputindex)
        outdir = editor.itemOutputDir(inputitem, outputindex)
        inpos = editor.itemInputPos(outputitem, inputindex)
        indir = editor.itemInputDir(outputitem, inputindex)
        shapes.append(hou.NetworkShapeConnection(
                outpos, outdir, nodecenter, -outdir, clr, alpha))
        shapes.append(hou.NetworkShapeConnection(
                nodecenter, -indir, inpos, indir, clr, alpha))

    elif inputitem is not None:
        outpos = editor.itemOutputPos(inputitem, outputindex)
        outdir = editor.itemOutputDir(inputitem, outputindex)
        shapes.append(hou.NetworkShapeConnection(
                outpos, outdir, nodecenter, -outdir, clr, alpha))
        if not branch:
            conns = inputitem.outputConnections()
            for conn in conns:
                if conn.outputIndex() != outputindex:
                    continue
                inpos = editor.itemInputPos(
                        conn.outputItem(), conn.inputIndex())
                indir = editor.itemInputDir(
                        conn.outputItem(), conn.inputIndex())
                shapes.append(hou.NetworkShapeConnection(
                        nodecenter, -indir, inpos, indir, clr, alpha))

    elif outputitem is not None:
        conns = outputitem.inputConnections()
        inpos = editor.itemInputPos(outputitem, inputindex)
        indir = editor.itemInputDir(outputitem, inputindex)
        shapes.append(hou.NetworkShapeConnection(
                nodecenter, -indir, inpos, indir, clr, alpha))
        if not branch:
            for conn in conns:
                if conn.inputIndex() != inputindex:
                    continue
                outpos = editor.itemOutputPos(
                        conn.inputItem(), conn.inputItemOutputIndex())
                outdir = editor.itemOutputDir(
                        conn.inputItem(), conn.inputItemOutputIndex())
                shapes.append(hou.NetworkShapeConnection(
                        outpos, outdir, nodecenter, -outdir, clr, alpha))
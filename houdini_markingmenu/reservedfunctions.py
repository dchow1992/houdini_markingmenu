import hou

import toolutils

import menueditor as mm

from PySide2 import QtWidgets

reload(mm)

def createNode(**kwargs):
    """Create a node, place it, and pick input wire if activeWire is set."""
    if kwargs is not None:
        network_editor = kwargs['editor']
        try:
            scriptargs = {}
            scriptargs['pane'] = network_editor

            nodenames = []
            nodetypenames = []

            categories = hou.nodeTypeCategories()
            for category in categories.keys():
                node_types = categories[category].nodeTypes()
                for node_type in node_types.keys():
                    nodenames.append(node_types[node_type].nameComponents()[2])
                    nodetypenames.append(node_types[node_type].name())

            # for whatever reason, I had to call two functions to get the correct
            # interactions to pick up, so the first call to selectPosition() doesn't do anything
            network_editor.selectPosition()

            node = toolutils.genericTool(scriptargs, nodetypename=nodetypenames[nodenames.index(kwargs['nodetype'])])
            if kwargs['activeWire'] and len(network_editor.allVisibleRects(())):
                pickWire(node, network_editor)
        except hou.OperationInterrupted:
            pass


def runShelfTool(commandstr, editor, activeWire):
    # run first matching tool
    tools = hou.shelves.tools()
    for t in tools.keys():
        if t == commandstr:
            # dummy event first
            editor.selectPosition()
            toolutils.testTool(tools[t], pane=editor)
            if activeWire:
                node = hou.selectedNodes()[0]
                pickWire(node, editor)


def pickWire(node, network_editor):
    if not len(node.inputs()):
        data = {
                'connection': False,
                'inputitem': None,
                'inputindex': 0,
                'outputitem': node,
                'outputindex': 0,
                'branch': False,
                'nodetypename': None
                }
        network_editor.pushEventContext('nodegraphactivewire', data)
        node.setInput(0, data['inputitem'], data['outputindex'])
        network_editor.setCurrentNode(node)


def launchEditor(**kwargs):
    """Open the marking menu editor."""
    for entry in QtWidgets.qApp.allWidgets():
        if type(entry).__name__ == 'MarkingMenuEditor':
            entry.setParent(None)
            entry.close()
    ex = mm.MarkingMenuEditor()

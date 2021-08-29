from PySide2 import QtWidgets

import hou

import toolutils

import menueditor as editor

import utils

def createNode(**kwargs):
    """Create a node, place it, and pick input wire if activeWire is set."""
    if kwargs is not None:
        network_editor = kwargs['editor']
        try:
            scriptargs = {}
            scriptargs['pane'] = network_editor
            context = utils.getContext(network_editor)

            mapping = {
            'Sop':'Sop',
            'Object': 'Obj',
            'Driver': 'Rop',
            'Vop': 'Vop'            
            }

            # Issue #22: make sure latest version of each node is created
            version = 0
            categories = hou.nodeTypeCategories()
            nodes = []
            for category in categories.keys():
                compare = category
                if category in mapping:
                    compare = mapping[category]                
                if compare.lower() == context.lower():
                    node_types = categories[category].nodeTypes()
                    for node_type in node_types.keys():
                        components = node_types[node_type].nameComponents()
                        checklist = [kwargs['nodetype']]
                        matches = set(checklist).intersection(set(components))
                        if matches:                        
                            nodes.append(node_type)

            network_editor.selectPosition()

            node = toolutils.genericTool(scriptargs, nodetypename=nodes[-1])

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
            try:
                toolutils.testTool(tools[t], pane=editor)
                if activeWire:
                    node = hou.selectedNodes()[0]
                    pickWire(node, editor)
            except hou.OperationInterrupted:
                pass


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
    for entry in QtWidgets.QApplication.instance().allWidgets():
        if type(entry).__name__ == 'MarkingMenuEditor':
            entry.setParent(None)
            entry.close()
    ex = editor.MarkingMenuEditor(kwargs['editor'])

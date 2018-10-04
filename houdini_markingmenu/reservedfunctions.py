import hou
 
import menueditor as mm
 
from PySide2 import QtWidgets
 
 
def createNode(**kwargs):
    """Create a node, place it, and pick input wire if activeWire is set."""
    if kwargs is not None:
        network_editor = kwargs['editor']
        parm_view = hou.ui.paneTabOfType(hou.paneTabType.Parm)
 
        try:
            position = network_editor.selectPosition()
            position = network_editor.selectPosition()
            node = network_editor.pwd().createNode(kwargs['nodetype'])
            node.move(position)
            node.setSelected(True, clear_all_selected=True)
 
            if kwargs['activeWire']:
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
                node.setInput(0, data['inputitem'], data['inputindex'])
 
            network_editor.setCurrentNode(node)
        except hou.OperationInterrupted:
            pass
 
 
def launchEditor(**kwargs):
    """Open the marking menu editor."""
    for entry in QtWidgets.qApp.allWidgets():
        if type(entry).__name__ == 'MarkingMenuEditor':
            entry.setParent(None)
            entry.close()
    ex = mm.MarkingMenuEditor()

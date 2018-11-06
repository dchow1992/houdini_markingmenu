import sys
 
import os
 
import hou
 
import toolutils
 
sys.path.insert(0, os.path.join(os.environ['REZ_HOUDINI_MARKINGMENU_ROOT'], 'python', 'houdini_markingmenu'))
 
import reservedfunctions as cmdsreserved
 
''' Set menu_activate = 1 to turn on menu '''
menu_activate = 1
 
 
def assetImporter(**kwargs):
    """Open MAS browser."""
    from houdini_asset_importer import dialog
    dialog.show_dialog()
 
 
# Script Examples
 
def _mergeSelection(**kwargs):
    """Merge selected nodes and pick position."""
    if kwargs is not None:
        x = hou.selectedNodes()
        network_editor = kwargs['editor']
        try:
            # for whatever reason, I had to call two functions to get the correct
            # interactions to pick up, so the first call to selectPosition() doesn't do anything
            position = network_editor.selectPosition()
            position = network_editor.selectPosition()
 
            a = network_editor.pwd().createNode("merge")
 
            a.setPosition(position)
            if(len(x) > 0):
                for node in x:
                    a.setNextInput(node)
 
            network_editor.setCurrentNode(a)
            a.setSelected(True, clear_all_selected=1)
        except hou.OperationInterrupted:
            pass
 
 
def _objMergeSelection(**kwargs):
    """Object merge selected node and pick position."""
    if kwargs is not None:
        network_editor = kwargs['editor']
        try:
            # for whatever reason, I had to call two functions to get the correct
            # interactions to pick up, so the first call to selectPosition() doesn't do anything
            pos = network_editor.selectPosition()
            pos = network_editor.selectPosition()
 
            if(len(hou.selectedNodes()) > 0):
                x = hou.selectedNodes()[0]
 
                a = network_editor.pwd().createNode(
                        "object_merge", "ref_"+x.name()
                        )
                a.parm('objpath1').set(x.path())
            else:
                a = network_editor.pwd().createNode("object_merge")
 
            a.setPosition(pos)
            network_editor.setCurrentNode(a)
            a.setSelected(True, clear_all_selected=1)
        except hou.OperationInterrupted:
            pass
 
 
# SOP Toolscripts
 
def createDetailWrangle(**kwargs):
    """Create an attribute wrangle in detail mode, place it, and pick input wire."""
    if kwargs is not None:
        network_editor = kwargs['editor']
        try:
            scriptargs = {}
            scriptargs['pane'] = network_editor
 
            # for whatever reason, I had to call two functions to get the correct
            # interactions to pick up, so the first call to selectPosition() doesn't do anything
            network_editor.selectPosition()
 
            node = toolutils.genericTool(scriptargs, nodetypename='attribwrangle')
            node.parm('class').set(0)
            node.setName('detailwrangle1', True)
            if kwargs['activeWire'] and len(network_editor.allVisibleRects(())):
                cmdsreserved.pickWire(node, network_editor)
        except hou.OperationInterrupted:
            pass
 
 
def createDetailVOP(**kwargs):
    """Create an attribute vop in detail mode, place it, and pick input wire."""
    if kwargs is not None:
        network_editor = kwargs['editor']
        try:
            scriptargs = {}
            scriptargs['pane'] = network_editor
 
            # for whatever reason, I had to call two functions to get the correct
            # interactions to pick up, so the first call to selectPosition() doesn't do anything
            network_editor.selectPosition()
 
            node = toolutils.genericTool(scriptargs, nodetypename='attribvop')
            node.parm('bindclass').set(0)
            node.setName('detailvop1', True)
            if kwargs['activeWire'] and len(network_editor.allVisibleRects(())):
                cmdsreserved.pickWire(node, network_editor)
        except hou.OperationInterrupted:
            pass
 
 
# ROP Toolscripts
 
def createAfterJob(**kwargs):
    """Create a bind export and place it."""
    if kwargs is not None:
        network_editor = kwargs['editor']
 
        try:
            position = network_editor.selectPosition()
            position = network_editor.selectPosition()
 
            node = network_editor.pwd().createNode('rw_depend')
            node.move(position)
            node.setSelected(True, clear_all_selected=True)
            node.parm('dependency').set(2)
            node.setName('AfterJob1', unique_name=True)
            node.setColor(hou.Color(1, .6, .6))
            network_editor.setCurrentNode(node)
 
        except hou.OperationInterrupted:
            pass
 
 
def createFXRop(**kwargs):
    from houdini_render import mantra_rop
    if kwargs is not None:
        network_editor = kwargs['editor']
        try:
            position = network_editor.selectPosition()
            position = network_editor.selectPosition()
 
            # Actual create node
            node = network_editor.pwd().createNode('ifd', node_name='main')
 
            # Setup node
            mantra_rop.init_mantra_rop_with_preset(node, 'fx')
 
            node.move(position)
            node.setSelected(True, clear_all_selected=True)
            network_editor.setCurrentNode(node)
 
        except hou.OperationInterrupted:
            pass
 
 
def createLightRop(**kwargs):
    from houdini_render import mantra_rop
    if kwargs is not None:
        network_editor = kwargs['editor']
        try:
            position = network_editor.selectPosition()
            position = network_editor.selectPosition()
 
            # Actual create node
            node = network_editor.pwd().createNode('ifd', node_name='main')
 
            # Setup node
            mantra_rop.init_mantra_rop_with_preset(node, 'light')
 
            node.move(position)
            node.setSelected(True, clear_all_selected=True)
            network_editor.setCurrentNode(node)
 
        except hou.OperationInterrupted:
            pass

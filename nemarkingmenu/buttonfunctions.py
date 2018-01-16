import hou
<<<<<<< HEAD
import nodegraphactivewire
=======
>>>>>>> a7a97274a979e752d3a9f885369fd7c2f0922b70
from nemarkingmenu import menueditor as mm
from PySide2 import QtWidgets
reload(mm)


<<<<<<< HEAD
def createNode(node_name, editor, activeWire):
    network_editor = editor
    parm_view = hou.ui.paneTabOfType(hou.paneTabType.Parm)

    try:
        position = network_editor.selectPosition()
        position = network_editor.selectPosition()
        node = network_editor.pwd().createNode(node_name)
        node.move(position)
        node.setSelected(True, clear_all_selected=True)

        # if activeWire:
        #     data = {
        #             'connection': False,
        #             'inputitem': None,
        #             'inputindex': 0,
        #             'outputitem': node,
        #             'outputindex': 0,
        #             'branch': False,
        #             'nodetypename': None
        #             }

        #     network_editor.pushEventContext('nodegraphactivewire', data)
        #     node.setInput(0, data['inputitem'], data['inputindex'])

        network_editor.setCurrentNode(node)
    except hou.OperationInterrupted:
        pass


def openEditor():
    for entry in QtWidgets.qApp.allWidgets():
        if type(entry).__name__ == 'MarkingMenuEditor':
            entry.setParent(None)
            entry.close()
    ex = mm.MarkingMenuEditor()

# SOP FUNCTIONS #########################################################################


def mergeSelection():
    x = hou.selectedNodes()

    network_editor = hou.ui.paneTabOfType(hou.paneTabType.NetworkEditor)
    parm_view = hou.ui.paneTabOfType(hou.paneTabType.Parm)

    try:
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


def objMergeSelection():
    network_editor = hou.ui.paneTabOfType(hou.paneTabType.NetworkEditor)
    parm_view = hou.ui.paneTabOfType(hou.paneTabType.Parm)

    try:
        pos = network_editor.selectPosition()
        pos = network_editor.selectPosition()

        if(len(hou.selectedNodes()) > 0):
            x = hou.selectedNodes()[0]

            a = network_editor.pwd().createNode("object_merge", "ref_"+x.name())

            a.parm('objpath1').set(x.path())
        else:
            a = network_editor.pwd().createNode("object_merge")
        a.setPosition(pos)
        network_editor.setCurrentNode(a)
        a.setSelected(True, clear_all_selected=1)
    except hou.OperationInterrupted:
        pass

# SOP TOOLSCRIPTS #######################################################################
=======
def createNode(node_name, activeWire):
    network_editor = hou.ui.paneTabOfType(hou.paneTabType.NetworkEditor)
    parm_view = hou.ui.paneTabOfType(hou.paneTabType.Parm)

    position = network_editor.selectPosition()
    position = network_editor.selectPosition()

    node = network_editor.pwd().createNode(node_name)
    node.move(position)
    node.setSelected(True, clear_all_selected=True)
    '''
    if 1:
        data = {
                'connection':False,
                'inputitem':None,
                'inputindex':0,
                'outputitem':node,
                'outputindex':0,
                'branch':False,
                'nodetypename':None
                }

        network_editor.pushEventContext('nodegraphactivewire', data)
        node.setInput(0, data['inputitem'], data['inputindex'])'''
    parm_view.setCurrentNode(node)
>>>>>>> a7a97274a979e752d3a9f885369fd7c2f0922b70


def createPointWrangle():
    network_editor = hou.ui.paneTabOfType(hou.paneTabType.NetworkEditor)
    parm_view = hou.ui.paneTabOfType(hou.paneTabType.Parm)

<<<<<<< HEAD
    try:
        position = network_editor.selectPosition()
        position = network_editor.selectPosition()

        node = network_editor.pwd().createNode('attribwrangle')
        node.move(position)
        node.setSelected(True, clear_all_selected=True)
        node.parm('class').set(2)
        node.setName('pointwrangle1', True)
        parm_view.setCurrentNode(node)
    except hou.OperationInterrupted:
        pass
=======
    position = network_editor.selectPosition()
    position = network_editor.selectPosition()

    node = network_editor.pwd().createNode('attribwrangle')
    node.move(position)
    node.setSelected(True, clear_all_selected=True)
    node.parm('class').set(2)
    node.setName('pointwrangle1', True)
    parm_view.setCurrentNode(node)
>>>>>>> a7a97274a979e752d3a9f885369fd7c2f0922b70


def createPrimitiveWrangle():
    network_editor = hou.ui.paneTabOfType(hou.paneTabType.NetworkEditor)
    parm_view = hou.ui.paneTabOfType(hou.paneTabType.Parm)

<<<<<<< HEAD
    try:
        position = network_editor.selectPosition()
        position = network_editor.selectPosition()

        node = network_editor.pwd().createNode('attribwrangle')
        node.move(position)
        node.setSelected(True, clear_all_selected=True)
        node.parm('class').set(1)
        node.setName('primitivewrangle1', True)
        parm_view.setCurrentNode(node)
    except hou.OperationInterrupted:
        pass
=======
    position = network_editor.selectPosition()
    position = network_editor.selectPosition()

    node = network_editor.pwd().createNode('attribwrangle')
    node.move(position)
    node.setSelected(True, clear_all_selected=True)
    node.parm('class').set(1)
    node.setName('primitivewrangle1', True)
    parm_view.setCurrentNode(node)
>>>>>>> a7a97274a979e752d3a9f885369fd7c2f0922b70


def createDetailWrangle():
    network_editor = hou.ui.paneTabOfType(hou.paneTabType.NetworkEditor)
    parm_view = hou.ui.paneTabOfType(hou.paneTabType.Parm)

<<<<<<< HEAD
    try:
        position = network_editor.selectPosition()
        position = network_editor.selectPosition()

        node = network_editor.pwd().createNode('attribwrangle')
        node.move(position)
        node.setSelected(True, clear_all_selected=True)
        node.parm('class').set(0)
        node.setName('detailwrangle1', True)
        parm_view.setCurrentNode(node)
    except hou.OperationInterrupted:
        pass
=======
    position = network_editor.selectPosition()
    position = network_editor.selectPosition()

    node = network_editor.pwd().createNode('attribwrangle')
    node.move(position)
    node.setSelected(True, clear_all_selected=True)
    node.parm('class').set(0)
    node.setName('detailwrangle1', True)
    parm_view.setCurrentNode(node)
>>>>>>> a7a97274a979e752d3a9f885369fd7c2f0922b70


def createVertexWrangle():
    network_editor = hou.ui.paneTabOfType(hou.paneTabType.NetworkEditor)
    parm_view = hou.ui.paneTabOfType(hou.paneTabType.Parm)

<<<<<<< HEAD
    try:
        position = network_editor.selectPosition()
        position = network_editor.selectPosition()

        node = network_editor.pwd().createNode('attribwrangle')
        node.move(position)
        node.setSelected(True, clear_all_selected=True)
        node.parm('class').set(3)
        node.setName('vertexwrangle1', True)
        parm_view.setCurrentNode(node)
    except hou.OperationInterrupted:
        pass
=======
    position = network_editor.selectPosition()
    position = network_editor.selectPosition()

    node = network_editor.pwd().createNode('attribwrangle')
    node.move(position)
    node.setSelected(True, clear_all_selected=True)
    node.parm('class').set(3)
    node.setName('vertexwrangle1', True)
    parm_view.setCurrentNode(node)
>>>>>>> a7a97274a979e752d3a9f885369fd7c2f0922b70


def createVolumeWrangle():
    network_editor = hou.ui.paneTabOfType(hou.paneTabType.NetworkEditor)
    parm_view = hou.ui.paneTabOfType(hou.paneTabType.Parm)

<<<<<<< HEAD
    try:
        position = network_editor.selectPosition()
        position = network_editor.selectPosition()

        node = network_editor.pwd().createNode('volumewrangle')
        node.move(position)
        node.setSelected(True, clear_all_selected=True)
        parm_view.setCurrentNode(node)
    except hou.OperationInterrupted:
        pass
=======
    position = network_editor.selectPosition()
    position = network_editor.selectPosition()

    node = network_editor.pwd().createNode('volumewrangle')
    node.move(position)
    node.setSelected(True, clear_all_selected=True)
    parm_view.setCurrentNode(node)
>>>>>>> a7a97274a979e752d3a9f885369fd7c2f0922b70


def createPointVOP():
    network_editor = hou.ui.paneTabOfType(hou.paneTabType.NetworkEditor)
    parm_view = hou.ui.paneTabOfType(hou.paneTabType.Parm)

<<<<<<< HEAD
    try:
        position = network_editor.selectPosition()
        position = network_editor.selectPosition()

        node = network_editor.pwd().createNode('attribvop')
        node.move(position)
        node.setSelected(True, clear_all_selected=True)
        node.parm('bindclass').set(2)
        node.setName('pointvop1', True)
        parm_view.setCurrentNode(node)
    except hou.OperationInterrupted:
        pass
=======
    position = network_editor.selectPosition()
    position = network_editor.selectPosition()

    node = network_editor.pwd().createNode('attribvop')
    node.move(position)
    node.setSelected(True, clear_all_selected=True)
    node.parm('bindclass').set(2)
    node.setName('pointvop1', True)
    parm_view.setCurrentNode(node)
>>>>>>> a7a97274a979e752d3a9f885369fd7c2f0922b70


def createPrimitiveVOP():
    network_editor = hou.ui.paneTabOfType(hou.paneTabType.NetworkEditor)
    parm_view = hou.ui.paneTabOfType(hou.paneTabType.Parm)

<<<<<<< HEAD
    try:
        position = network_editor.selectPosition()
        position = network_editor.selectPosition()

        node = network_editor.pwd().createNode('attribvop')
        node.move(position)
        node.setSelected(True, clear_all_selected=True)
        node.parm('bindclass').set(1)
        node.setName('primitivevop1', True)
        parm_view.setCurrentNode(node)
    except hou.OperationInterrupted:
        pass
=======
    position = network_editor.selectPosition()
    position = network_editor.selectPosition()

    node = network_editor.pwd().createNode('attribvop')
    node.move(position)
    node.setSelected(True, clear_all_selected=True)
    node.parm('bindclass').set(1)
    node.setName('primitivevop1', True)
    parm_view.setCurrentNode(node)
>>>>>>> a7a97274a979e752d3a9f885369fd7c2f0922b70


def createDetailVOP():
    network_editor = hou.ui.paneTabOfType(hou.paneTabType.NetworkEditor)
    parm_view = hou.ui.paneTabOfType(hou.paneTabType.Parm)

<<<<<<< HEAD
    try:
        position = network_editor.selectPosition()
        position = network_editor.selectPosition()

        node = network_editor.pwd().createNode('attribvop')
        node.move(position)
        node.setSelected(True, clear_all_selected=True)
        node.parm('bindclass').set(0)
        node.setName('detailvop1', True)
        parm_view.setCurrentNode(node)
    except hou.OperationInterrupted:
        pass
=======
    position = network_editor.selectPosition()
    position = network_editor.selectPosition()

    node = network_editor.pwd().createNode('attribvop')
    node.move(position)
    node.setSelected(True, clear_all_selected=True)
    node.parm('bindclass').set(0)
    node.setName('detailvop1', True)
    parm_view.setCurrentNode(node)
>>>>>>> a7a97274a979e752d3a9f885369fd7c2f0922b70


def createVertexVOP():
    network_editor = hou.ui.paneTabOfType(hou.paneTabType.NetworkEditor)
    parm_view = hou.ui.paneTabOfType(hou.paneTabType.Parm)

<<<<<<< HEAD
    try:
        position = network_editor.selectPosition()
        position = network_editor.selectPosition()

        node = network_editor.pwd().createNode('attribvop')
        node.move(position)
        node.setSelected(True, clear_all_selected=True)
        node.parm('bindclass').set(3)
        node.setName('vertexvop1', True)
        parm_view.setCurrentNode(node)
    except hou.OperationInterrupted:
        pass
=======
    position = network_editor.selectPosition()
    position = network_editor.selectPosition()

    node = network_editor.pwd().createNode('attribvop')
    node.move(position)
    node.setSelected(True, clear_all_selected=True)
    node.parm('bindclass').set(3)
    node.setName('vertexvop1', True)
    parm_view.setCurrentNode(node)
>>>>>>> a7a97274a979e752d3a9f885369fd7c2f0922b70


def createVolumeVOP():
    network_editor = hou.ui.paneTabOfType(hou.paneTabType.NetworkEditor)
    parm_view = hou.ui.paneTabOfType(hou.paneTabType.Parm)

<<<<<<< HEAD
    try:
        position = network_editor.selectPosition()
        position = network_editor.selectPosition()

        node = network_editor.pwd().createNode('volumevop')
        node.move(position)
        node.setSelected(True, clear_all_selected=True)
        parm_view.setCurrentNode(node)
    except hou.OperationInterrupted:
        pass


def forLoopFeedback():
    network_editor = hou.ui.paneTabOfType(hou.paneTabType.NetworkEditor)
    parm_view = hou.ui.paneTabOfType(hou.paneTabType.Parm)

    try:
        position = network_editor.selectPosition()
        position = network_editor.selectPosition()

        blockbegin = network_editor.pwd().createNode(
            'block_begin', node_name='feedback_begin1')
        blockbegin.move(position)

        blockend = network_editor.pwd().createNode(
            'block_end', node_name='feedback_end1')
        blockend.move(position + hou.Vector2(0, -2))

        meta = network_editor.pwd().createNode(
            'block_begin', node_name='meta1')
        meta.move(position + hou.Vector2(-2, 0))
        meta.parm('blockpath').set('../' + blockend.name())

        blockbegin.parm('blockpath').set('../' + blockend.name())
        blockend.parm('blockpath').set('../' + blockbegin.name())
        blockend.setInput(0, blockbegin)

        blockend.parm('itermethod').set(2)

        color = hou.Color(.475, .812, .204)
        blockbegin.setColor(color)
        blockend.setColor(color)

        blockbegin.setSelected(True, clear_all_selected=True)
        blockend.setSelected(True)

        parm_view.setCurrentNode(blockend)

    except hou.OperationInterrupted:
        pass


def forLoopNamedPiece():
    network_editor = hou.ui.paneTabOfType(hou.paneTabType.NetworkEditor)
    parm_view = hou.ui.paneTabOfType(hou.paneTabType.Parm)

    try:
        position = network_editor.selectPosition()
        position = network_editor.selectPosition()

        blockbegin = network_editor.pwd().createNode(
            'block_begin', node_name='namedPiece_begin1')
        blockbegin.move(position)

        blockend = network_editor.pwd().createNode(
            'block_end', node_name='namedPiece_end1')
        blockend.move(position + hou.Vector2(0, -2))

        meta = network_editor.pwd().createNode(
            'block_begin', node_name='meta1')
        meta.move(position + hou.Vector2(-2, 0))
        meta.parm('blockpath').set('../' + blockend.name())

        blockbegin.parm('blockpath').set('../' + blockend.name())
        blockend.parm('blockpath').set('../' + blockbegin.name())
        blockend.setInput(0, blockbegin)

        blockbegin.parm('method').set(1)
        blockend.parm('itermethod').set(1)
        blockend.parm('method').set(1)
        blockend.parm('class').set(0)
        blockend.parm('useattrib').set(1)
        blockend.parm('attrib').set('name')
        blockend.parm('templatepath').set('../' + blockbegin.name())

        color = hou.Color(.094, .369, .69)
        blockbegin.setColor(color)
        blockend.setColor(color)

        blockbegin.setSelected(True, clear_all_selected=True)
        blockend.setSelected(True)

        parm_view.setCurrentNode(blockend)

    except hou.OperationInterrupted:
        pass


def forLoopConnected():
    network_editor = hou.ui.paneTabOfType(hou.paneTabType.NetworkEditor)
    parm_view = hou.ui.paneTabOfType(hou.paneTabType.Parm)

    try:
        position = network_editor.selectPosition()
        position = network_editor.selectPosition()

        blockbegin = network_editor.pwd().createNode(
            'block_begin', node_name='connected_begin1')
        blockbegin.move(position)

        blockend = network_editor.pwd().createNode(
            'block_end', node_name='connected_end1')
        blockend.move(position + hou.Vector2(0, -2))

        meta = network_editor.pwd().createNode(
            'block_begin', node_name='meta1')
        meta.move(position + hou.Vector2(-2, 0))
        meta.parm('blockpath').set('../' + blockend.name())

        blockbegin.parm('blockpath').set('../' + blockend.name())
        blockend.parm('blockpath').set('../' + blockbegin.name())
        blockend.setInput(0, blockbegin)

        blockbegin.parm('method').set(1)
        blockend.parm('itermethod').set(1)
        blockend.parm('method').set(1)
        blockend.parm('class').set(0)
        blockend.parm('useattrib').set(1)
        blockend.parm('attrib').set('class')
        blockend.parm('templatepath').set('../' + blockbegin.name())

        color = hou.Color(.565, .494, .863)
        blockbegin.setColor(color)
        blockend.setColor(color)

        blockbegin.setSelected(True, clear_all_selected=True)
        blockend.setSelected(True)

        parm_view.setCurrentNode(blockend)

    except hou.OperationInterrupted:
        pass


def forLoopPoints():
    network_editor = hou.ui.paneTabOfType(hou.paneTabType.NetworkEditor)
    parm_view = hou.ui.paneTabOfType(hou.paneTabType.Parm)

    try:
        position = network_editor.selectPosition()
        position = network_editor.selectPosition()

        blockbegin = network_editor.pwd().createNode(
            'block_begin', node_name='points_begin1')
        blockbegin.move(position)

        blockend = network_editor.pwd().createNode(
            'block_end', node_name='points_end1')
        blockend.move(position + hou.Vector2(0, -2))

        meta = network_editor.pwd().createNode(
            'block_begin', node_name='meta1')
        meta.move(position + hou.Vector2(-2, 0))
        meta.parm('blockpath').set('../' + blockend.name())

        blockbegin.parm('blockpath').set('../' + blockend.name())
        blockend.parm('blockpath').set('../' + blockbegin.name())
        blockend.setInput(0, blockbegin)

        blockbegin.parm('method').set(1)
        blockend.parm('itermethod').set(1)
        blockend.parm('method').set(1)
        blockend.parm('class').set(1)
        blockend.parm('templatepath').set('../' + blockbegin.name())

        # color = hou.Color(.094, .369, .69)
        # blockbegin.setColor(color)
        # blockend.setColor(color)

        blockbegin.setSelected(True, clear_all_selected=True)
        blockend.setSelected(True)

        parm_view.setCurrentNode(blockend)

    except hou.OperationInterrupted:
        pass


def forLoopPrims():
    network_editor = hou.ui.paneTabOfType(hou.paneTabType.NetworkEditor)
    parm_view = hou.ui.paneTabOfType(hou.paneTabType.Parm)

    try:
        position = network_editor.selectPosition()
        position = network_editor.selectPosition()

        blockbegin = network_editor.pwd().createNode(
            'block_begin', node_name='prims_begin1')
        blockbegin.move(position)

        blockend = network_editor.pwd().createNode(
            'block_end', node_name='prims_end1')
        blockend.move(position + hou.Vector2(0, -2))

        meta = network_editor.pwd().createNode(
            'block_begin', node_name='meta1')
        meta.move(position + hou.Vector2(-2, 0))
        meta.parm('blockpath').set('../' + blockend.name())

        blockbegin.parm('blockpath').set('../' + blockend.name())
        blockend.parm('blockpath').set('../' + blockbegin.name())
        blockend.setInput(0, blockbegin)

        blockbegin.parm('method').set(1)
        blockend.parm('itermethod').set(1)
        blockend.parm('method').set(1)
        blockend.parm('class').set(0)
        blockend.parm('templatepath').set('../' + blockbegin.name())

        # color = hou.Color(.094, .369, .69)
        # blockbegin.setColor(color)
        # blockend.setColor(color)

        blockbegin.setSelected(True, clear_all_selected=True)
        blockend.setSelected(True)

        parm_view.setCurrentNode(blockend)

    except hou.OperationInterrupted:
        pass


def compiledBlock():
    network_editor = hou.ui.paneTabOfType(hou.paneTabType.NetworkEditor)
    parm_view = hou.ui.paneTabOfType(hou.paneTabType.Parm)

    try:
        position = network_editor.selectPosition()
        position = network_editor.selectPosition()

        blockbegin = network_editor.pwd().createNode(
            'compile_begin', node_name='compile_begin1')
        blockbegin.move(position)

        blockend = network_editor.pwd().createNode(
            'compile_end', node_name='compile_end1')
        blockend.move(position + hou.Vector2(0, -2))

        blockbegin.parm('blockpath').set('../' + blockend.name())
        blockend.setInput(0, blockbegin)

        color = hou.Color(1, 1, 1)
        blockbegin.setColor(color)
        blockend.setColor(color)

        blockbegin.setSelected(True, clear_all_selected=True)
        blockend.setSelected(True)

        parm_view.setCurrentNode(blockend)

    except hou.OperationInterrupted:
        pass

# VOP TOOLSCRIPTS #######################################################################
=======
    position = network_editor.selectPosition()
    position = network_editor.selectPosition()

    node = network_editor.pwd().createNode('volumevop')
    node.move(position)
    node.setSelected(True, clear_all_selected=True)
    parm_view.setCurrentNode(node)
>>>>>>> a7a97274a979e752d3a9f885369fd7c2f0922b70


def createBindExport():
    network_editor = hou.ui.paneTabOfType(hou.paneTabType.NetworkEditor)
    parm_view = hou.ui.paneTabOfType(hou.paneTabType.Parm)

<<<<<<< HEAD
    try:
        position = network_editor.selectPosition()
        position = network_editor.selectPosition()

        node = network_editor.pwd().createNode('bind')
        node.move(position)
        node.setSelected(True, clear_all_selected=True)
        node.parm('overridetype').set(True)
        node.parm('useasparmdefiner').set(True)
        node.parm('exportparm').set(2)
        parm_view.setCurrentNode(node)
    except hou.OperationInterrupted:
        pass


def VOPwhileLoop():
    network_editor = hou.ui.paneTabOfType(hou.paneTabType.NetworkEditor)
    parm_view = hou.ui.paneTabOfType(hou.paneTabType.Parm)

    try:
        position = network_editor.selectPosition()
        position = network_editor.selectPosition()

        blockbegin = network_editor.pwd().createNode(
            'block_begin_if', node_name='while_begin1')
        blockend = network_editor.pwd().createNode(
            'block_end_while', node_name='end_while1')

        blockbegin.move(position)
        blockend.move(position + hou.Vector2(2, 0))

        blockbegin.parm('blockpath').set('../' + blockend.name())
        blockend.parm('blockpath').set('../' + blockbegin.name())

        blockbegin.setSelected(True, clear_all_selected=True)
        blockend.setSelected(True)

        color = hou.Color(.75, .4, 0)
        blockbegin.setColor(color)
        blockend.setColor(color)

        parm_view.setCurrentNode(blockend)

    except hou.OperationInterrupted:
        pass


def VOPforLoop():
    network_editor = hou.ui.paneTabOfType(hou.paneTabType.NetworkEditor)
    parm_view = hou.ui.paneTabOfType(hou.paneTabType.Parm)

    try:
        position = network_editor.selectPosition()
        position = network_editor.selectPosition()

        blockbegin = network_editor.pwd().createNode(
            'block_begin_for', node_name='for_begin1')
        blockend = network_editor.pwd().createNode(
            'block_end', node_name='end_for1')

        blockbegin.move(position)
        blockend.move(position + hou.Vector2(2, 0))

        blockbegin.parm('blockpath').set('../' + blockend.name())
        blockend.parm('blockpath').set('../' + blockbegin.name())

        blockbegin.setSelected(True, clear_all_selected=True)
        blockend.setSelected(True)

        color = hou.Color(.75, .4, 0)
        blockbegin.setColor(color)
        blockend.setColor(color)

        parm_view.setCurrentNode(blockend)

    except hou.OperationInterrupted:
        pass


def VOPdoWhileLoop():
    network_editor = hou.ui.paneTabOfType(hou.paneTabType.NetworkEditor)
    parm_view = hou.ui.paneTabOfType(hou.paneTabType.Parm)

    try:
        position = network_editor.selectPosition()
        position = network_editor.selectPosition()

        blockbegin = network_editor.pwd().createNode(
            'block_begin', node_name='do_while_begin1')
        blockend = network_editor.pwd().createNode(
            'block_end_while', node_name='end_do_while1')

        blockbegin.move(position)
        blockend.move(position + hou.Vector2(2, 0))

        blockbegin.parm('blockpath').set('../' + blockend.name())
        blockend.parm('blockpath').set('../' + blockbegin.name())

        blockbegin.setSelected(True, clear_all_selected=True)
        blockend.setSelected(True)

        color = hou.Color(.75, .4, 0)
        blockbegin.setColor(color)
        blockend.setColor(color)

        parm_view.setCurrentNode(blockend)

    except hou.OperationInterrupted:
        pass


def VOPifBlock():
    network_editor = hou.ui.paneTabOfType(hou.paneTabType.NetworkEditor)
    parm_view = hou.ui.paneTabOfType(hou.paneTabType.Parm)

    try:
        position = network_editor.selectPosition()
        position = network_editor.selectPosition()

        blockbegin = network_editor.pwd().createNode(
            'block_begin_if', node_name='if_begin1')
        blockend = network_editor.pwd().createNode(
            'block_end', node_name='end_if1')

        blockbegin.move(position)
        blockend.move(position + hou.Vector2(2, 0))

        blockbegin.parm('blockpath').set('../' + blockend.name())
        blockend.parm('blockpath').set('../' + blockbegin.name())

        blockbegin.setSelected(True, clear_all_selected=True)
        blockend.setSelected(True)

        color = hou.Color(0, .466667, 1)
        blockbegin.setColor(color)
        blockend.setColor(color)

        parm_view.setCurrentNode(blockend)

    except hou.OperationInterrupted:
        pass
=======
    position = network_editor.selectPosition()
    position = network_editor.selectPosition()

    node = network_editor.pwd().createNode('bind')
    node.move(position)
    node.setSelected(True, clear_all_selected=True)
    node.parm('overridetype').set(True)
    node.parm('useasparmdefiner').set(True)
    node.parm('exportparm').set(2)
    parm_view.setCurrentNode(node)


def openEditor():
    for entry in QtWidgets.qApp.allWidgets():
        if type(entry).__name__ == 'MarkingMenuEditor':
            entry.setParent(None)
            entry.close()
    ex = mm.MarkingMenuEditor()


def mergeSelection():
    x = hou.selectedNodes()

    if(len(x) > 0):
        network_editor = hou.ui.paneTabOfType(hou.paneTabType.NetworkEditor)
        parm_view = hou.ui.paneTabOfType(hou.paneTabType.Parm)

        position = network_editor.selectPosition()
        position = network_editor.selectPosition()

        a = network_editor.pwd().createNode("merge")

        a.setPosition(position)

        for node in x:
            a.setNextInput(node)

        network_editor.setCurrentNode(a)

        a.setSelected(True, clear_all_selected=1)


def objMergeSelection():
    network_editor = hou.ui.paneTabOfType(hou.paneTabType.NetworkEditor)
    parm_view = hou.ui.paneTabOfType(hou.paneTabType.Parm)

    pos = network_editor.selectPosition()
    pos = network_editor.selectPosition()

    if(len(hou.selectedNodes()) > 0):
        x = hou.selectedNodes()[0]

        a = network_editor.pwd().createNode("object_merge", "ref_"+x.name())

        a.parm('objpath1').set(x.path())
    else:
        a = network_editor.pwd().createNode("object_merge")
    a.setPosition(pos)
    network_editor.setCurrentNode(a)
    a.setSelected(True, clear_all_selected=1)
>>>>>>> a7a97274a979e752d3a9f885369fd7c2f0922b70

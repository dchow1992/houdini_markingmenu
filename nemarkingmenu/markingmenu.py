import hou
 
''' Set menu_activate = 1 to turn on menu '''
menu_activate = 0
 
 
def assetImporter(**kwargs):
    """Open MAS browser."""
    from houdini_asset_importer import dialog
    dialog.show_dialog()
 
 
# SOP SCRIPTS
def absRefCopy(**kwargs):
    """Make a copy of a node and absolute reference its parameters."""
    if kwargs is not None:
        network_editor = kwargs['editor']
        sel = hou.selectedNodes()
        try:
            if len(sel) == 0:
                hou.ui.displayMessage('no node selected')
            else:
                root = hou.node(sel[0].parent().path())
                final_sel = []
                for c in sel:
                    x = (c,)
                    copy = hou.copyNodesTo(x, root)[0]
 
                    # nudge copy
                    nudge = hou.Vector2(.5, -.5)
                    copy.move(nudge)
                    # make abs references
                    ref_parms = c.parmTuples()
                    c_parms = copy.parmTuples()
                    # for each parm tuple
                    for p in range(len(ref_parms)):
                        ptype = ref_parms[p].parmTemplate().type()
                        # for each index of the tuple
                        if ptype == hou.parmTemplateType.String:
                            for i in range(len(ref_parms[p])):
                                c_parms[p][i].setExpression('chs("{}")'.format(
                                    ref_parms[p][i].path()))
                        else:
                            for i in range(len(ref_parms[p])):
                                c_parms[p][i].setExpression('ch("{}")'.format(
                                    ref_parms[p][i].path()))
 
                    # add to final_sel
                    final_sel.append(copy)
                    # add comment
                    copy.setComment('Referenced from ' + c.path())
                    copy.setGenericFlag(hou.nodeFlag.DisplayComment, True)
                    # set color
                    copy.setColor(hou.Color((.45, .15, .45)))
                # select final_sel
                for node in final_sel:
                    node.setSelected(True, clear_all_selected=1)
                    network_editor.setCurrentNode(node)
 
        except hou.OperationInterrupted:
            pass
 
 
def mergeSelection(**kwargs):
    """Merge selected nodes and pick position."""
    if kwargs is not None:
        x = hou.selectedNodes()
        network_editor = kwargs['editor']
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
 
 
def objMergeSelection(**kwargs):
    """Object merge selected node and pick position."""
    if kwargs is not None:
        network_editor = kwargs['editor']
        try:
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
 
 
def stickyLabel(**kwargs):
    """Make a borderless stickynote with bold font."""
    if kwargs is not None:
        network_editor = kwargs['editor']
        n = network_editor.pwd()
        try:
            pos = network_editor.selectPosition()
            pos = network_editor.selectPosition()
 
            a = n.createStickyNote()
            a.setSize(hou.Vector2(4.0,2.0))
            a.setPosition(pos - hou.Vector2(1,1))
            a.setText("label1")
            a.setTextSize(0.35)
            a.setTextColor(hou.Color(.65,.65,.85))
            a.setDrawBackground(0)
 
        except hou.OperationInterrupted:
            pass
 
 
def toggleBlastSplit(**kwargs):
    """Convert a blast to a split, or vice versa."""
    if kwargs is not None:
        network_editor = kwargs['editor']
        current_node = network_editor.currentNode()
        if current_node:
            if current_node.type().category() == hou.sopNodeTypeCategory():
                if current_node.type() == hou.nodeType(hou.sopNodeTypeCategory(),"blast"):
                    negate = current_node.parm("negate").eval()
                    current_node = current_node.changeNodeType('split',keep_name=False,keep_network_contents=False,keep_parms=True)
                    current_node.parm('negate').set(1-negate)
                elif current_node.type() == hou.nodeType(hou.sopNodeTypeCategory(),"split"):
                    negate = current_node.parm("negate").eval()
                    current_node = current_node.changeNodeType('blast',keep_name=False,keep_network_contents=False,keep_parms=True)
                    current_node.parm('negate').set(1-negate)
 
 
# SOP TOOLSCRIPTS
 
 
def createPointWrangle(**kwargs):
    """Create an attribute wrangle in point mode, place it, and pick input wire."""
    if kwargs is not None:
        network_editor = kwargs['editor']
        try:
            position = network_editor.selectPosition()
            position = network_editor.selectPosition()
 
            node = network_editor.pwd().createNode('attribwrangle')
            node.move(position)
            node.setSelected(True, clear_all_selected=True)
            node.parm('class').set(2)
            node.setName('pointwrangle1', True)
 
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
 
 
def createPrimitiveWrangle(**kwargs):
    """Create an attribute wrangle in primitive mode, place it, and pick input wire."""
    if kwargs is not None:
        network_editor = kwargs['editor']
        try:
            position = network_editor.selectPosition()
            position = network_editor.selectPosition()
 
            node = network_editor.pwd().createNode('attribwrangle')
            node.move(position)
            node.setSelected(True, clear_all_selected=True)
            node.parm('class').set(1)
            node.setName('primitivewrangle1', True)
 
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
 
 
def createDetailWrangle(**kwargs):
    """Create an attribute wrangle in detail mode, place it, and pick input wire."""
    if kwargs is not None:
        network_editor = kwargs['editor']
        try:
            position = network_editor.selectPosition()
            position = network_editor.selectPosition()
 
            node = network_editor.pwd().createNode('attribwrangle')
            node.move(position)
            node.setSelected(True, clear_all_selected=True)
            node.parm('class').set(0)
            node.setName('detailwrangle1', True)
 
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
 
 
def createVertexWrangle(**kwargs):
    """Create an attribute wrangle in vertex mode, place it, and pick input wire."""
    if kwargs is not None:
        network_editor = kwargs['editor']
        try:
            position = network_editor.selectPosition()
            position = network_editor.selectPosition()
 
            node = network_editor.pwd().createNode('attribwrangle')
            node.move(position)
            node.setSelected(True, clear_all_selected=True)
            node.parm('class').set(3)
            node.setName('vertexwrangle1', True)
 
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
 
 
def createVolumeWrangle(**kwargs):
    """Create a volume wrangle, place it, and pick input wire."""
    if kwargs is not None:
        network_editor = kwargs['editor']
        try:
            position = network_editor.selectPosition()
            position = network_editor.selectPosition()
 
            node = network_editor.pwd().createNode('volumewrangle')
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
 
 
def createPointVOP(**kwargs):
    """Create an attribute vop in point mode, place it, and pick input wire."""
    if kwargs is not None:
        network_editor = kwargs['editor']
 
        try:
            position = network_editor.selectPosition()
            position = network_editor.selectPosition()
 
            node = network_editor.pwd().createNode('attribvop')
            node.move(position)
            node.setSelected(True, clear_all_selected=True)
            node.parm('bindclass').set(2)
            node.setName('pointvop1', True)
 
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
 
 
def createPrimitiveVOP(**kwargs):
    """Create an attribute vop in primitive mode, place it, and pick input wire."""
    if kwargs is not None:
        network_editor = kwargs['editor']
 
        try:
            position = network_editor.selectPosition()
            position = network_editor.selectPosition()
 
            node = network_editor.pwd().createNode('attribvop')
            node.move(position)
            node.setSelected(True, clear_all_selected=True)
            node.parm('bindclass').set(1)
            node.setName('primitivevop1', True)
 
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
 
 
def createDetailVOP(**kwargs):
    """Create an attribute vop in detail mode, place it, and pick input wire."""
    if kwargs is not None:
        network_editor = kwargs['editor']
 
        try:
            position = network_editor.selectPosition()
            position = network_editor.selectPosition()
 
            node = network_editor.pwd().createNode('attribvop')
            node.move(position)
            node.setSelected(True, clear_all_selected=True)
            node.parm('bindclass').set(0)
            node.setName('detailvop1', True)
 
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
 
 
def createVertexVOP(**kwargs):
    """Create an attribute vop in vertex mode, place it, and pick input wire."""
    if kwargs is not None:
        network_editor = kwargs['editor']
 
        try:
            position = network_editor.selectPosition()
            position = network_editor.selectPosition()
 
            node = network_editor.pwd().createNode('attribvop')
            node.move(position)
            node.setSelected(True, clear_all_selected=True)
            node.parm('bindclass').set(3)
            node.setName('vertexvop1', True)
 
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
 
 
def createVolumeVOP(**kwargs):
    """Create a volume vop, place it, and pick input wire."""
    if kwargs is not None:
        network_editor = kwargs['editor']
 
        try:
            position = network_editor.selectPosition()
            position = network_editor.selectPosition()
 
            node = network_editor.pwd().createNode('volumevop')
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
 
 
def forLoopFeedback(**kwargs):
    """Create a for loop feedback block in sops."""
    if kwargs is not None:
        network_editor = kwargs['editor']
 
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
 
            network_editor.setCurrentNode(blockend)
 
        except hou.OperationInterrupted:
            pass
 
 
def forLoopNamedPiece(**kwargs):
    """Create a for each named piece block in sops."""
    if kwargs is not None:
        network_editor = kwargs['editor']
 
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
 
            network_editor.setCurrentNode(blockend)
 
        except hou.OperationInterrupted:
            pass
 
 
def forLoopConnected(**kwargs):
    """Create a for each connected piece block in sops."""
    if kwargs is not None:
        network_editor = kwargs['editor']
 
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
 
            network_editor.setCurrentNode(blockend)
 
        except hou.OperationInterrupted:
            pass
 
 
def forLoopPoints(**kwargs):
    """Create a for each point block in sops."""
    if kwargs is not None:
        network_editor = kwargs['editor']
 
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
 
            blockbegin.setSelected(True, clear_all_selected=True)
            blockend.setSelected(True)
 
            network_editor.setCurrentNode(blockend)
 
        except hou.OperationInterrupted:
            pass
 
 
def forLoopPrims(**kwargs):
    """Create a for each primitive block in sops."""
    if kwargs is not None:
        network_editor = kwargs['editor']
 
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
 
            blockbegin.setSelected(True, clear_all_selected=True)
            blockend.setSelected(True)
 
            network_editor.setCurrentNode(blockend)
 
        except hou.OperationInterrupted:
            pass
 
 
def compiledBlock(**kwargs):
    """Create a compile block in sops."""
    if kwargs is not None:
        network_editor = kwargs['editor']
 
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
 
            network_editor.setCurrentNode(blockend)
 
        except hou.OperationInterrupted:
            pass
 
 
# VOP TOOLSCRIPTS
 
 
def createBindExport(**kwargs):
    """Create a bind export and place it."""
    if kwargs is not None:
        network_editor = kwargs['editor']
 
        try:
            position = network_editor.selectPosition()
            position = network_editor.selectPosition()
 
            node = network_editor.pwd().createNode('bind')
            node.move(position)
            node.setSelected(True, clear_all_selected=True)
            node.parm('overridetype').set(True)
            node.parm('useasparmdefiner').set(True)
            node.parm('exportparm').set(2)
            network_editor.setCurrentNode(node)
 
        except hou.OperationInterrupted:
            pass
 
 
def VOP_whileLoop(**kwargs):
    """Create a while loop in vops."""
    if kwargs is not None:
        network_editor = kwargs['editor']
 
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
 
            network_editor.setCurrentNode(blockend)
 
        except hou.OperationInterrupted:
            pass
 
 
def VOP_forLoop(**kwargs):
    """Create a for loop in vops."""
    if kwargs is not None:
        network_editor = kwargs['editor']
 
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
 
            network_editor.setCurrentNode(blockend)
 
        except hou.OperationInterrupted:
            pass
 
 
def VOP_doWhileLoop(**kwargs):
    """Create a do while loop in vops."""
    if kwargs is not None:
        network_editor = kwargs['editor']
 
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
 
            network_editor.setCurrentNode(blockend)
 
        except hou.OperationInterrupted:
            pass
 
 
def VOP_ifBlock(**kwargs):
    """Create a if block in vops."""
    if kwargs is not None:
        network_editor = kwargs['editor']
 
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
 
            network_editor.setCurrentNode(blockend)
 
        except hou.OperationInterrupted:
            pass
 
# ROP TOOLSCRIPTS
 
 
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

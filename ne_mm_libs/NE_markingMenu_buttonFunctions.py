import hou

def createNode(node_name, activeWire):
	network_editor = hou.ui.paneTabOfType(hou.paneTabType.NetworkEditor)
	parm_view = hou.ui.paneTabOfType(hou.paneTabType.Parm)

	position = network_editor.selectPosition()
	position = network_editor.selectPosition() 

	node = network_editor.pwd().createNode(node_name)
	node.move(position)
	node.setSelected(True, clear_all_selected=True)
	
	parm_view.setCurrentNode(node)
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

def createPointWrangle():
	network_editor = hou.ui.paneTabOfType(hou.paneTabType.NetworkEditor)
	parm_view = hou.ui.paneTabOfType(hou.paneTabType.Parm)

	position = network_editor.selectPosition()
	position = network_editor.selectPosition() 

	node = network_editor.pwd().createNode('attribwrangle')
	node.move(position)
	node.setSelected(True, clear_all_selected=True)
	node.parm('class').set(2)	
	parm_view.setCurrentNode(node)

def createPrimitiveWrangle():
	network_editor = hou.ui.paneTabOfType(hou.paneTabType.NetworkEditor)
	parm_view = hou.ui.paneTabOfType(hou.paneTabType.Parm)

	position = network_editor.selectPosition()
	position = network_editor.selectPosition() 

	node = network_editor.pwd().createNode('attribwrangle')
	node.move(position)
	node.setSelected(True, clear_all_selected=True)
	node.parm('class').set(1)	
	parm_view.setCurrentNode(node)

def createDetailWrangle():
	network_editor = hou.ui.paneTabOfType(hou.paneTabType.NetworkEditor)
	parm_view = hou.ui.paneTabOfType(hou.paneTabType.Parm)

	position = network_editor.selectPosition()
	position = network_editor.selectPosition() 

	node = network_editor.pwd().createNode('attribwrangle')
	node.move(position)
	node.setSelected(True, clear_all_selected=True)
	node.parm('class').set(0)	
	parm_view.setCurrentNode(node)

def createVertexWrangle():
	network_editor = hou.ui.paneTabOfType(hou.paneTabType.NetworkEditor)
	parm_view = hou.ui.paneTabOfType(hou.paneTabType.Parm)

	position = network_editor.selectPosition()
	position = network_editor.selectPosition() 

	node = network_editor.pwd().createNode('attribwrangle')
	node.move(position)
	node.setSelected(True, clear_all_selected=True)
	node.parm('class').set(3)	
	parm_view.setCurrentNode(node)

def createVolumeWrangle():
	network_editor = hou.ui.paneTabOfType(hou.paneTabType.NetworkEditor)
	parm_view = hou.ui.paneTabOfType(hou.paneTabType.Parm)

	position = network_editor.selectPosition()
	position = network_editor.selectPosition() 

	node = network_editor.pwd().createNode('volumewrangle')
	node.move(position)
	node.setSelected(True, clear_all_selected=True)	
	parm_view.setCurrentNode(node)

def createPointVOP():
	network_editor = hou.ui.paneTabOfType(hou.paneTabType.NetworkEditor)
	parm_view = hou.ui.paneTabOfType(hou.paneTabType.Parm)

	position = network_editor.selectPosition()
	position = network_editor.selectPosition() 

	node = network_editor.pwd().createNode('attribvop')
	node.move(position)
	node.setSelected(True, clear_all_selected=True)	
	node.parm('bindclass').set(2)	
	parm_view.setCurrentNode(node)

def createPrimitiveVOP():
	network_editor = hou.ui.paneTabOfType(hou.paneTabType.NetworkEditor)
	parm_view = hou.ui.paneTabOfType(hou.paneTabType.Parm)

	position = network_editor.selectPosition()
	position = network_editor.selectPosition() 

	node = network_editor.pwd().createNode('attribvop')
	node.move(position)
	node.setSelected(True, clear_all_selected=True)	
	node.parm('bindclass').set(1)	
	parm_view.setCurrentNode(node)

def createDetailVOP():
	network_editor = hou.ui.paneTabOfType(hou.paneTabType.NetworkEditor)
	parm_view = hou.ui.paneTabOfType(hou.paneTabType.Parm)

	position = network_editor.selectPosition()
	position = network_editor.selectPosition() 

	node = network_editor.pwd().createNode('attribvop')
	node.move(position)
	node.setSelected(True, clear_all_selected=True)	
	node.parm('bindclass').set(0)	
	parm_view.setCurrentNode(node)

def createVertexVOP():
	network_editor = hou.ui.paneTabOfType(hou.paneTabType.NetworkEditor)
	parm_view = hou.ui.paneTabOfType(hou.paneTabType.Parm)

	position = network_editor.selectPosition()
	position = network_editor.selectPosition() 

	node = network_editor.pwd().createNode('attribvop')
	node.move(position)
	node.setSelected(True, clear_all_selected=True)	
	node.parm('bindclass').set(3)	
	parm_view.setCurrentNode(node)

def createVolumeVOP():
	network_editor = hou.ui.paneTabOfType(hou.paneTabType.NetworkEditor)
	parm_view = hou.ui.paneTabOfType(hou.paneTabType.Parm)

	position = network_editor.selectPosition()
	position = network_editor.selectPosition() 

	node = network_editor.pwd().createNode('volumevop')
	node.move(position)
	node.setSelected(True, clear_all_selected=True)			
	parm_view.setCurrentNode(node)
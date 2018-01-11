import hou
from ne_mm_libs import NE_markingMenuEditor as mm           
from PySide2 import QtWidgets
reload(mm)

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

def createPointWrangle():
	network_editor = hou.ui.paneTabOfType(hou.paneTabType.NetworkEditor)
	parm_view = hou.ui.paneTabOfType(hou.paneTabType.Parm)

	position = network_editor.selectPosition()
	position = network_editor.selectPosition() 

	node = network_editor.pwd().createNode('attribwrangle')
	node.move(position)
	node.setSelected(True, clear_all_selected=True)
	node.parm('class').set(2)	
	node.setName('pointwrangle1', True)
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
	node.setName('primitivewrangle1', True)
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
	node.setName('detailwrangle1', True)
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
	node.setName('vertexwrangle1', True)
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
	node.setName('pointvop1', True)	
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
	node.setName('primitivevop1', True)
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
	node.setName('detailvop1', True)
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
	node.setName('vertexvop1', True)
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



def createBindExport():
	network_editor = hou.ui.paneTabOfType(hou.paneTabType.NetworkEditor)
	parm_view = hou.ui.paneTabOfType(hou.paneTabType.Parm)

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
	    if type(entry).__name__ == 'NE_MarkingMenuEditor':
	        entry.setParent(None)
	        entry.close()	        
	ex = mm.NE_MarkingMenuEditor()

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
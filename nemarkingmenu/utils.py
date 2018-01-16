import json
import os
import hou
from math import sqrt
from PySide2 import QtWidgets, QtGui, QtCore, QtTest


class ButtonConfig:
    def __init__(
            self,
            context,
            index,
            isMenu,
            label,
            icon,
            collection,
            commandType,
            command,
            nodetype,
            activeWire):

        self.active = 1
        self.nodetype = nodetype
        self.label = label
        self.icon = icon
        self.index = index
        self.activeWire = activeWire

        self.defaultcommand = 'cmds.createNode("{}", {})'.format(
            self.nodetype, self.activeWire)

        self.config = {
            'context': context,
            'active': self.active,
            'isMenu': isMenu,
            'label': self.label,
            'icon': self.icon,
            'index': self.index,
            'menuCollection': collection,
            'nodetype': self.nodetype,
            'commandType': commandType,
            'activeWire': self.activeWire,
            'command': self.defaultcommand if commandType == 'createnode' else command
        }


def filterCollections(path, context):
    # return a list of collections on disk matching context
    filteredObj = []
    for obj in os.listdir(path):
        if os.path.splitext(obj)[-1] == '.json':
            if obj.split('_', 1)[0] == context:
                filteredObj.append(obj)
    baseC = context + '_baseCollection.json'
    filteredObj.insert(0, filteredObj.pop(filteredObj.index(baseC)))
    return filteredObj


def loadMenuPreferences(path):
<<<<<<< HEAD
    with open(path, 'r') as f:
=======
    with open(os.path.join(path, 'menuprefs.json'), 'r') as f:
>>>>>>> a7a97274a979e752d3a9f885369fd7c2f0922b70
        return json.load(f)


def loadCollection(collection):
    # creates list from collection fullpath
    with open(collection, 'r') as f:
        return json.load(f)['menu']


def saveCollection(collection, data):
    # saves data to collection fullpath
    a = {'menu': data}
    with open(collection, 'w') as f:
        json.dump(a, f, indent=4, sort_keys=True)


<<<<<<< HEAD
def getContext(editor=hou.ui.paneTabOfType(hou.paneTabType.NetworkEditor)):
    hou_context = editor.pwd().childTypeCategory().name()
=======
def getContext():
    hou_context = hou.ui.paneTabOfType(
        hou.paneTabType.NetworkEditor).pwd().childTypeCategory().name()
>>>>>>> a7a97274a979e752d3a9f885369fd7c2f0922b70
    if hou_context == 'Sop':
        return 'SOP'
    elif hou_context == 'Object':
        return 'OBJ'
    elif hou_context == 'Driver':
        return 'ROP'
    elif hou_context == 'ChopNet':
        return 'CHOP'
    elif hou_context == 'Vop':
        return 'VOP'
    elif hou_context == 'Shop':
        return 'SHOP'
    elif hou_context == 'CopNet':
        return 'COP'


def buildCompleter(jsonfile):
    strlist = []

    jsondict = {}
    with open(jsonfile, 'r') as f:
        jsondict = json.load(f)

    for x in jsondict.keys():
        for item in jsondict[x]:
            strlist.append(item)

    comp = QtWidgets.QCompleter(strlist)
    comp.popup().setStyleSheet(hou.qt.styleSheet())
    comp.setCompletionMode(QtWidgets.QCompleter.InlineCompletion)
    return comp


def pointRectDist(pos, rect):
        # pos = QtCore.QPoint, rect= QtCore.QRect
        # return the distance from pos to rect
        x = pos.x()
        y = pos.y()
        rx = rect.topLeft().x()
        ry = rect.topLeft().y()
        width = rect.width()
        height = rect.height()
        cx = max(min(x, rx+width), rx)
        cy = max(min(y, ry+height), ry)
        return sqrt((x - cx)*(x - cx) + (y - cy)*(y - cy))


def qpDist(pt0, pt1):
    # QtCore.QPoints
    a = hou.Vector2(pt0.x(), pt0.y())
    b = hou.Vector2(pt1.x(), pt1.y())
    return a.distanceTo(b)

# a = {
#     "activeWire": False,
#     "command": "",
#     "commandType": "None",
#     "context": "SOP",
#     "icon": "SOP_object_merge",
#     "index": 6,
#     "isMenu": True,
#     "label": "Utilities",
#     "menuCollection": "SOP_soputils.collection",
#     "nodetype": "null"
#     }

# b = {
#     "activeWire": False,
#     "command": "cmds.createNode(\"null\", False)",
#     "commandType": "createnode",
#     "context": "SOP",
#     "icon": "COMMON_null",
#     "index": 7,
#     "isMenu": False,
#     "label": "Null",
#     "menuCollection": "",
#     "nodetype": "null"
#     }

# c = [a,b]

# d = {}
# d['menu'] = c

# x = json.dumps(d, indent=4, sort_keys=True)
# print x

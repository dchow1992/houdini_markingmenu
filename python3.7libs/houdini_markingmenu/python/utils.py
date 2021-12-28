import json

import os

import hou

from math import sqrt

from PySide2 import QtWidgets


class ButtonConfig:
    """Create a button object.

    Keyword arguments:
    context -- the houdini context
    index -- the button's position in the marking menu
    isMenu -- determines if the button opens a menu or performs an action
    label -- the button's displayed name
    icon -- the button's displayed icon
    collection -- the json file a menu button points to
    commandType -- a button can either create a node or run a custom function
    command -- custom function name or createnode string
    nodetype -- houdini nodetype string
    activeWire -- boolean should input wire be picked on creation
    """

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
            'command': command
        }


def filterCollections(path, context):
    """Return a list of collection strings that match context."""
    filteredObj = []
    for obj in os.listdir(path):
        if os.path.splitext(obj)[-1] == '.json':
            if obj.split('_', 1)[0] == context:
                filteredObj.append(obj)
    baseC = context + '_baseCollection.json'
    filteredObj = sorted(filteredObj, key=str.lower)
    filteredObj.insert(0, filteredObj.pop(filteredObj.index(baseC)))
    return filteredObj


def loadMenuPreferences(path):
    """Return dictionary of menu preference json file."""
    with open(path, 'r') as f:
        return json.load(f)


def loadCollection(collection):
    """Return dictionary list from json file collection."""
    if os.path.isfile(collection):
        with open(collection, 'r') as f:
            return json.load(f)['menu']
    else:
        return []


def saveCollection(collection, data):
    """Save dictionary list data to json file collection."""
    a = {'menu': data}
    with open(collection, 'w') as f:
        json.dump(a, f, indent=4, sort_keys=True)


def getContext(editor):
    """Return houdini context string."""
    hou_context = editor.pwd().childTypeCategory().name()
    if hou_context == 'Sop':
        return 'SOP'
    elif hou_context == 'Dop':
        return 'DOP'
    elif hou_context == 'Object':
        return 'OBJ'
    elif hou_context == 'Driver':
        return 'ROP'
    elif hou_context == 'Chop':
        return 'CHOP'
    elif hou_context == 'Vop':
        return 'VOP'
    elif hou_context == 'Shop':
        return 'SHOP'
    elif hou_context == 'Cop2':
        return 'COP'


def buildCompleter(jsonfile):
    """Create QCompleter from jsonfile."""
    strlist = []
    jsondict = {}
    with open(jsonfile, 'r') as f:
        jsondict = json.load(f)

    for x in jsondict.keys():
        for item in jsondict[x]:
            strlist.append(item)

    comp = QtWidgets.QCompleter(strlist)
    comp.popup().setStyleSheet(hou.qt.styleSheet())
    comp.setCompletionMode(QtWidgets.QCompleter.PopupCompletion)
    return comp


def pointRectDist(pos, rect):
    """Calculate the distance from a point to a rectangle.

    Keyword arguments:
    pos -- position (type QtCore.QPoint)
    rect -- rectangle (type QtCore.QRect)
    """
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
    """Calculate the distance between 2 vectors.

    pt0, pt1 -- type QtCore.QPoint
    """
    a = hou.Vector2(pt0.x(), pt0.y())
    b = hou.Vector2(pt1.x(), pt1.y())
    return a.distanceTo(b)

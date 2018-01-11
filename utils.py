import json
import os

class ButtonConfig:
    def __init__(self, context, index, isMenu, label, icon, collection, commandType, command, nodetype, activeWire):                
        self.nodetype = nodetype
        self.label = label
        self.icon = icon
        self.index = index
        self.activeWire = activeWire
        self.defaultcommand = 'cmds.createNode("%s", %s)' % (self.nodetype, self.activeWire)
        self.config = {
            'context':context,
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
    with open(path+'menuprefs.json', 'r') as f:
        return json.load(f)

def loadCollection(collection):
    # creates dictionary from collection fullpath
    with open(collection, 'r') as f:
        return json.load(f)['menu']

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
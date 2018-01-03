import json

class buttonConfig:
    def __init__(self, buttonType, nodetype, label, icon, index, activeWire):
        self.itemType = buttonType
        self.nodetype = nodetype
        self.label = label
        self.icon = icon
        self.index = index
        self.activeWire = activeWire
        self.config = {
            'itemType': self.itemType,
            'isMenu': True if buttonType == 'menu' else False,
            'label': self.label,
            'icon': self.icon,
            'index': self.index,        
            'menuObjects': {},
            'menuCollection': '',
            'nodetype': self.nodetype,
            'commandType': 'createnode',
            'activeWire': self.activeWire,
            'command': 'cmds.createNode("%s", %s)' % (self.nodetype, self.activeWire)
        }

outputFile = {}
for i in range(8):
    outputFile['menuItem%d'%i] = None

outputFile['menuItem0'] = buttonConfig('button', 'vdbfrompolygons', 'VDB from Polygons', 'SOP_OpenVDB', 0, False).config
outputFile['menuItem1'] = buttonConfig('button', 'bound', 'Bound', 'SOP_bound', 1, False).config
outputFile['menuItem2'] = buttonConfig('button', 'box', 'Box', 'SOP_box', 2, False).config
outputFile['menuItem3'] = buttonConfig('button', 'null', 'Null', 'SOP_null', 3, False).config
outputFile['menuItem4'] = buttonConfig('button', 'attribrename', 'Attribute Rename', 'SOP_attribute', 4, False).config
outputFile['menuItem5'] = buttonConfig('menu', 'attribdelete', 'Attribute Delete', 'SOP_attribdelete', 5, False).config
outputFile['menuItem6'] = buttonConfig('button', 'attribwrangle', 'Vertex Wrangle', 'SOP_attribwrangle', 6, False).config
outputFile['menuItem7'] = buttonConfig('button', 'normal', 'Normal', 'SOP_normal', 7, False).config

inputFile = {}

filename = 'SOP_baseCollection.collection'
dirpath = hou.getenv('HOUDINI_USER_PREF_DIR')+'/python2.7libs/ne_mm_libs/collections/'

with open(dirpath+filename, 'w') as f:
    json.dump(outputFile, f)
'''
with open(dirpath+filename, 'r') as f:
    inputFile = json.load(f)'''

#import pprint
#pprint.pprint(inputFile)

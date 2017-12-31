import json

class buttonConfig:
    def __init__(self, buttonType, nodetype, label, icon):
        self.itemType = buttonType
        self.nodetype = nodetype
        self.label = label
        self.icon = icon
        self.config = {
            'itemType': self.itemType,
            'isMenu': True if buttonType == 'menu' else False,
            'label': self.label,
            'icon': self.icon,
            'command': 'cmds.createNode("%s", False)' % self.nodetype
        }

menuItem0 = None
menuItem1 = None
menuItem2 = None
menuItem3 = None
menuItem4 = None
menuItem5 = None
menuItem6 = None
menuItem7 = None

menuItem0 = buttonConfig('button', 'null', 'Null', 'SOP_null')
menuItem1 = buttonConfig('button', 'attribwrangle', 'Attribute Wrangle', 'SOP_attribwrangle')
menuItem2 = buttonConfig('button', 'null', 'Null', 'SOP_null')
menuItem3 = buttonConfig('button', 'null', 'Null', 'SOP_null')
menuItem4 = buttonConfig('button', 'null', 'Null', 'SOP_null')
menuItem5 = buttonConfig('button', 'null', 'Null', 'SOP_null')
menuItem6 = buttonConfig('button', 'null', 'Null', 'SOP_null')
menuItem7 = buttonConfig('button', 'null', 'Null', 'SOP_null')

inputFile = {}

outputFile = {
    'menuItem0': menuItem0.config if menuItem0 != None else None,
    'menuItem1': menuItem1.config if menuItem1 != None else None,
    'menuItem2': menuItem2.config if menuItem2 != None else None,
    'menuItem3': menuItem3.config if menuItem3 != None else None,
    'menuItem4': menuItem4.config if menuItem4 != None else None,
    'menuItem5': menuItem5.config if menuItem5 != None else None,
    'menuItem6': menuItem6.config if menuItem6 != None else None,
    'menuItem7': menuItem7.config if menuItem7 != None else None
}

filename = 'NE_markingMenu_SOP.json'
dirpath = hou.getenv('HOUDINI_USER_PREF_DIR')+'/python2.7libs/'

with open(dirpath+filename, 'w') as f:
    json.dump(outputFile, f)

with open(dirpath+filename, 'r') as f:
    inputFile = json.load(f)

import pprint
pprint.pprint(inputFile)

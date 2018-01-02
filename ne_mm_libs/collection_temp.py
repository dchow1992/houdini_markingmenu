import json

class buttonConfig:
    def __init__(self, buttonType, nodetype, label, icon, index):
        self.itemType = buttonType
        self.nodetype = nodetype
        self.label = label
        self.icon = icon
        self.index = index
        self.config = {
            'itemType': self.itemType,
            'isMenu': True if buttonType == 'menu' else False,
            'label': self.label,
            'icon': self.icon,
            'index': self.index,        
            'menuObjects': {},
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

menuItem0 = buttonConfig('button', 'null', 'Null', 'SOP_null', 0)
menuItem1 = buttonConfig('button', 'attribwrangle', 'Attribute Wrangle', 'SOP_attribwrangle', 1)
menuItem2 = buttonConfig('menu', 'null', 'Null', 'SOP_null', 2)
menuItem3 = buttonConfig('button', 'null', 'Null', 'SOP_null', 3)
menuItem4 = buttonConfig('button', 'null', 'Null', 'SOP_null', 4)
menuItem5 = buttonConfig('button', 'null', 'Null', 'SOP_null', 5)
menuItem6 = buttonConfig('button', 'null', 'Null', 'SOP_null', 6)
menuItem7 = buttonConfig('button', 'null', 'Null', 'SOP_null', 7)

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

filename = 'SOP_wrangles.collection'
dirpath = hou.getenv('HOUDINI_USER_PREF_DIR')+'/python2.7libs/ne_mm_libs/collections/'

with open(dirpath+filename, 'w') as f:
    json.dump(outputFile, f)

with open(dirpath+filename, 'r') as f:
    inputFile = json.load(f)

#import pprint
#pprint.pprint(inputFile)

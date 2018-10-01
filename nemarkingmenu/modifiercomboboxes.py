from Qt_py.Qt import QtWidgets
 
from subwidgets import labelcombobox
 
reload(labelcombobox)
 
 
class ModifierComboBoxes(QtWidgets.QWidget):
    def __init__(self):
        super(ModifierComboBoxes, self).__init__()
        self.initUI()
 
    def initUI(self):
        self.layout = QtWidgets.QVBoxLayout()
 
        self.shift = labelcombobox.LabelComboBox(
            'SHIFT: Base Collection       ',
            350)
 
        self.ctrl = labelcombobox.LabelComboBox(
            'CONTROL: Base Collection',
            349)
        self.layout.addLayout(self.shift.layout)
        self.layout.addLayout(self.ctrl.layout)

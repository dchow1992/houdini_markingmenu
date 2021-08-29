from PySide2 import QtWidgets

from subwidgets import labelcombobox


class ModifierComboBoxes(QtWidgets.QWidget):
    def __init__(self, *args, **kwargs):
        super(ModifierComboBoxes, self).__init__()
        self.whitespace = 29
        self.dpifactor = 1.2 if kwargs['highdpi'] else 1
        self.initUI()

    def initUI(self):
        self.layout = QtWidgets.QVBoxLayout()

        self.shift = labelcombobox.LabelComboBox(
            'SHIFT: Base Collection'.ljust(self.whitespace),
            350*self.dpifactor)

        self.ctrl = labelcombobox.LabelComboBox(
            'CONTROL: Base Collection',
            349*self.dpifactor)

        self.layout.addLayout(self.shift.layout)
        self.layout.addLayout(self.ctrl.layout)

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QWidget, QLabel, QVBoxLayout, QSizePolicy, QHBoxLayout, QFrame
from .option_box import OptionBox

class SelectionBox(QFrame):
    def __init__(self):
        super().__init__()
        self.setSizePolicy(
            QSizePolicy.Policy.Expanding,
            QSizePolicy.Policy.Preferred
        )
        self.setObjectName('SelectionBox')

        title: QLabel = QLabel()
        title.setText('Tipo de Conciliação')
        title.setObjectName('selection_box_title')

        self.option_box: OptionBox = OptionBox()

        layout: QVBoxLayout = QVBoxLayout()
        layout.setContentsMargins(20, 30, 20, 30)
        layout.setSpacing(0)
        layout.addWidget(title)
        layout.addWidget(self.option_box)

        layout.setSizeConstraint(QVBoxLayout.SetMinimumSize)

        self.setLayout(layout)
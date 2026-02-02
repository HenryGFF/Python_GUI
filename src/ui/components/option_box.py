from cProfile import label

from PySide6.QtGui import QPixmap
from PySide6.QtWidgets import QPushButton, QWidget, QHBoxLayout, QVBoxLayout, QLabel, QButtonGroup, QSizePolicy
from PySide6.QtCore import QSize, Signal
from dataclasses import dataclass
from enum import Enum, auto


class TargetForm(Enum):
    FormA = auto()
    FormB = auto()


@dataclass
class ButtonConfig:
    label: str
    sublabel: str
    form_type: TargetForm
    icon: str


class OptionBox(QWidget):
    def __init__(self):
        super().__init__()
        self.setFixedHeight(100)
        self.setSizePolicy(
            QSizePolicy.Policy.Expanding,
            QSizePolicy.Policy.Fixed
        )

        layout: QHBoxLayout = QHBoxLayout(self)

        self.optionA: Button = Button(
            layout,
            ButtonConfig(
                label = 'Um dia',
                sublabel = 'Conciliação para uma data específica',
                form_type = TargetForm.FormA,
                icon = 'assets/images/calendario_icon.png'
            )
        )
        self.optionB: Button = Button(
            layout,
            ButtonConfig(
                label='Período',
                sublabel='Conciliação para um intervalo de datas',
                form_type = TargetForm.FormB,
                icon='assets/images/calendario2_icon.png'

            )
        )

        group: QButtonGroup = QButtonGroup(self)
        group.setExclusive(True)
        group.addButton(self.optionA)
        group.addButton(self.optionB)

class Button(QPushButton):
    add_form_requested = Signal(TargetForm, TargetForm, dict)

    def __init__(self, parent_layout, config: ButtonConfig):
        super().__init__('Adicionar Form')
        self._form_cache = {}
        self.config = config
        self.setText('')

        self.label = QLabel(config.label)
        self.label.setObjectName('button_label')

        self.sublabel = QLabel(config.sublabel)
        self.sublabel.setObjectName('button_sublabel')

        icon = QWidget()
        icon.setFixedWidth(60)
        icon.setFixedHeight(60)

        icon_layout = QHBoxLayout(icon)
        icon_label = QLabel()
        img = QPixmap(config.icon)
        icon_label.setPixmap(img)
        icon_label.setScaledContents(True)
        icon_layout.addWidget(icon_label)

        container = QWidget(self)
        container.setSizePolicy(
            QSizePolicy.Policy.Expanding,
            QSizePolicy.Policy.Fixed
        )

        layout = QVBoxLayout(container)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(5)
        layout.addWidget(self.label)
        layout.addWidget(self.sublabel)

        button_layout = QHBoxLayout(self)
        button_layout.setContentsMargins(10, 10, 10, 10)
        button_layout.addWidget(icon)
        button_layout.addWidget(container)

        self.setSizePolicy(
            QSizePolicy.Policy.Expanding,
            QSizePolicy.Policy.Fixed
        )

        self.setObjectName('OptionButton')
        self.setCheckable(True)
        self.clicked.connect(self.on_click)

        parent_layout.addWidget(self)

    def on_click(self):
        self.add_form_requested.emit(TargetForm, self.config, self._form_cache)

    def sizeHint(self) -> QSize:
        return self.layout().sizeHint()

    def minimumSizeHint(self) -> QSize:
        return self.layout().minimumSize()
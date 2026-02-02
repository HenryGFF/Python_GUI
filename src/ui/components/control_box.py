from PySide6.QtCore import QSize, Signal, Qt
from PySide6.QtWidgets import QWidget, QSizePolicy, QPushButton, QLabel, QHBoxLayout, QVBoxLayout

class ControlBox(QWidget):
    reset_content_widget = Signal()
    send_content_data = Signal()

    def __init__(self):
        super().__init__()

        self.setSizePolicy(
            QSizePolicy.Policy.Expanding,
            QSizePolicy.Policy.Expanding
        )

        layout: QVBoxLayout = QVBoxLayout(self)
        layout.setContentsMargins(0, 10, 0, 0)
        layout.setSpacing(0)

        container: QWidget = QWidget()
        container_layout: QHBoxLayout = QHBoxLayout(container)
        container_layout.setContentsMargins(0, 0, 0, 0)
        container_layout.setSpacing(10)

        self.reset_btn: Button = Button('Limpar')
        self.reset_btn.setObjectName('reset_btn')
        self.reset_btn.clicked.connect(self.reset_btn_click)
        container_layout.addWidget(self.reset_btn, alignment=Qt.AlignHCenter)

        self.send_btn: Button = Button('> Executar Conciliação')
        self.send_btn.setObjectName('send_btn')
        self.send_btn.clicked.connect(self.send_btn_click)
        container_layout.addWidget(self.send_btn, alignment=Qt.AlignHCenter)
        self.send_btn.setEnabled(False)

        layout.addWidget(container, alignment=Qt.AlignHCenter)

    def reset_btn_click(self):
        self.reset_content_widget.emit()

    def send_btn_click(self):
        self.send_content_data.emit()



class Button(QPushButton):
    def __init__(self, label):
        super().__init__()
        self.label = QLabel(label)
        self.label.setObjectName('control_btn_label')

        container = QWidget(self)
        container.setSizePolicy(
            QSizePolicy.Policy.Expanding,
            QSizePolicy.Policy.Fixed
        )

        layout = QHBoxLayout(container)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(5)
        layout.addWidget(self.label)

        button_layout = QHBoxLayout(self)
        button_layout.setContentsMargins(15, 15, 15, 15)
        button_layout.addWidget(container)

        self.setSizePolicy(
            QSizePolicy.Policy.Expanding,
            QSizePolicy.Policy.Fixed
        )

        self.setObjectName('control_btn')


    def sizeHint(self) -> QSize:
        return self.layout().sizeHint()

    def minimumSizeHint(self) -> QSize:
        return self.layout().minimumSize()
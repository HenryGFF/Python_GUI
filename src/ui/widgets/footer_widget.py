from PySide6.QtCore import Qt
from PySide6.QtWidgets import QLabel, QVBoxLayout, QFrame, QSizePolicy


class FooterWidget(QFrame):
    def __init__(self):
        super().__init__()

        self.setObjectName('FooterWidget')

        footer_text: QLabel = QLabel()
        footer_text.setText('© 2026 Banco Daycoval S.A. — Sistema de Conciliação')
        footer_text.setObjectName('footer_text')
        footer_text.setAlignment(Qt.AlignCenter)

        layout: QVBoxLayout = QVBoxLayout()
        layout.setContentsMargins(30, 30, 30, 30)
        layout.setSpacing(0)
        layout.addWidget(footer_text, alignment=Qt.AlignTop)

        self.setSizePolicy(
            QSizePolicy.Policy.Expanding,
            QSizePolicy.Policy.Expanding
        )

        self.setLayout(layout)
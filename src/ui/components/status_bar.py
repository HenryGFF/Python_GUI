from PySide6.QtWidgets import QFrame, QLabel, QHBoxLayout, QSizePolicy
from PySide6.QtCore import Qt

class StatusMessage(QFrame):
    def __init__(self):
        super().__init__()

        self.setObjectName("StatusMessage")
        self.setVisible(False)

        self.label = QLabel("")
        self.label.setObjectName('status_text')
        self.label.setAlignment(Qt.AlignCenter)

        layout = QHBoxLayout(self)
        layout.setContentsMargins(10, 6, 10, 6)
        layout.addWidget(self.label)

        self.setSizePolicy(
            QSizePolicy.Policy.Expanding,
            QSizePolicy.Policy.Fixed
        )

    def show_message(self, text, status):
        self.label.setText(text)
        self.label.setProperty("status", status)

        self.label.style().unpolish(self.label)
        self.label.style().polish(self.label)

        self.setVisible(True)

    def clear(self):
        self.setVisible(False)
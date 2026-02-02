from PySide6.QtWidgets import QWidget, QVBoxLayout
from ui.components.header_bar import HeaderBar
from .content_widget import ContentSection
from .footer_widget import FooterWidget


class CentralWidget(QWidget):
    def __init__(self):
        super().__init__()

        layout: QVBoxLayout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(90)

        self.header: HeaderBar = HeaderBar()
        layout.addWidget(self.header)

        self.content: ContentSection = ContentSection()
        layout.addWidget(self.content)

        self.footer: FooterWidget = FooterWidget()
        layout.addWidget(self.footer)

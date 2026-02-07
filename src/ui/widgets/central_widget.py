from PySide6.QtCore import Qt
from PySide6.QtWidgets import QWidget, QVBoxLayout, QScrollArea, QFrame
from ui.components.header_bar import HeaderBar
from .content_widget import ContentSection
from .footer_widget import FooterWidget


class CentralWidget(QWidget):
    def __init__(self):
        super().__init__()

        # Layout raiz
        root_layout = QVBoxLayout(self)
        root_layout.setContentsMargins(0, 0, 0, 0)
        root_layout.setSpacing(0)

        # HEADER FIXA
        self.header = HeaderBar()
        root_layout.addWidget(self.header)

        # SCROLL
        self.scroll = QScrollArea()
        self.scroll.setWidgetResizable(True)
        self.scroll.setFrameShape(QFrame.NoFrame)
        self.scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        root_layout.addWidget(self.scroll)

        # CONTAINER DO SCROLL
        self.scroll_container = QWidget()
        scroll_layout = QVBoxLayout(self.scroll_container)
        scroll_layout.setContentsMargins(0, 30, 0, 0)
        scroll_layout.setSpacing(24)

        # CONTEÚDO
        self.content = ContentSection()
        scroll_layout.addWidget(self.content)

        self.footer: FooterWidget = FooterWidget()
        layout.addWidget(self.footer)

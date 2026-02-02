from PySide6.QtWidgets import QMainWindow, QScrollArea, QFrame
from .widgets import CentralWidget
from PySide6.QtCore import Qt

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle('App Daycoval')

        self.scroll = QScrollArea()
        self.scroll.setWidgetResizable(True)
        self.setCentralWidget(self.scroll)

        self.central = CentralWidget()
        self.scroll.setWidget(self.central)

        self.central.layout().addStretch()

        self.scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.scroll.setFrameShape(QFrame.NoFrame)
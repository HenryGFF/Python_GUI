from PySide6.QtWidgets import QMainWindow, QScrollArea, QFrame
from .widgets import CentralWidget
from PySide6.QtCore import Qt

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle('App Daycoval')

        self.central = CentralWidget()
        self.setCentralWidget(self.central)
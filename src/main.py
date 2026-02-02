import sys
from PySide6.QtCore import QLocale
from PySide6.QtWidgets import QApplication
from PySide6.QtGui import QFontDatabase
from ui import MainWindow

app = QApplication(sys.argv)

QFontDatabase.addApplicationFont(
    "assets/fonts/Quicksand/Quicksand-VariableFont_wght.ttf"
)
with open('ui/style/base.qss') as f:
    app.setStyleSheet(f.read())

QLocale.setDefault(QLocale(QLocale.Portuguese, QLocale.Brazil))

window: MainWindow = MainWindow()
window.showMaximized()

app.exec()
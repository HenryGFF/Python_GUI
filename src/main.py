import sys
from PySide6.QtCore import QLocale
from PySide6.QtWidgets import QApplication
from PySide6.QtGui import QFontDatabase, QPalette, QColor
from ui import MainWindow
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent

qss_path = BASE_DIR / 'ui' / 'style' / 'base.qss'
font_path = BASE_DIR / 'assets' / 'fonts' / 'Quicksand' / 'Quicksand-VariableFont_wght.ttf'

app = QApplication(sys.argv)
app.setStyle("Fusion")
palette = QPalette()
palette.setColor(QPalette.Window, QColor(249, 250, 251))
palette.setColor(QPalette.Base, QColor(249, 250, 251))
palette.setColor(QPalette.AlternateBase, QColor(255, 255, 255))
app.setPalette(palette)

QFontDatabase.addApplicationFont(str(font_path))

with open(qss_path, 'r', encoding='utf-8') as f:
    app.setStyleSheet(f.read())

QLocale.setDefault(QLocale(QLocale.Portuguese, QLocale.Brazil))

window: MainWindow = MainWindow()
window.showMaximized()

app.exec()
from PySide6.QtCore import Qt
from PySide6.QtGui import QPixmap, QIcon
from PySide6.QtWidgets import QVBoxLayout, QLabel, QSizePolicy, QFrame, QHBoxLayout, QWidget


class HeaderBar(QFrame):
    def __init__(self):
        super().__init__()

        self.setFixedHeight(100)
        self.setSizePolicy(
            QSizePolicy.Policy.Expanding,
            QSizePolicy.Policy.Fixed
        )
        self.setObjectName('HeaderBar')

        icon = QFrame()
        icon.setFixedWidth(60)
        icon.setFixedHeight(60)
        icon.setObjectName('header_icon')

        icon_layout = QHBoxLayout(icon)
        label = QLabel()
        img = QPixmap('assets/images/daycoval-logo.png')
        label.setPixmap(img)
        label.setScaledContents(True)
        icon_layout.addWidget(label)

        title:  QLabel = QLabel()
        title.setText('Conciliação Non Deliverable Forward')
        title.setObjectName('title')

        subtitle: QLabel = QLabel()
        subtitle.setText('Sistema de conciliação de bases')
        subtitle.setObjectName('subtitle')

        container = QWidget()
        container_layout: QVBoxLayout = QVBoxLayout(container)
        container_layout.setContentsMargins(20, 20, 20, 20)
        container_layout.setSpacing(0)
        container_layout.addWidget(title)
        container_layout.addWidget(subtitle)

        layout: QHBoxLayout = QHBoxLayout(self)
        layout.setContentsMargins(30, 0, 0, 0)
        layout.setSpacing(0)
        layout.addWidget(icon)
        layout.addWidget(container)
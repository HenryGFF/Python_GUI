from PySide6.QtWidgets import QVBoxLayout, QLabel, QFileDialog, QPushButton, QFrame
from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QDragEnterEvent, QDropEvent
import os

class FinancialBasesUploadWidget(QFrame):
    def __init__(self):
        super().__init__()

        layout = QVBoxLayout(self)
        layout.setSpacing(12)

        self.fields = {
            "Base 360t": FileUploadZone(
                "Base 360T",
                "Arquivo da base 360T",
                [".xlsx", ".xls", ".csv"]
            ),
            "Base ET Filtrada": FileUploadZone(
                "Base ET Filtrada",
                "Arquivo Eletronic Trading",
                [".xlsx", ".xls", ".csv"]
            ),
            "Base ET Completa": FileUploadZone(
                "Base ET Completa",
                "Arquivo Eletronic Trading Completa",
                [".xlsx", ".xls", ".csv"]
            ),
            "Base BBG": FileUploadZone(
                "Base BBG",
                "Arquivo Bloomberg",
                [".xlsx", ".csv"]
            ),
            "Base InfoTreasure": FileUploadZone(
                "Base Info",
                "Arquivo InfoTreasure",
                [".csv"]
            ),
            "Base Planilha": FileUploadZone(
                "Base OP_NDFxSWAP",
                "Base histórico",
                [".xlsx", ".xls"],
                fixed_max_files=1
            )
        }

        self.setObjectName('upload_box')

        for name, widget in self.fields.items():
            layout.addWidget(widget)

    def values(self) -> dict:
        return {
            name: widget.value()
            for name, widget in self.fields.items()
        }

class FileUploadZone(QFrame):
    filesChanged = Signal(list)
    activateSendBtn = Signal()

    def __init__(self, label: str, description: str, accept: list[str], fixed_max_files: int | None = None):
        super().__init__()

        self.setObjectName("upload_area")
        self.setAcceptDrops(True)

        self.accept = accept
        self.files: list[str] = []
        self.fixed_max_files = fixed_max_files
        self.max_files = fixed_max_files or 0

        self.label = QLabel(label)
        self.label.setStyleSheet('color: black;')

        self.description = QLabel(description)
        self.description.setStyleSheet('color: black;')

        self.info = QLabel("Nenhum arquivo selecionado")
        self.info.setStyleSheet('color: black;')

        self.remove_btn = QPushButton("✕")

        self.label.setAlignment(Qt.AlignCenter)
        self.description.setAlignment(Qt.AlignCenter)
        self.info.setAlignment(Qt.AlignCenter)

        self.remove_btn.setVisible(False)
        self.remove_btn.clicked.connect(self.clear_files)

        layout = QVBoxLayout(self)
        layout.setSpacing(6)
        layout.addWidget(self.label)
        layout.addWidget(self.description)
        layout.addWidget(self.info)
        layout.addWidget(self.remove_btn, alignment=Qt.AlignCenter)

        self._update_ui()

    # ---------- Drag & Drop ----------
    def dragEnterEvent(self, event: QDragEnterEvent):
        if event.mimeData().hasUrls():
            event.acceptProposedAction()
            self.setProperty("dragging", True)
            self.style().polish(self)

    def dragLeaveEvent(self, event):
        self.setProperty("dragging", False)
        self.style().polish(self)

    def dropEvent(self, event: QDropEvent):
        self.setProperty("dragging", False)
        self._repolish()

        for url in event.mimeData().urls():
            self._add_file(url.toLocalFile())

    # ---------- Click ----------
    def mousePressEvent(self, event):
        if self.max_files == 0:
            return

        paths, _ = QFileDialog.getOpenFileNames(
            self,
            "Selecionar arquivos",
            "",
            self._qt_filter()
        )

        for path in paths:
            self._add_file(path)

    # ---------- Logic ----------
    def _set_file(self, path: str):
        if not any(path.lower().endswith(ext) for ext in self.accept):
            return

        self.file_path = path
        size_kb = os.path.getsize(path) / 1024

        self.info.setText(
            f"{os.path.basename(path)} — {size_kb:.1f} KB"
        )
        self.remove_btn.setVisible(True)

        self.setProperty("uploaded", True)
        self.style().polish(self)

        self.fileChanged.emit(path)

    def clear_files(self):
        self.files.clear()
        self._update_ui()
        self.filesChanged.emit(self.files)
        self.activateSendBtn.emit()

    def value(self) -> list[str]:
        return self.files

    def _qt_filter(self) -> str:
        exts = " ".join(f"*{e}" for e in self.accept)
        return f"Arquivos ({exts})"

    def _repolish(self):
        self.style().unpolish(self)
        self.style().polish(self)
        self.update()

    # ---------- API pública ----------
    def set_max_files(self, n: int):
        if self.fixed_max_files is None:
            self.max_files = max(0, n)

            if len(self.files) > self.max_files:
                self.files = self.files[:self.max_files]

            self.setEnabled(self.max_files > 0)
            self._update_ui()

    def _enforce_limit(self):
        if len(self.files) > self.max_files:
            self.files = self.files[:self.max_files]
            self._update_ui()

    def _add_file(self, path: str):
        if self.max_files == 0:
            return

        if len(self.files) >= self.max_files:
            return

        if not any(path.lower().endswith(ext) for ext in self.accept):
            return

        if path in self.files:
            return

        self.files.append(path)
        self._update_ui()
        self.filesChanged.emit(self.files)
        if len(self.files) == self.max_files:
            self.activateSendBtn.emit()

    def _update_ui(self):
        if not self.files:
            self.info.setText("Nenhum arquivo selecionado")
            self.remove_btn.setVisible(False)
            self.setProperty("uploaded", False)
        else:
            self.info.setText(
                f"{len(self.files)} / {self.max_files} arquivo(s)"
            )
            self.remove_btn.setVisible(True)
            self.setProperty("uploaded", True)

        self._repolish()
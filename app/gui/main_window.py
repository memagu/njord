from PySide6.QtWidgets import QMainWindow, QWidget, QHBoxLayout, QVBoxLayout

from .compund_widgets import CallForm, GenerateReportBar, CallTable
from app.configuration.global_config import get_version


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle(f"Njord {get_version()}")

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.central_layout = QHBoxLayout(self.central_widget)

        self.call_form = CallForm()
        self.call_form.setMaximumWidth(320)
        self.call_form.setMaximumHeight(512)

        call_display_layout = QVBoxLayout()
        self.top_bar = GenerateReportBar()
        self.call_table = CallTable()

        call_display_layout.addWidget(self.top_bar)
        call_display_layout.addWidget(self.call_table)

        self.central_layout.addWidget(self.call_form)
        self.central_layout.addLayout(call_display_layout)

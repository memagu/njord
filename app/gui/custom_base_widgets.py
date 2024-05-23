from typing import Iterable, Optional


from PySide6.QtWidgets import QSpinBox, QDateTimeEdit, QListWidget, QListWidgetItem, QLineEdit, QMessageBox


from .util import MAX_INT

DATE_TIME_FORMAT = "yyyy-MM-dd hh:mm:ss"
DATE_TIME_MIN_WIDTH = 148


class PositiveSpinbox(QSpinBox):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.setMinimum(1)
        self.setMaximum(MAX_INT)


class BetterDateTimeEdit(QDateTimeEdit):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.setDisplayFormat(DATE_TIME_FORMAT)
        self.setCalendarPopup(True)
        self.setMinimumWidth(DATE_TIME_MIN_WIDTH)

        self.setStyleSheet("""
            QSpinBox {
                width: 64px
            }
        """)


class ExpandableLineEditList(QListWidget):
    def __init__(self, initial_entries: Optional[Iterable[str]] = None):
        super().__init__()

        self.set_entries(initial_entries or tuple())

    def append_entry(self, text: str = "") -> None:
        item = QListWidgetItem()
        self.addItem(item)

        line_edit = QLineEdit(text)
        line_edit.textChanged.connect(self._entry_edited)
        line_edit.item = item

        self.setItemWidget(item, line_edit)

    def remove_entry(self, line_edit: QLineEdit) -> None:
        self.takeItem(next(i for i in range(self.count()) if self.itemWidget(self.item(i)) is line_edit))

    def set_entries(self, entries: Iterable[str]):
        self.clear()
        for entry in entries:
            self.append_entry(entry)
        self.append_entry()

    def _entry_edited(self, new_text: str):
        last_text = self.itemWidget(self.item(self.count() - 1)).text()
        if last_text:
            if last_text.strip():
                self.append_entry()
            return

        if not new_text.strip() and self.count() > 1:
            self.remove_entry(self.sender())

    def get_entries(self) -> tuple[str, ...]:
        return tuple(self.itemWidget(self.item(i)).text() for i in range(self.count() - 1))


class ConfirmationMessageBox(QMessageBox):
    def __init__(self, title: str, prompt: str):
        super().__init__()

        self.setIcon(QMessageBox.Icon.Warning)
        self.setWindowTitle(title)
        self.setText(prompt)
        self.setStandardButtons(QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        self.setDefaultButton(QMessageBox.StandardButton.No)

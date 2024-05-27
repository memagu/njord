import logging
from pathlib import Path
from typing import Optional, Iterable

from PySide6.QtCore import QDateTime, QDate, QTime, Qt, Signal
from PySide6.QtGui import QGuiApplication
from PySide6.QtWidgets import QLineEdit, QWidget, QFormLayout, QLabel, QHBoxLayout, QGroupBox, QFileDialog, \
    QTableWidget, QHeaderView, QTableWidgetItem, QAbstractItemView, QPushButton

from .custom_base_widgets import PositiveSpinbox, ExpandableLineEditList, BetterDateTimeEdit, ConfirmationMessageBox
from .util import Call, NewCall


DATETIME_FILE_NAME_FORMAT = "yyyyMMddHHmmss"


class CallForm(QWidget):
    registerCallSubmitted = Signal(tuple)
    updateCallSubmitted = Signal(tuple)

    def __init__(self):
        super().__init__()

        self._layout = QFormLayout(self)
        self.phone_number = QLineEdit()
        self.start_time = BetterDateTimeEdit(QDateTime.currentDateTime())
        self.id = QLabel("None")
        self.duration = PositiveSpinbox()
        self.duration.setSuffix(" minutes")
        self.cases = ExpandableLineEditList()

        _button_layout = QHBoxLayout()

        self.register_new_call = QPushButton("Register new call")
        self.register_new_call.clicked.connect(self._submit_register_call)
        self.update_call = QPushButton("Update call")
        self.update_call.clicked.connect(self._submit_update_call)

        _button_layout.addWidget(self.register_new_call, 2)
        _button_layout.addWidget(self.update_call, 1)

        self.clear_form = QPushButton("Clear")
        self.clear_form.clicked.connect(self.reset_fields)

        self._layout.addRow("ID:", self.id)
        self._layout.addRow("Phone number:", self.phone_number)
        self._layout.addRow("Start time:", self.start_time)
        self._layout.addRow("Duration:", self.duration)
        self._layout.addRow("Cases:", self.cases)
        self._layout.addRow(_button_layout)
        self._layout.addRow(self.clear_form)

    def _submit_register_call(self) -> None:
        form_data = self.get_form_data()
        self.registerCallSubmitted.emit((None, *form_data[1:]))
        self.reset_fields()

    def _submit_update_call(self) -> None:
        form_data = self.get_form_data()
        self.updateCallSubmitted.emit(form_data)
        self.reset_fields()

    def get_form_data(self) -> Call | NewCall:
        return (
            int(self.id.text()) if self.id.text() != "None" else None,
            self.phone_number.text(),
            self.start_time.dateTime(),
            self.duration.value(),
            self.cases.get_entries()
        )

    def set_form_data(self, call: Call) -> None:
        self.id.setText(str(call[0]))
        self.phone_number.setText(call[1])
        self.start_time.setDateTime(call[2])
        self.duration.setValue(call[3])
        self.cases.set_entries(call[4])

    def reset_fields(self):
        self.id.setText("None")
        self.phone_number.clear()
        self.start_time.setDateTime(QDateTime.currentDateTime())
        self.duration.setValue(1)
        self.cases.set_entries(tuple())


class DateTimeRangeEdit(QWidget):
    dateRangeChanged = Signal(tuple)

    def __init__(self, start: Optional[QDateTime] = None, end: Optional[QDateTime] = None):
        super().__init__()

        if start is not None or end is not None:
            if start is not None and end is not None:
                if start > end:
                    logging.error("Start can't be greater than end.")
                    raise ValueError("Start can't be greater than end.")
            else:
                logging.error("Both start and end must be set if one of them is set.")
                raise ValueError("Both start and end must be set if one of them is set.")

        self._layout = QHBoxLayout(self)

        start = start or QDateTime(QDate.currentDate(), QTime())
        end = end or QDateTime(start.addDays(1).addMSecs(-1))

        self.start = BetterDateTimeEdit(start)
        self.start.dateTimeChanged.connect(self._date_range_changed)
        self.start.dateTimeChanged.connect(self._update_min_end)

        self.end = BetterDateTimeEdit(end)
        self.end.dateTimeChanged.connect(self._date_range_changed)
        self.end.dateTimeChanged.connect(self._update_max_start)

        self._update_min_end(start)
        self._update_max_start(end)

        start_layout = QHBoxLayout()
        start_layout.setAlignment(Qt.AlignmentFlag.AlignLeft)
        start_layout.addWidget(QLabel("Start:"))
        start_layout.addWidget(self.start)

        end_layout = QHBoxLayout()
        end_layout.setAlignment(Qt.AlignmentFlag.AlignLeft)
        end_layout.addWidget(QLabel("End:"))
        end_layout.addWidget(self.end)

        self._layout.addLayout(start_layout)
        self._layout.addLayout(end_layout)

    def _date_range_changed(self):
        start = self.start.dateTime()
        end = self.end.dateTime()
        self.dateRangeChanged.emit((start, end))

    def _update_min_end(self, datetime: QDateTime) -> None:
        self.end.setMinimumDateTime(datetime)

    def _update_max_start(self, datetime: QDateTime) -> None:
        self.start.setMaximumDateTime(datetime)

    def get_date_range(self) -> tuple[QDateTime, QDateTime]:
        return self.start.dateTime(), self.end.dateTime()


class GenerateReportBar(QWidget):
    generateReportPressed = Signal(tuple)

    def __init__(self, default_interval_value: int = 30):
        super().__init__()
        self._layout = QHBoxLayout(self)

        self.date_range_edit = DateTimeRangeEdit()

        generate_report_container = QGroupBox("Generate Report")
        generate_report_container_layout = QHBoxLayout(generate_report_container)

        self.interval_size = PositiveSpinbox()
        self.interval_size.setValue(default_interval_value)
        self.interval_size.setSuffix(" minutes")

        interval_layout = QHBoxLayout()
        interval_layout.setAlignment(Qt.AlignmentFlag.AlignLeft)
        interval_layout.addWidget(QLabel("Interval:"))
        interval_layout.addWidget(self.interval_size)

        self.create_report_button = QPushButton("Generate report")
        self.create_report_button.clicked.connect(self._create_report_button_clicked)

        generate_report_container_layout.addLayout(interval_layout, 1)
        generate_report_container_layout.addWidget(self.create_report_button, 2)

        self._layout.addWidget(self.date_range_edit, 2)
        self._layout.addWidget(generate_report_container, 3)

    def _create_report_button_clicked(self):
        start, end = self.date_range_edit.get_date_range()
        interval_size = self.interval_size.value()
        file_name, _ = QFileDialog.getSaveFileName(
            self,
            "Create report",
            f"{start.toString(DATETIME_FILE_NAME_FORMAT)}-{end.toString(DATETIME_FILE_NAME_FORMAT)}_({interval_size}_minutes).txt",
            filter="Text files (*.txt)"
        )
        self.generateReportPressed.emit((start, end, interval_size, Path(file_name)))


class CallTable(QTableWidget):
    HEADERS = ("id", "Phone Number", "Start Time", "Duration", "Cases", "")

    callSelected = Signal(int)  # ID of call
    deleteCall = Signal(int)  # ID of call

    def __init__(self, initial_calls: Optional[Iterable[Call]] = None) -> None:
        super().__init__()

        initial_calls = initial_calls or tuple()

        self.setColumnCount(len(self.HEADERS))
        self.setRowCount(len(initial_calls))

        self.setSortingEnabled(True)
        self.setAlternatingRowColors(True)

        self.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.setSelectionMode(QAbstractItemView.SelectionMode.SingleSelection)
        self.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        self.itemSelectionChanged.connect(self._row_selected)

        self.setHorizontalHeaderLabels(self.HEADERS)
        self.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeMode.ResizeToContents)
        self.horizontalHeader().setSectionResizeMode(self.columnCount() - 1, QHeaderView.ResizeMode.ResizeToContents)
        # self.hideColumn(0)
        self.horizontalHeader().sectionClicked.connect(self.sort_table)

        self.verticalHeader().setSectionResizeMode(QHeaderView.ResizeMode.ResizeToContents)
        self.verticalHeader().setVisible(False)

        self.set_calls(initial_calls)

    def _row_selected(self) -> None:
        try:
            row = self.selectionModel().selectedRows()[0].row()
            id_ = int(self.item(row, 0).text())
            self.callSelected.emit(id_)
        except IndexError:
            return

    def _delete_row_clicked(self, _, call_id: int) -> None:
        if not QGuiApplication.queryKeyboardModifiers() & Qt.KeyboardModifier.ShiftModifier:
            confirmation_message_box = ConfirmationMessageBox("Delete Call",
                                                              "Are you sure you want to delete the call?")
            if confirmation_message_box.exec() != confirmation_message_box.StandardButton.Yes:
                return
        self.deleteCall.emit(call_id)

    def add_call(self, call: Call) -> None:
        row = self.rowCount()
        self.insertRow(row)

        id_ = call[0]
        phone_number = call[1]
        start_time = call[2]
        duration = f"{call[3]} minutes"
        cases = '\n'.join(call[4])

        for column, data in enumerate((id_, phone_number, start_time, duration, cases)):
            item = QTableWidgetItem()
            item.setData(Qt.ItemDataRole.DisplayRole, data)
            item.setTextAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignHCenter)
            self.setItem(row, column, item)

        delete = QPushButton("Delete")
        delete.clicked.connect(lambda state, call_id=id_: self._delete_row_clicked(state, call_id))
        self.setCellWidget(row, self.columnCount() - 1, delete)

    def clear_calls(self) -> None:
        self.setRowCount(0)

    def set_calls(self, calls: Iterable[Call]) -> None:
        self.clear_calls()
        for call in calls:
            self.add_call(call)

    def sort_table(self, column) -> None:
        self.sortItems(
            column,
            Qt.SortOrder.AscendingOrder
            if self.horizontalHeader().sortIndicatorOrder() == Qt.SortOrder.AscendingOrder else
            Qt.SortOrder.DescendingOrder
        )  # WTF

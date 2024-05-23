import sys
from datetime import datetime, timedelta
from pathlib import Path

from PySide6.QtWidgets import QApplication
from PySide6.QtCore import QDateTime, Qt

from app.core.model.call import Call
from app.gui.util import Call as QtCall
from app.gui.util import NewCall as QtNewCall
from app.core.ports.api.calls_port_api import CallsPortAPI
from app.core.ports.api.report_port_api import ReportPortAPI
from app.gui.main_window import MainWindow


def qt_call_to_call(qt_call: QtCall | QtNewCall) -> Call:
    return Call(
        qt_call[0],
        qt_call[1],
        qt_call[2].toPython(),
        timedelta(minutes=qt_call[3]),
        qt_call[4]
    )


def call_to_qt_call(call: Call) -> QtCall:
    return (
        call.id,
        call.phone_number,
        QDateTime.fromString(call.start_time.isoformat(), Qt.DateFormat.ISODate),
        round(call.duration.total_seconds() / 60),
        call.cases
    )


class QTAdapterAPI:
    def __init__(self, calls_port_api: CallsPortAPI, report_port_api: ReportPortAPI):
        self.calls_port_api = calls_port_api
        self.report_port_api = report_port_api

        self.app = QApplication(sys.argv)

        self.window = MainWindow()
        self.window.resize(1280, 720)
        self.window.call_form.registerCallSubmitted.connect(self._register_call)
        self.window.call_form.updateCallSubmitted.connect(self._update_call)
        self.window.top_bar.date_range_edit.dateRangeChanged.connect(self._date_range_changed)
        self.window.top_bar.generateReportPressed.connect(self._generate_report)
        self.window.call_table.callSelected.connect(self._populate_form)
        self.window.call_table.deleteCall.connect(self._delete_call)

        self._refresh_call_table()

    def _refresh_call_table(self) -> None:
        start, end = self.window.top_bar.date_range_edit.get_date_range()
        calls = self.calls_port_api.get_calls_by_date_range(start.toPython(), end.toPython())
        self.window.call_table.set_calls(map(call_to_qt_call, calls))

    def _register_call(self, qt_call: QtNewCall) -> None:
        self.calls_port_api.create_call(qt_call_to_call(qt_call))
        self._refresh_call_table()

    def _update_call(self, qt_call: QtCall) -> None:
        self.calls_port_api.update_call(qt_call_to_call(qt_call))
        self._refresh_call_table()

    def _date_range_changed(self, _) -> None:
        self._refresh_call_table()

    def _generate_report(self, generate_report_request: tuple[QDateTime, QDateTime, int, Path]) -> None:
        start = generate_report_request[0].toPython()
        end = generate_report_request[1].toPython()
        interval = generate_report_request[2]
        file_name = str(generate_report_request[3].absolute())
        self.report_port_api.export_report(start, end, timedelta(minutes=interval), file_name,
                                           self.report_port_api.get_flavors().pop())

    def _populate_form(self, id_: int) -> None:
        call = self.calls_port_api.get_call(id_)
        self.window.call_form.set_form_data(call_to_qt_call(call))

    def _delete_call(self, id_: int) -> None:
        self.calls_port_api.delete_call(id_)
        if int(self.window.call_form.id.text()) == id_:
            self.window.call_form.id.setText("None")
        self._refresh_call_table()  # TODO optimize this
        self.window.call_form.reset_fields()

    def run_gui(self) -> None:
        self.window.show()
        self.app.exec()

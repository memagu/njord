from pathlib import Path

from app.adapters.api.qt_adapter_api import QTAdapterAPI
from app.adapters.spi.file_report_exporter_adapter_spi import FileReportExporterAdapterSPI
from app.adapters.spi.sqlite3_adapter_spi import SQLite3AdapterSPI
from app.adapters.spi.text_report_renderer_adapter_spi import TextReportRendererAdapterSPI
from app.configuration.global_config import DATABASE
from app.core.services.calls_service import CallsService
from app.core.services.report_service import ReportService


def njord_gui(database: Path) -> None:
    sqlite3_adapter_spi = SQLite3AdapterSPI(database)
    calls_service = CallsService(sqlite3_adapter_spi)

    text_report_renderer_adapter_spis = (
        TextReportRendererAdapterSPI("text.utf-8"),
    )

    file_report_exporter_adapter_spi = FileReportExporterAdapterSPI()

    report_service = ReportService(sqlite3_adapter_spi, text_report_renderer_adapter_spis,
                                   file_report_exporter_adapter_spi)
    qt_adapter_api = QTAdapterAPI(calls_service, report_service)

    qt_adapter_api.run_gui()


if __name__ == "__main__":
    njord_gui(DATABASE)

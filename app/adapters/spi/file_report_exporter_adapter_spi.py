from app.core.model.report import ReportFlavor
import logging
from pathlib import Path


class FileReportExporterAdapterSPI:

    def export_report(self, data: bytes, name: str, flavor: ReportFlavor) -> None:
        logging.info(f"Saving report of flavor '{flavor}' to '{name}'")
        Path(name).write_bytes(data)

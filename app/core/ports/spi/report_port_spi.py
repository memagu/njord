from typing import Protocol

from app.core.model.report import Report, ReportFlavor


class ReportRendererPortSPI(Protocol):

    def get_flavor(self) -> ReportFlavor:
        ...

    def render_report(self, report: Report) -> bytes:
        ...


class ReportExporterPortSPI(Protocol):

    def export_report(self, data: bytes, name: str, flavor: ReportFlavor) -> None:
        ...

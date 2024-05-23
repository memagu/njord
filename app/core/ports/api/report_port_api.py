from datetime import datetime, timedelta
from typing import Protocol

from app.core.model.report import Report, ReportFlavor, ReportFlavors


class ReportPortAPI(Protocol):

    def export_report(self, start: datetime, end: datetime, interval: timedelta, name: str, flavor: ReportFlavor) -> Report:
        ...

    def get_flavors(self) -> ReportFlavors:
        ...
from dataclasses import dataclass
from datetime import datetime, timedelta

from app.core.model.call import Call


@dataclass(frozen=True)
class Report:
    interval_size: timedelta
    intervals: dict[datetime, tuple[Call, ...]]

    @property
    def calls(self) -> tuple[Call, ...]:
        return tuple({value for values in self.intervals.values() for value in values})


ReportFlavor = str
ReportFlavors = set[ReportFlavor]

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timedelta
from functools import total_ordering
from typing import Optional


@dataclass(frozen=True)
@total_ordering
class Call:
    id: Optional[int]
    phone_number: str
    start_time: datetime
    duration: timedelta
    cases: tuple[str, ...]

    def __eq__(self, other: Call) -> bool:
        return self.start_time == other.start_time

    def __lt__(self, other: Call) -> bool:
        return self.start_time < other.start_time

    @property
    def end(self) -> datetime:
        return self.start_time + self.duration







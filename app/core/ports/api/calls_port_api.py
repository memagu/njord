from datetime import datetime
from typing import Protocol

from app.core.model.call import Call


class CallsPortAPI(Protocol):
    def create_call(self, call: Call) -> Call:
        ...

    def delete_call(self, id_: int) -> Call:
        ...

    def update_call(self, call: Call) -> Call:
        ...

    def get_call(self, id_: int) -> Call:
        ...

    def get_calls_by_date_range(self, start: datetime, end: datetime) -> tuple[Call, ...]:
        ...

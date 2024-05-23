from datetime import datetime

from app.core.model.call import Call
from app.core.ports.spi.calls_port_spi import CallsPortSPI


class CallsService:
    def __init__(self, calls_spi: CallsPortSPI) -> None:
        self.calls_spi = calls_spi

    def create_call(self, call: Call) -> Call:
        assert call.id is None
        return self.calls_spi.store_call(call)

    def delete_call(self, id_: int) -> Call:
        return self.calls_spi.delete_call(id_)

    def update_call(self, call: Call) -> Call:
        assert call.id is not None
        return self.calls_spi.update_call(call)

    def get_call(self, id_: int) -> Call:
        return self.calls_spi.get_call(id_)

    def get_calls_by_date_range(self, start: datetime, end: datetime) -> tuple[Call, ...]:
        assert start <= end
        return self.calls_spi.get_calls_by_date_range(start, end)

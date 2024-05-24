import logging
from collections import defaultdict
from datetime import datetime, timedelta
from math import ceil
from typing import Sequence

from app.core.model.call import Call
from app.core.model.report import Report, ReportFlavors, ReportFlavor
from app.core.ports.spi.calls_port_spi import CallsPortSPI
from app.core.ports.spi.report_port_spi import ReportRendererPortSPI, ReportExporterPortSPI


def _intersecting_intervals(call: Call, initial_half_hour: datetime, interval: timedelta) -> tuple[datetime, ...]:
    if initial_half_hour + interval < call.start_time:
        initial_half_hour = call.start_time

    return tuple(
        initial_half_hour + interval * i
        for i in
        range(ceil((call.end - initial_half_hour).seconds / interval.total_seconds()))
    )


def _interval_groups(calls: Sequence[Call], interval: timedelta) -> dict[datetime, tuple[Call, ...]]:
    """
    Groups calls by intersecting intervals. Assumes that calls are sorted in ascending order.

    :param calls: A sequence of Call objects
    :param interval: The intervals to group in
    :return: A dictionary representing the calls in each interval
    """

    groups = defaultdict(list)
    active_half_hour = datetime.min

    for call in calls:
        intervals = _intersecting_intervals(call, active_half_hour, interval)
        active_half_hour = intervals[-1]

        for _interval in intervals:
            groups[_interval].append(call)

    return {interval: tuple(group) for interval, group in groups.items()}


class ReportService:
    def __init__(self, calls_port_spi: CallsPortSPI, _report_renderer_spis: tuple[ReportRendererPortSPI, ...], report_exporter_spi: ReportExporterPortSPI) -> None:
        self._calls_port_spi = calls_port_spi
        self._report_renderer_spis = _report_renderer_spis
        self._report_exporter = report_exporter_spi

    def _generate_report(self, start: datetime, end: datetime, interval: timedelta) -> Report:
        assert start <= end
        assert interval > timedelta()

        calls = self._calls_port_spi.get_calls_by_date_range(start, end)
        groups = _interval_groups(calls, interval)
        return Report(interval, groups)

    def export_report(self, start: datetime, end: datetime, interval: timedelta, name: str,
                      flavor: ReportFlavor) -> Report:
        report = self._generate_report(start, end, interval)

        try:
            report_renderer = next((report_renderer for report_renderer in self._report_renderer_spis if
                                   report_renderer.get_flavor() == flavor))
            rendered_report = report_renderer.render_report(report)
            self._report_exporter.export_report(rendered_report, name, flavor)
            return report
        except StopIteration:
            logging.exception("Invalid flavor")
            raise ValueError("Invalid flavor")

    def get_flavors(self) -> ReportFlavors:
        return {report_renderer.get_flavor() for report_renderer in self._report_renderer_spis}

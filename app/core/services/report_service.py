import logging
from collections import defaultdict, deque
from datetime import datetime, timedelta
from math import ceil
from typing import Sequence

from app.core.model.call import Call
from app.core.model.report import Report, ReportFlavors, ReportFlavor
from app.core.ports.spi.calls_port_spi import CallsPortSPI
from app.core.ports.spi.report_port_spi import ReportRendererPortSPI, ReportExporterPortSPI


def _intersecting_intervals(call: Call, initial_half_hour: datetime, interval_size: timedelta) -> tuple[datetime, ...]:
    if initial_half_hour + interval_size < call.start_time:
        initial_half_hour = call.start_time

    return tuple(
        initial_half_hour + interval_size * i
        for i in
        range(ceil((call.end - initial_half_hour).seconds / interval_size.total_seconds()))
    )


def _interval_groups(calls: Sequence[Call], interval_size: timedelta) -> dict[datetime, tuple[Call, ...]]:
    """
    Groups calls by intersecting intervals. Assumes that calls are sorted in ascending order.

    :param calls: A sequence of Call objects
    :param interval: The intervals to group in
    :return: A dictionary representing the calls in each interval
    """

    intervals = deque()
    groups = defaultdict(list)

    for call in calls:
        # Remove intervals that are too far to the left
        while intervals and intervals[0] + interval_size < call.start_time:
            intervals.popleft()

        # Determine the initial interval
        initial_interval = intervals[0] if intervals else call.start_time

        # Compute new intersecting intervals
        new_intervals = _intersecting_intervals(call, initial_interval, interval_size)

        # Append data point to all intersecting intervals
        for interval in new_intervals:
            groups[interval].append(call)

        # Initialize intervals deque if empty
        if not intervals:
            intervals = deque(new_intervals)
            continue

        # Skip if the last interval is larger than the last new interval
        if intervals[-1] >= new_intervals[-1]:
            continue

        # Update intervals to include only those intersecting with new intervals
        intervals = deque(new_intervals[new_intervals.index(intervals[-1]):])

    return {interval: tuple(group) for interval, group in groups.items()}


class ReportService:
    def __init__(self, calls_port_spi: CallsPortSPI, _report_renderer_spis: tuple[ReportRendererPortSPI, ...],
                 report_exporter_spi: ReportExporterPortSPI) -> None:
        self._calls_port_spi = calls_port_spi
        self._report_renderer_spis = _report_renderer_spis
        self._report_exporter = report_exporter_spi

    def _generate_report(self, start: datetime, end: datetime, interval_size: timedelta) -> Report:
        assert start <= end
        assert interval_size > timedelta()

        calls = self._calls_port_spi.get_calls_by_date_range(start, end)
        groups = _interval_groups(calls, interval_size)
        return Report(interval_size, groups)

    def export_report(self, start: datetime, end: datetime, interval_size: timedelta, name: str,
                      flavor: ReportFlavor) -> Report:
        report = self._generate_report(start, end, interval_size)

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

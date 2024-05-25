from datetime import timedelta
from functools import reduce

from app.core.model.report import ReportFlavor, Report


def seconds_to_minutes(seconds: int | float) -> int:
    return round(seconds / 60)


class TextReportRendererAdapterSPI:
    def __init__(self, flavor: ReportFlavor, group_separator: str = '#', call_separator: str = '-'):
        self._flavor = flavor
        self._group_separator = group_separator
        self._call_separator = call_separator

    def get_flavor(self) -> ReportFlavor:
        return self._flavor

    def render_report(self, report: Report) -> bytes:
        intervals = sorted(report.intervals.items())

        start = intervals[0][0]
        end = intervals[-1][0]

        data = [
            f"Period: {start.astimezone().isoformat()} -> {end.astimezone().isoformat()}",
            "",
            f"Calls: {len(report.calls)}", f"Initiated {seconds_to_minutes(report.interval_size.total_seconds())} minute intervals: {len(intervals)}",
            f"Active work time: {reduce(lambda td, c: td + c.duration, report.calls, timedelta())}",
            ""
        ]

        for n, (half_hour, group) in enumerate(intervals, 1):
            data.append(f"{f" {n}. {half_hour.isoformat()} ".center(64, self._group_separator)}")
            data.append("")
            data.append(
                f"\n\n{self._call_separator * 48}\n\n".join((
                    '\n'.join((
                        f"Tel: {call.phone_number}",
                        f"Start time: {call.start_time.isoformat()}",
                        f"Duration: Ca. {call.duration}",
                        f"Cases: {", ".join(call.cases)}",
                        f"{seconds_to_minutes(report.interval_size.total_seconds())} minute interval: {half_hour.isoformat()}"
                    )) for call in group
                ))
            )
            data.append("")

        return '\n'.join(data).encode("UTF-8")

from typing import Sequence

from PySide6.QtCore import QDateTime

MAX_INT = (1 << 31) - 1

Call = tuple[int, str, QDateTime, int, tuple[str, ...]]
NewCall = tuple[None, str, QDateTime, int, tuple[str, ...]]

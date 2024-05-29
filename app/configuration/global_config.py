from pathlib import Path

__version__ = "1.0.0"

DATABASE = Path("./njord.db")


def get_version() -> str:
    return __version__

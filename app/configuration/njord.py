from pathlib import Path

from app.configuration.njord_gui import njord_gui

DATABASE = Path("./njord.db")


def main() -> None:
    njord_gui(DATABASE)


if __name__ == "__main__":
    main()

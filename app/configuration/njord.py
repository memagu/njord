from app.configuration.global_config import DATABASE
from app.configuration.njord_gui import njord_gui


def main() -> None:
    njord_gui(DATABASE)


if __name__ == "__main__":
    main()

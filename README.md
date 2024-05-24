# njord
An application for easy logging and reporting of on-call worktime

## Compiling from Source

If you wish to compile the Python program into an executable file, you will need to
install [PyInstaller](https://pypi.org/project/pyinstaller/).

### Installing PyInstaller

Please follow the instructions below to install PyInstaller:

```bash
pip install pyinstaller
```

After PyInstaller has been installed, either `build.cmd` or `build.sh` can be used to compile the source code.

## Architecture
This application uses [hexagonal architecture](https://en.wikipedia.org/wiki/Hexagonal_architecture_(software)) also known as ports and adapters to be as modular as possible.

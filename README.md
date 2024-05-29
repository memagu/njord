# njord
An application for easy logging and reporting of on-call worktime
<hr>

## Installation

### Precompiled executable
Simply download the precompiled executable from the [latest release](https://github.com/memagu/njord/releases/latest). No further installation needed.

### Building from Source Code
* **Prerequisites**:
    * [PyInstaller](https://pypi.org/project/pyinstaller/) is necessary for compiling the source code.
    * All commands should be executed in the root directory of the project.

1. **Install PyInstaller**:
    - **Windows**: `$ pip install pyinstaller`
    - **UNIX**: `$ pip3 install pyinstaller`
2. **Download Source Code**: Fetch the source code for the [latest release](https://github.com/memagu/njord/releases/latest) of Njord.
3. **Set Up Virtual Environment and Install Dependencies**: Create a virtual environment and install the project's dependencies using the appropriate command for your system:
    - **Windows**: `$ py -m venv venv && .\venv\Scripts\activate && pip install -r requirements.txt && deactivate`
    - **UNIX**: `$ python3 -m venv venv && source venv/bin/activate && pip3 install -r requirements.txt && deactivate`
4. **Build the Application**: Execute `build.cmd` or `build.sh` based on your system:
    - **Windows**: `$ .\build.cmd`
    - **UNIX**: `$ chmod +x ./build.sh && ./build.sh`

## Usage
Run the `njord.exe` executable.

## Contributing
Contributions are welcome and greatly appreciated! Every little bit helps, and credit will always be given. You can contribute in many ways:

* **Report Bugs**: Report bugs at the issue tracker. If you are reporting a bug, please include any details about your local setup that might be helpful in troubleshooting.
* **Fix Bugs**: Look through the GitHub issues for bugs. Anything tagged with "bug" is open to whoever wants to implement it.
* **Implement Features**: Look through the GitHub issues for features. Anything tagged with "feature" is open to whoever wants to implement it.
* **Write Documentation**: Njord could always use more documentation, whether as part of the official docs, in docstrings, or even on the web in blog posts, articles, and such.
* **Submit Feedback**: Any issue with the 'question' label is open for feedback, so feel free to share your thoughts and ideas.

For more details, check out our CONTRIBUTING.md guide.

## Licence
This project is licensed under the terms of the MIT license. For more details, see the [LICENSE](LICENSE) file.

## Technical

### Application Architecture
This application uses the [hexagonal architecture](https://en.wikipedia.org/wiki/Hexagonal_architecture_(software)) pattern, also known as ports and adapters, to be as modular, expandable and maintainable as possible.

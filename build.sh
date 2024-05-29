#!/bin/bash

pyinstaller --onefile --noconsole --clean --paths "./venv/lib/python3.12/site-packages" --icon=NONE "./app/configuration/njord.py"
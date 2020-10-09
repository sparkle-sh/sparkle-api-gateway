#!/bin/bash

source ./venv/bin/activate
MISC = $PWD/misc PYTHONPATH=./test/integration ./venv/bin/py.test ./test/integration/*tests.py --verbose --disable-pytest-warnings

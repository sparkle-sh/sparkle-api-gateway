#!/bin/bash

source ./venv/bin/activate
MISC=$(pwd)/test_misc PYTHONPATH=./test/integration ./venv/bin/py.test ./test/integration/*tests.py --verbose --disable-pytest-warnings

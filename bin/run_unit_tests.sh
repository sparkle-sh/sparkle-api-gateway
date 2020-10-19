#!/bin/bash

source ./venv/bin/activate
UTILS_PATH=$(pwd)/test/unit/test_utils PYTHONPATH=./src ./venv/bin/py.test ./test/unit/**/*tests.py --verbose --disable-pytest-warnings
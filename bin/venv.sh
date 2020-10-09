#!/bin/bash

if [ -d ./venv ]; then
    sudo rm -rf ./venv
fi

echo "Generating venv"
sudo python3.7 -m venv ./venv
source ./venv/bin/activate

echo "Upgrading pip"
sudo ./venv/bin/python3.7 -m pip install --upgrade pip
echo "Instaling requirements"
sudo ./venv/bin/python3.7 -m pip install -r ./misc/requirements.txt
echo "Installing test requirements"
sudo ./venv/bin/python3.7 -m pip install -r ./misc/test-requirements.txt

if [ -d ./test/integration/sparkle_test_base ]; then
    echo "Installing test base requirements"
    sudo ./venv/bin/python3.7 -m pip install -r ./test/integration/sparkle_test_base/requirements.txt
fi

echo "Done!"

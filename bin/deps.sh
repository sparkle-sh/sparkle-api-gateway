#!/bin/bash

sudo apt-get install -y python3.7
sudo apt-get install -y python3-setuptools
sudo apt-get install -y python3.7-venv
sudo apt-get install -y build-essential
sudo apt-get install -y python3.7-dev
sudo apt-get install -y libpq-dev

sudo python3.7 -m ensurepip
sudo python3.7 -m pip install virtualenv
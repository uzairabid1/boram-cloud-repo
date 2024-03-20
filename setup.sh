#!/bin/bash

sudo apt-get update
sudo apt-get install -y python3

sudo apt-get install -y python3-venv

python3 -m venv myenv
source myenv/bin/activate

pip install -r requirements.txt

wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb

mv google-chrome-stable_current_amd64.deb /

sudo apt-get -f install /google-chrome-stable_current_amd64.deb

deactivate

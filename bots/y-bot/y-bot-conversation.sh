#! /bin/sh

clear

export PYTHONPATH=../../src;../../libs/MetOffer-1.3.2;.

python3 ../../src/programy/clients/conversation.py --config ./config.windows.yaml --cformat yaml --logging ./logging.windows.yaml


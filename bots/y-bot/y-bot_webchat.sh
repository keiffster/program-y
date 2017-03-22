#! /bin/sh

clear

export PYTHONPATH=$PYTHONPATH:../../src/:./src

python3 ../../src/programy/clients/webchat/chatsrv.py --config ./config.yaml --cformat yaml --logging ./logging.yaml --debug


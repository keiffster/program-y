#! /bin/sh

clear

export PYTHONPATH=.

python3 programy/clients.py --config ../bots/alice2/config.yaml --cformat yaml --logging ../bots/alice2/logging.yaml --bot_root ../bots/alice2/ --debug


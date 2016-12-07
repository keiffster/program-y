#! /bin/sh

clear

export PYTHONPATH=.

python3 programy/clients.py --config ../bots/rosie/config.yaml --cformat yaml --logging ../bots/rosie/logging.yaml --debug


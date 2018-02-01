#! /bin/sh

clear

export PYTHONPATH=../../../src:.

python3 ../../../src/programy/clients/flaskrest.py --config ../../y-bot/config.yaml --cformat yaml --logging ../../y-bot/logging.yaml


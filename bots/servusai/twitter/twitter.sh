#! /bin/sh

clear

export PYTHONPATH=../../../src:.

python3 ../../../src/programy/clients/polling/twitter/client.py --config ./config.yaml --cformat yaml --logging ../../y-bot/logging.yaml

#! /bin/sh

clear

export PYTHONPATH=../../../src:.

python3 ../../../src/programy/clients/restful/flask/client.py --config ../../y-bot/config.yaml --cformat yaml --logging ../../y-bot/logging.yaml


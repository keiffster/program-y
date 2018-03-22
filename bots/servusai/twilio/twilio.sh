#! /bin/sh

clear

export PYTHONPATH=../../../src:.

python3 ../../../src/programy/clients/restful/flask/twilio/client.py --config ./config.yaml --cformat yaml --logging ../../y-bot/logging.yaml


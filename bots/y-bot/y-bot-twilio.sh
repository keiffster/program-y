#! /bin/sh

clear

export PYTHONPATH=../../src:.

python3 ../../src/programy/clients/twilio_client.py --config ./config.yaml --cformat yaml --logging ./logging.yaml


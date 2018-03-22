#! /bin/sh

clear

export PYTHONPATH=../../src:.

python3 ../../src/programy/clients/restful/flask/client.py --config ./config.production.yaml --cformat yaml --logging ./logging.production.yaml


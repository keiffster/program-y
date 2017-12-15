#! /bin/sh

clear

export PYTHONPATH=../../src:.

python3 ../../src/programy/clients/rest.py --config ./config.production.yaml --cformat yaml --logging ./logging.production.yaml


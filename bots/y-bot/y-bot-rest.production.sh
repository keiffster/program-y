#! /bin/sh

clear

export PYTHONPATH=../../src:../../libs/MetOffer-1.3.2:.

python3 ../../src/programy/clients/rest.py --config ./config.production.yaml --cformat yaml --logging ./logging.production.yaml


#! /bin/sh

clear

export PYTHONPATH=$PYTHONPATH:../../src/:./src:../../libs/MetOffer-1.3.2/

python3 ../../src/programy/clients/rest.py --config ./config.yaml --cformat yaml --logging ./logging.yaml --debug


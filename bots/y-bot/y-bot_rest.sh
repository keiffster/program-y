#! /bin/sh

clear

export PYTHONPATH=$PYTHONPATH:../../src/:./src

python3 ../../src/programy/clients/rest.py --config ./config.yaml --cformat yaml --logging ./logging.yaml --debug


#! /bin/sh

clear

export PYTHONPATH=../../../../src:.

python3 ../../../../src/programy/clients/twitter.py --config ./config.yaml --cformat yaml --logging ./logging.yaml
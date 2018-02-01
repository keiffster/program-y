
#! /bin/sh

clear

export PYTHONPATH=../../../../src:.

python3 ../../../../src/programy/clients/tcpsocket.py --config ./config.yaml --cformat yaml --logging ./logging.yaml


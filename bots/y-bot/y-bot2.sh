#! /bin/sh

clear

export PYTHONPATH=../../src:.

python3 -m programy.clients.events.console.client --config ./config.yaml --cformat yaml --logging ./logging.yaml


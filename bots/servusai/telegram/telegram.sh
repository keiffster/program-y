#! /bin/sh

clear

export PYTHONPATH=../../../../src:.

python3 ../../../../src/programy/clients/telegram_client.py --config ./config.yaml --cformat yaml --logging ./logging.yaml


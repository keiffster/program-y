#!/bin/bash

export PYTHONPATH=../../src:.

/usr/bin/python3 ../../src/programy/clients/webchat/chatsrv.py --config ./config.yaml --cformat yaml --logging ./logging.yaml


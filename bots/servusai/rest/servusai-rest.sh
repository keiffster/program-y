#! /bin/sh

# This file is for use on Servusai.com AWS Server

export PYTHONPATH=/opt/program-y/src:.

cd /opt/program-y

python3 /opt/program-y/src/programy/clients/flaskrest.py --config /opt/program-y/bots/multibot/rest/config.yaml --cformat yaml --logging /opt/program-y/bots/multibot/rest/logging.yaml


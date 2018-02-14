#! /bin/sh

# This file is for use on Servusai.com AWS Server

export PYTHONPATH=/opt/program-y/src:.

cd /opt/program-y

python3 /opt/program-y/src/programy/clients/viber_client.py --config /opt/program-y/bots/servusai/viber/config.yaml --cformat yaml --logging /opt/program-y/bots/y-bot/logging.yaml


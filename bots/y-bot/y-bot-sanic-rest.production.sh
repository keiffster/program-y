#! /bin/sh

clear

echo WARNING - Have you installed Sanic before running this [pip install sanic] - WARNING

export PYTHONPATH=../../src:.

python3 ../../src/programy/clients/sanicrest.py --config ./config.production.yaml --cformat yaml --logging ./logging.production.yaml


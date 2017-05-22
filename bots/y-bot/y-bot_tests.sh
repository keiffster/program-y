#! /bin/sh

clear

export PYTHONPATH=../../src:../../libs/MetOffer-1.3.2:.

python3 ../../src/programy/clients/test_runner.py --test_dir ./tests --config ./config.yaml --cformat yaml --logging ./logging.yaml


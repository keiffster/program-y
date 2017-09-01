#! /bin/sh

clear

export PYTHONPATH=../../src:../../libs/MetOffer-1.3.2:.

python3 ../../src/programy/clients/test_runner.py --test_dir ./aiml_tests --config ./test_config.yaml --cformat yaml --logging ./logging.yaml

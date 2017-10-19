#!/usr/bin/env bash

clear

export PYTHONPATH=../../src:../../libs/MetOffer-1.3.2:.

python3 ./test_creator.py $1 $2 $3


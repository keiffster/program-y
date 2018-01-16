#!/usr/bin/env bash

clear

export PYTHONPATH=./src:.

python3 src/botflow.py -flow "../../../bots/botflow/flow/flightbook.csv" -topic flightbook -aiml "../../../bots/botflow/aiml"
#!/bin/sh

export PYTHONPATH=../../src:.

python3 generator.py --directory ./input --output ./output

#! /bin/sh

clear

export PYTHONPATH=../../src/

python3 -m cProfile  -o /tmp/alice2.cprof ../../src/programy/clients/console.py --config ./config.yaml --cformat yaml --logging ./logging.yaml --noloop

pyprof2calltree -k -i /tmp/alice2.cprof



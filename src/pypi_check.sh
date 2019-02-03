#!/usr/bin/env bash

cd /tmp

mkdir pypi

cd pypi

python3 -m venv programy

cd programy

source ./bin/activate

pip3 install programy

deactivate

cd ..
cd ..
rm -Rf pypi

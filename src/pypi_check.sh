#!/usr/bin/env bash

cd /tmp

mkdir pypi

cd pypi

python3 -m venv programy

cd programy

source ./bin/activate

pip3 install --no-cache-dir programy

python3 -m programy.admin.tool

python3 -m programy.admin.tool install y-bot

deactivate

cd ..
cd ..
rm -Rf pypi

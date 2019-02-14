#!/usr/bin/env bash

cd /tmp

mkdir pypi

cd pypi

python3 -m venv programy

cd programy

source cd ./bin/activate

pip3 install --no-cache-dir programy

python3 -m programy.admin.tool

python3 -m programy.admin.tool install textblob

python3 -m programy.admin.tool download y-bot

cd scripts/xnix

deactivate

cd ..
cd ..
rm -Rf pypi

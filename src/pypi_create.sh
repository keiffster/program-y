#!/usr/bin/env bash

echo $1 > version.txt

git tag $1 -m "Version %1 Release"

git push --tags github master

rm dist/*
rm -Rf programy.egg-info

python3 setup.py sdist


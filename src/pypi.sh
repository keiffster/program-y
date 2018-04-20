#!/usr/bin/env bash

git tag 2.0.1 -m "Version 2.0.1"

git push --tags github master

rm dist/*
rm -Rf programy.egg-info

python3 setup.py sdist

twine upload dist/*


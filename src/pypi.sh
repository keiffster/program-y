#!/usr/bin/env bash

git tag x.y -m "Comments"

git push --tags github master

python3 setup.py sdist

twine upload dist/*


#!/usr/bin/env bash

git tag 1.9 -m "Version 1.9 Release"

git push --tags github master

python3 setup.py sdist

twine upload dist/*


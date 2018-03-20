#!/usr/bin/env bash

git tag 2.0-m "Version 2.0 Release"

git push --tags github master

python3 setup.py sdist

twine upload dist/*


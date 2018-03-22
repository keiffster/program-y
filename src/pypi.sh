#!/usr/bin/env bash

git tag 2.0c1 -m "Version 2.0 Candidate 1 Release"

git push --tags github master

python3 setup.py sdist

twine upload dist/*


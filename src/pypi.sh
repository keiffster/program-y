#!/usr/bin/env bash

git tag 2.0rc2 -m "Version 2.0 Release Candidate 2"

git push --tags github master

python3 setup.py sdist

twine upload dist/*


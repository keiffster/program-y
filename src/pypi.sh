#!/usr/bin/env bash

git tag 2.0rc3 -m "Version 2.0 Release Candidate 3"

git push --tags github master

rm dist/*
rm -Rf programy.egg-info

python3 setup.py sdist

twine upload dist/*


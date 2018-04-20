#!/usr/bin/env bash

git tag $1 -m "Version %1 Release"

git push --tags github master

rm dist/*
rm -Rf programy.egg-info

python3 setup.py sdist --version $1

#twine upload dist/*


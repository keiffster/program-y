#!/usr/bin/env bash

clear

rm .coverage
rm -rf ./cover

nosetests --with-coverage --cover-html --cover-erase --with-xunit --cover-branches --cover-package=programy --ignore-files=.*test_runner.* --ignore-files=programytest/clients/restful/asyncio/microsoft/*.py

coverage html -d cover --omit=src/programy/clients/test_runner.py,*__init__.py

open ./cover/index.html

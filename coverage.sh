#!/usr/bin/env bash

clear

export PYTHONPATH=./src:./bots/y-bot/src:.

nosetests --with-coverage --cover-erase --with-xunit --cover-branches --cover-package=programy --ignore-files=.*clients\\facebook.* --ignore-files=.*test_runner.*

coverage html -d cover --omit=src/programy/clients/facebook.py,src/programy/clients/test_runner.py,*__init__.py

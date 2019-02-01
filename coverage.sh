#!/usr/bin/env bash

clear

export PATH=$PATH:~/Library/Python/3.7/bin

nosetests --with-coverage --cover-html --cover-erase --with-xunit --cover-branches --cover-package=programy --ignore-files=.*test_runner.*

coverage html -d cover --omit=src/programy/clients/test_runner.py,*__init__.py

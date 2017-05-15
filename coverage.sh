#!/usr/bin/env bash

clear

export PYTHONPATH=./src:./bots/y-bot/src:./bots/y-bot/libs/MetOffer-1.3.2/

nosetests --with-coverage --cover-erase --with-xunit --cover-branches --cover-package=programy

coverage html -d cover

#!/usr/bin/env bash

clear

export PYTHONPATH=./src:./libs/MetOffer-1.3.2/:./bots/y-bot/src:.

nosetests --with-coverage --cover-erase --with-xunit --cover-branches --cover-package=programy

coverage html -d cover

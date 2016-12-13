#!/usr/bin/env bash

clear

nosetests --with-xcoverage --cover-html --with-xunit --cover-erase --cover-branches --cover-package=programy


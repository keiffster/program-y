#!/usr/bin/env bash

clear

nosetests --cover-html --cover-html-dir=cover --with-xunit --cover-erase --cover-branches --cover-package=programy


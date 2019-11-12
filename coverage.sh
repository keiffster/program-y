#!/usr/bin/env bash

clear
echo "=============================================================================="

rm .coverage*
rm nosetests.xml
rm -rf ./cover
rm -rf ./storage

echo "nosetests running..........."
nosetests --config=nose.cfg
# --cover-package=programy --with-coverage --cover-html --cover-erase --with-xunit --cover-branches --ignore-files=.*test_runner.* --ignore-files=programytest/clients/restful/asyncio/microsoft/*.py

echo "coverage running..........."
coverage html -d cover --omit=src/programy/clients/test_runner.py,*__init__.py

rm -rf ./storage

open ./cover/index.html

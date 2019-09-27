#!/bin/bash

clear
echo "=============================================================================="
echo "pylint running..........."

pylint -v --rcfile=pylint.cfg $(find src/programy -path ./libs -prune -o -name "*.py" -print) . > pylint.log

cat pylint.log

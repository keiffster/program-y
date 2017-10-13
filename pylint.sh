#!/bin/bash
 
pylint --rcfile=pylint.cfg $(find src/programy -path ./libs -prune -o -name "*.py" -print) . > pylint.log

cat pylint.log

#!/bin/bash
 
./pylint3 --rcfile=pylint.cfg $(find src/programy -path ./libs -prune -o -name "*.py" -print) . > pylint.log

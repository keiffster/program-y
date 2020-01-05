#!/usr/bin/env bash

clear
echo "=============================================================================="
echo "pytype running..........."

pytype --config ./pytype.cfg > pytype.log

cat pytype.log


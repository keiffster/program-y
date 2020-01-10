#!/usr/bin/env bash

twine upload --verbose --repository-url https://test.pypi.org/legacy/ dist/*

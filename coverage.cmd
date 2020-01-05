@echo off

SUBST Y: /D
SUBST Y: Z:\Development\Python\Projects\AIML\program-y

SET PYTHONPATH=Y:\src;Y:\bots\y-bot

nosetests --config=nose.cfg

coverage --rcfile=coverage.cfg html

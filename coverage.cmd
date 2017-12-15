@echo off

SUBST Y: /D
SUBST Y: Z:\Development\Python\Projects\AIML\program-y

SET PYTHONPATH=Y:\src;Y:\bots\y-bot

nosetests --with-coverage --cover-erase --with-xunit --cover-branches --cover-package=programy

coverage html -d cover --omit=src\programy\clients\facebook.py,src\programy\clients\test_runner.py,*__init__.py

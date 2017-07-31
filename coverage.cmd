@echo off

SUBST Y: /D
SUBST Y: Z:\Development\Python\Projects\AIML\program-y

SET PYTHONPATH=Y:\src;Y:\libs\MetOffer-1.3.2;Y:\bots\y-bot

nosetests --with-coverage --cover-erase --with-xunit --cover-branches --cover-package=programy

coverage html -d cover


@echo off

cls

SUBST Y: /D
SUBST Y: Z:\Development\Python\Projects\AIML\program-y

SET PYTHONPATH=Y:\src;Y:\libs\MetOffer-1.3.2;Y:\bots\y-bot

python Y:\src\programy\clients\console.py --bot_root Y:\bots\y-bot --config Y:\bots\y-bot\config.windows.yaml --cformat yaml --logging Y:\bots\y-bot\logging.windows.yaml


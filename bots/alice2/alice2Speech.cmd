@echo off

CLS

SET PYTHONPATH=..\..\src;..\..\libs\MetOffer-1.3.2;


python ..\..\src\programy\clients\console.py --config .\config.windows.yaml --cformat yaml --bot_type talk --logging .\logging.windows.yaml
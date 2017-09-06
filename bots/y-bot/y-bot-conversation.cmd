@echo off

CLS

SET PYTHONPATH=..\..\src;..\..\libs\MetOffer-1.3.2;.

python ..\..\src\programy\clients\conversation.py --config .\config.windows.yaml --cformat yaml --logging .\logging.windows.yaml


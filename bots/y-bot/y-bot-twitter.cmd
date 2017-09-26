@echo off

CLS

SET PYTHONPATH=..\..\src;..\..\libs\MetOffer-1.3.2;.

python3 ..\..\src\programy\clients\twitter.py --config .\config.windows.yaml --cformat yaml --logging .\logging.windows.yaml

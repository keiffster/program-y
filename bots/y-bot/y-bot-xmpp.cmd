@echo off

CLS

SET PYTHONPATH=..\..\src;..\..\libs\MetOffer-1.3.2;.

python3 ..\..\src\programy\clients\xmpp.py --config .\config.windows.yaml --cformat yaml --logging .\logging.windows.yaml


SET PROGRAMY=y:\program-y

SET PYTHONPATH=%PROGRAMY\src;%PROGRAMY\libs\MetOffer-1.3.2;%PROGRAMY\bots\professor

python3 %PROGRAMY\src\programy\clients\console.py --bot_root %PROGRAMY\bots\professor --config %PROGRAMY\bots\professor\config.yaml --cformat yaml --logging %PROGRAMY\bots\professor\logging.yaml


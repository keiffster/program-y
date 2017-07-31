SET PROGRAMY=y:\program-y

SET PYTHONPATH=%PROGRAMY\src;%PROGRAMY\libs\MetOffer-1.3.2;%PROGRAMY\bots\rosie

python3 %PROGRAMY\src\programy\clients\console.py --bot_root %PROGRAMY\bots\rosie --config %PROGRAMY\bots\rosie\config.yaml --cformat yaml --logging %PROGRAMY\bots\rosie\logging.yaml


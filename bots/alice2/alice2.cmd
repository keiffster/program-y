SET PROGRAMY=y:\program-y

SET PYTHONPATH=%PROGRAMY\src;%PROGRAMY\libs\MetOffer-1.3.2;%PROGRAMY\bots\alice2

python3 %PROGRAMY\src\programy\clients\console.py --bot_root %PROGRAMY\bots\alice2 --config %PROGRAMY\bots\alice2\config.yaml --cformat yaml --logging %PROGRAMY\bots\alice2\logging.yaml


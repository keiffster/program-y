#! /bin/sh

clear

export PYTHONPATH=../../src:.

python3 ../../src/utils/test_runner/test_runner.py --test_file ./aiml_tests/games/blackjack.tests --config ./test_config.yaml --cformat yaml --logging ./logging.yaml --qna_file /tmp/y-bot.tests

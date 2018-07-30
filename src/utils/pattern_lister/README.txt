Pattern Lister
==============
Creates a single CSV file containing all AIML patterns from the files specified in the directory ( and sub directories )

Useful tool for debugging and seeing the spread of AIML categories across files.

Usage:
    python3 pattern_lister aiml_dir csv_file

CSV File Format:

../../../bots/y-bot/aiml/core/system/repeat.aiml, #, AGAIN, #
../../../bots/y-bot/aiml/core/profanity/insults.aiml, #, B, ASTERISK, ASTERISK, ASTERISK, ASTERISK
../../../bots/y-bot/aiml/extensions/energy/directdebits.aiml, #, CANCEL, #, DIRECT, DEBUT, #
../../../bots/y-bot/aiml/extensions/energy/directdebits.aiml, #, CHANGE, #, DIRECT, DEBUT, #
../../../bots/y-bot/aiml/extensions/maps/maps.aiml, #, DISTANCE, *, BETWEEN, *
../../../bots/y-bot/aiml/extensions/maps/maps.aiml, #, DISTANCE, *, TO, *
../../../bots/y-bot/aiml/extensions/maps/maps.aiml, #, DISTANCE, BETWEEN, *, AND, *
../../../bots/y-bot/aiml/extensions/maps/maps.aiml, #, DISTANCE, FROM, *, TO, *
../../../bots/y-bot/aiml/core/personality.aiml, #, GLASS, HALF, #
../../../bots/y-bot/aiml/personality/hello.aiml, #, HEY, #
../../../bots/y-bot/aiml/personality/hello.aiml, #, HI, #
../../../bots/y-bot/aiml/personality/hello.aiml, #, HIYA, #
../../../bots/y-bot/aiml/extensions/maps/maps.aiml, #, HOW, #, GET, FROM, *, TO, *
../../../bots/y-bot/aiml/extensions/energy/directdebits.aiml, #, HOW, MUCH, #, DIRECT, DEBIT, #

Program-Y is an Python 3.x implementation of an AIML 2.0 Grammar

For more details of what AIML then head over to the spec at
http://alicebot.blogspot.co.uk/2013/01/aiml-20-draft-specification-released.html

For full documentation, tutorials and other helpful information, see the GitHub pages site
https://keiffster.github.io/program-y/

Whats New
==========

0.7.0 introduces some interesting new features, specifically around the use of external services

y-bot introduces extensions to call UK Met Office Weather and Google Maps. This work introduces 2 new features
people need to be aware of

1) execute() method signatire on extensions has changed to include bot and clientid parameters. This gives Extensions access
to the bot and brain configurations. This will break existing code until you change your methods

2) Met Office requires a API key to use. To do this following the informaiton in the wiki page at
https://github.com/keiffster/program-y/wiki/Met-Officer-Weather-API

When you have an API Key, create the file license.keys in config folder of your bot, and make sure there is a
reference to this config.yaml under the files section

    files:
        license_keys: $BOT_ROOT/config/license.keys

This file should have the format

    METOFFICE_API_KEY=xxxx-xxxxxxx-xxxxxx-xxxxxx-xx-xxxxxxxx

You can now ask y_bot for the weather and directions and distance between locations
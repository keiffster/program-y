Y-Bot is my bot, its the bot I wanted to develop from the start and will grow over time

The intention is to create a great core bot with an exciting personality that has a good
core general knowledge and then to create suite of extended grammars for different purposes

I have a background in Energy, Finance, Telecoms and Gaming and therefore feel I have a
pretty good grasp of the types of questions a bot would ask and how they should be responded to

The ultimate intention is to create a series of Y-Bot tailored to specific industries

Whats New
==========

0.6 introduces some interesting new features, specifically around the use of external services

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


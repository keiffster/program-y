# Program-Y

Program Y is a fully compliant AIML 2.1 chatbot framework written in Python 3. It includes an entire platform for 
building your own chat bots using Artificial Intelligence Markup Language, or AIML for short. 
For more information about Program-y, its features and its history then check out the Background page.
q
## New in 4.0

### Baseline Release
Version 4.0 is a baseline release to prepare the ground work for a number of major changes in 2020. 
It includes the addition of over 2000 unit tests which brings coverage up to 99% of the core system and 96% overall
Along with the unit tests, we have refactored major parts of the code base for ease of use, performance and long term
sustainability. A number of defects have also been corrected due to the addition of the unit tests

### Configuration Changes
The major change is in the configuration file struture. This has been refactored and while a breaking change, its 
structural, rather than content and aligns the configuration files with the internal structure of the bot architecture. 
The main change is the inclusion of brains and bots contains, so a configuration file now looks like
```yaml
console:
    bots:
      bot1:
        brains:
          brain1:
          brain2:
      bot2:
        brains:
          brain3
```
Fixing config files should be as simple as introducing the bots and brains elements and shifting bot and brain elements 
a couple of tabs right

### Embeddable Clients
The third major feature is a complete refresh of the embeddable client, which now provides 3 simple ways to add a bot
to you Python app in as little as 2 lines of code
```python
from programy.clients.embed.basic import EmbeddedBasicBot

my_bot = EmbeddedBasicBot()

print("Response = %s" % my_bot.ask_question("Hello"))
```
For more information on this feature, see [Embedded Bots](./Tutorial-Embedded-Bots)

### Unified Naming
A number of configuration items have had their names changed so that all variables use underscore '_' as a 
space seperator rather than a mix of underscore and dash '-'. The list of changes re

* default_userid
* default_get
* default_property
* default_map
* default_response
* default_response_srai

The convention going forward is that all variables will use underscore '_' as a space seperator

## Contact
There are a number of ways you can get help

* [Github](https://github.com/keiffster/program-y/issues) Raise an issue directly
* [Slack](https://program-y.slack.com) Talk live with the Dev Team
* [Gitter](https://gitter.im/Program-y) Talk with the Dev Team
* Email (See below) although I don't check it every day
* Twitter, but more of an announcement channel

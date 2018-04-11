# Readme info:

Version: 2.0.0<br/>
Authors: Keith Sterling <br/>
Date: 22nd March 2018 <br/>

## V2.0

### New Features
Version 2.0 brings some important changes to the overall Program-Y platform and ecosystem including

* Thread Safety across all processing
* Multiple Bots per Client, useful to mix AIML and ML processing
* Multiple Brains per Bot, useful to seperate grammars, including langauge specific
* Wide variety of clients including
  * Console
  * Web
  * Facebook
  * Twitter
  * SMS
  * XMPP (Google Hangouts)
  * Telegram
  * Slack
  * Viber
  * Kik
  * Line
  * TCP Socket
  * REST
* Improved Logging which now includes more info about client, bot and brain
* Support for AIML 2.x Rich Media
* Support for Emojis
* Natively support Pypi instalation
* Asynchronous Scheduling of events, useful to carry out time dependent call backs, such as "remind me 7:00am to wake up" or
"Set a timer for 20 minutes". The bot will then call back to your client asynchronously with the text or parsed grammar

### Rich Media
Rich media is an exciting enhancement to AIML proposed by the [AIML Foundation](http://aiml.foundation) which adds a range
of new capabilities to the AIML langauge to help in building engaging interfaces. Rich media introduces a number of new
template tags including
* button
* card
* carousel
* delay
* image
* link
* list
* location
* reply
* split
* video
Rather than just returning plain text, using these tags allows you to build conversations that including buttons, clickable links, images, videos
and more complex UI structures

### Breaking Changes
Along with this work there are some break changes for anyone actively developing their own extensions or clients. The biggest change is
that any Python method that used used to take the parameters 'bot, clientid' has been modified and these 2 variables replaced
with the object client_context. Which stores conversational state, including the client making the call, the bot used to ask the
question, the brain that processed the grammar and parse depth. If you have built and extension, the code would have looking something like

```python
class SomeExtension(Extension):
    def execute(self, bot, clientid, data):
        return "OK"
```
This should now be refactored to 
```python
class SomeExtension(Extension):
    def execute(self, client_context, data):
        return "OK"
```

# Introduction

Program Y is an AIML interpretor written in Python. It includes an entire Python 3 framework for building you own chat bots using
Artificial Intelligence Markup Language, or AIML for short. 

Programy-Y is fully cross plaform, running on 

* Mac OSX
* Linux
* Windows

100% Support for all AIML 2.0 Tags plus all Pandora bot ones they never documented

* Full support for al AIML 2.0 Tags
* RDF Support through addtriple, deletetriple, select, uniq and uniq
* List processing with First and Rest
* Advanced learn support including resetlearn and resetlearnf
* Full Out Of Band Support
* Full embedded XML/HTML Support
* Dynamic Sets, Maps and Variables

Program Y is extremely extensible, you can

* Add you own AIML tags
* Add you own Spelling Checker
* Support User Authorisation
* Support User Authentication
* Add your own Out Out Band (OOB) tags
* Add Dynamic Sets in Python
* Add Dynamic Maps in Python
* Add Dynamic Variables in Python
* Run a variety of clients

Program-Y comes with a base set of grammars for various industry sectors, including

* Energy Industry
* Banking
* Telecoms
* Weather
* Surveys
* News Feeds
* Maps

# Using Program-Y

Full documentation is available on [Program Y Wiki](https://github.com/keiffster/program-y/wiki)

After installation from the Github repository you can chat with your Program Y by running one of the many bots found in the 
\bot folder. These include

* Y-Bot - My own bot under development
* Professor - A huge knowledge base of questions and answers
* Alice2 - AIML 2 version of the famous Alice chat bot
* Roise - An AIML base set of grammars for creating your own bot

See the individual folders for unix and windows scripts required to run a bot.

# Tutorial

Once you have got the system installed and have run one or more of the bots, head over to the [Tutorial](https://github.com/keiffster/program-y/wiki/AIML-Tutorial) on the Wiki for a full 
run down of everything possible in AIML






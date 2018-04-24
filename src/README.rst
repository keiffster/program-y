
Version 2.0
============
This release brings some important changes to the overall Program-Y platform and ecosystem including

- Thread Safety across all processing
- Multiple Bots per Client, useful to mix AIML and ML processing
- Multiple Brains per Bot, useful to separate grammars, including langauge specific
- Wide variety of clients including
  - Console
  - Web
  - Facebook
  - Twitter
  - SMS
  - XMPP (Google Hangouts)
  - Telegram
  - Slack
  - Viber
  - Kik
  - Line
  - TCP Socket
  - REST
- Improved Logging which now includes more info about client, bot and brain
- Support for AIML 2.x Rich Media
- Support for Emojis
- Natively support Pypi installation
- Asynchronous Scheduling of events

Rich Media
----------
Rich media is an exciting enhancement to AIML proposed by the [AIML Foundation](http://aiml.foundation) which adds a range
of new capabilities to the AIML language to help in building engaging interfaces. Rich media introduces a number of new
template tags including
- button
- card
- carousel
- delay
- image
- link
- list
- location
- reply
- split
- video
Rather than just returning plain text, using these tags allows you to build conversations that including buttons, clickable links, images, videos
and more complex UI structures

Introduction
------------
Program Y is an AIML interpreter written in Python. It includes an entire Python 3 framework for building you own chat bots using
Artificial Intelligence Markup Language, or AIML for short. 

Program Y is fully cross platform, running on

- Mac OSX
- Linux
- Windows

100% Support for all AIML 2.0 Tags plus all Pandora bot ones they never documented

- Full support for al AIML 2.0 Tags
- RDF Support through addtriple, deletetriple, select, uniq and uniq
- List processing with First and Rest
- Advanced learn support including resetlearn and resetlearnf
- Full Out Of Band Support
- Full embedded XML/HTML Support
- Dynamic Sets, Maps and Variables

Program Y is extremely extensible, you can

- Add you own AIML tags
- Add you own Spelling Checker
- Support User Authorisation
- Support User Authentication
- Add your own Out Out Band (OOB) tags
- Add Dynamic Sets in Python
- Add Dynamic Maps in Python
- Add Dynamic Variables in Python
- Run a variety of clients

Program-Y comes with a base set of grammars for various industry sectors, including

- Energy Industry
- Banking
- Telecoms
- Weather
- Surveys
- News Feeds
- Maps

Using Program-Y
----------------
Full documentation is available on `Program Y Wiki <https://github.com/keiffster/program-y/wiki>`_

Program-Y ships with a very basic bot that has a single answer, after installation you can chat with your Program Y by running one of the many bots found in GitHub repo

- `Y-Bot <https://github.com/keiffster/y-bot>`_
- `Alice2 <https://github.com/keiffster/alice2-y>`_
- `Rosie <https://github.com/keiffster/rosie-y>`_
- `Professor <https://github.com/keiffster/professor-y>`_

See the individual folders for unix and windows scripts required to run a bot.

Getting Started
---------------
Once you have got the system installed and have run one or more of the bots, head over to the
`Tutorial <https://github.com/keiffster/program-y/wiki/AIML-Tutorial>`_ on the Wiki for a full
run down of everything possible in AIML






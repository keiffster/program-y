
Coming in Version 3.1
======================
- Translation. You can now speak to it in any language supported by google translate and also have the answers in any language. This means you can keep your rules in English bur open your bot to a variety of language users
- Sentiment. Each question asked has a sentiment score attached to it and the bot also keeps a running score for the whole conversation. Both values are available through runtime variables to be used to adjust your responses
- Client account linking. You can now link accounts across all clients and therefore continue conversations. For example start on the web client, link Facebook and continue there and then link twitter and continue there then swap between all 3 at will preserving the entire conversation. This works across all 11 supported clients


Version 3.0
============
New in this release

- Support for SQL Storage (Currently tested on MariaDB and MySQL)
- Support for NoSQL Storage (Currently tested on MongoDB and Redis)
- Full support for AIML 2.x (Including Rich Media)


Where Used
===========
Program-Y is used in a variety of projects, some of which are public

- `Orange Research <https://oma-chatbot.kmt.orange.com/>`_
- `Cataluna University <https://bpm.cs.upc.edu/chatbot>`_
- `Heriot Watt University <https://www.researchgate.net/publication/319723461_Hybrid_Chat_and_Task_Dialogue_for_More_Engaging_HRI_Using_Reinforcement_Learning>`_
- Major automotive manufacturer

If you want to be listed, please let me know


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






# Program-Y

Program Y is a fully compliant AIML 2.0 chatbot framework written in Python 3. It includes an entire platform for building your own chat bots using Artificial Intelligence Markup Language, or AIML for short. 
For more information about Program-y, its features and its history then check out the Background page.

## New in 3.5
Version 3.5 ships with new [Google Client](https://github.com/keiffster/program-y/wiki/Client-Google). 
As well as supporting DialogFlow and hence
Google Assistant, it also enables access to the wide range of clients that DialogFlow supports including Cortana, Alexa, 
Skype and Cisco intelligent agents


## Installation
You can now install Program-y directly from PyPi with the follow commands

```bash
pip3 install programy
```

For more information about installing directly from GitHub or getting set up to develop and contriute to Program-y check out
the [Advanced Installation Options](https://github.com/keiffster/program-y/wiki/Install_Advanced) section

### Additional Installation

#### Sanic REST Server
Program-Y typically uses Flask as its underlying framework for REST servers and the webchast client.
If however you intend to use the Sanic REST client on Linux or OSX then you need to install those dependencies as follows
```bash
pip3 install sanic
```

## Post Installation
Once you have a basic install you can then use the Admin Tool
The Admin Tool is a useful tool when installing via pip from PyPi. 

To run the admin tool, you can call it directly from the command line with the following 
```bash
python3 -m programy.admin.tool
```

To get a list of the available command line options use the 'help' command
```bash
python3 -m programy.admin.tool help

Available commands are:

        help
        list
        download <bot-name>
        install <component>

```

### Available Bots
To get a list of the available components to download and/or install use the 'list' command
```bash
python3 -m programy.admin.tool list
Available bots are:

        alice2-y
        professor-y
        rosie-y
        talk-y
        y-bot
        template-y
        traintimes-y

        To download use 'python3 -m programy.admin.tool donwload <bot-name>'

Additional components are:

        textblob

        To install use 'python3 -m programy.admin.tool install <component>'
```

To download a specific bot into the current directory, use the 'download'
```bash
python3 -m programy.admin.tool download [bot-name]
```

### Additional Components
To install additional components required for advanced NLP, use the 'install'
```bash
python3 -m programy.admin.tool install [component]
```

NOTE. Program-y now uses TextBlob ( built on NLTK ) for advanced text and sentiment processing. 
To operate effectively TextBlob ( and therefore NLTK ) requires the download of additional data files, therefore
you need to run the following command after initial installation
```bash
python3 -m programy.admin.tool install textblob
```

## Running Your Bot
If everything has completed successfully you now have Program-y installed and your choice of bot
downloaded and read to go.

Each bot ships with a number of scripts to get you start which allow you to run 
you bot from the command line as a console. These are found in the'scripts ' folder of your bot. In this folder you will find
2 subfolders 'xnix' for scripts that work in both OSX and Linux installations and 'wiindows' for scripts that work in a windows installation

The console script is always named the same as the bot with the .sh or .cmd extension depdending upon your platform. As an example
running the bot in console mode on OSX is as follows

```bash
cd scripts/xnix
./y-bot.sh
Loading, please wait...
/Users/keith/Documents/Development/Python/Projects/AIML/y-bot/scripts/xnix
No bot root argument set, defaulting to [../../config/xnix]
Found a total of 1 errors in your grammars, check your errors store
Found a total of 6 duplicates in your grammars, check your duplicates store
Y-Bot, App: v3.0.0 Beta 1 Grammar v1.6.0, initiated March 14, 2017
Hi, how can I help you today?
>>> 
```
Your bot is now up and running and ready for you to talk to it, enjoy!




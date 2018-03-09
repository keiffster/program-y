"""
Copyright (c) 2016-2018 Keith Sterling http://www.keithsterling.com

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated
documentation files (the "Software"), to deal in the Software without restriction, including without limitation
the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software,
and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the
Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO
THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT,
TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
"""

AIML_TEMPLATE = """<?xml version="1.0" encoding="UTF-8"?>
<aiml version="2.0">
    <category>
        <pattern>HELLO</pattern>
        <template>Welcome to Program-Y</template>
    </category>
</aiml>
"""

LOGGING_TEMPLATE = """
version: 1
disable_existing_loggers: False

formatters:
  simple:
    format: '%(asctime)s  %(name)-10s %(levelname)-7s %(message)s'

handlers:
    file:
        class: logging.handlers.RotatingFileHandler
        formatter: simple
        filename: /tmp/bot.log
        maxBytes: 20972152
        backupCount: 10
        encoding: utf-8

root:
    level: DEBUG
    handlers:
        - file
"""

CONFIG_TEMPLATE = """
bot:
    license_keys: $BOT_ROOT/config/license.keys

    prompt: ">>>"

    initial_question: Hi, how can I help you today?
    initial_question_srai: YINITIALQUESTION
    default_response: Sorry, I don't have an answer for that!
    default_response_srai: YEMPTY
    empty_string: YEMPTY
    exit_response: So long, and thanks for the fish!
    exit_response_srai: YEXITRESPONSE

    override_properties: true

    max_question_recursion: 1000
    max_question_timeout: 60
    max_search_depth: 100
    max_search_timeout: 60

    conversations:
      type: file
      config_name: file_storage
      empty_on_start: true

    file_storage:
      dir: $BOT_ROOT/conversations

brain:

     # Overrides
    overrides:
      allow_system_aiml: true
      allow_learn_aiml: true
      allow_learnf_aiml: true

    # Defaults
    defaults:
      default-get: unknown
      default-property: unknown
      default-map: unknown
      learn-filename: $BOT_ROOT/aiml/learnf.aiml

    # Nodes
    nodes:
      pattern_nodes: $BOT_ROOT/config/pattern_nodes.conf
      template_nodes: $BOT_ROOT/config/template_nodes.conf

    # Binary
    binaries:
      save_binary: false
      load_binary: false
      binary_filename: /tmp/bot.brain
      load_aiml_on_binary_fail: false

    # Braintree
    braintree:
      file: /tmp/braintree.xml
      content: xml

    files:
        aiml:
            files: $BOT_ROOT/aiml
            extension: .aiml
            directories: true
            errors:
              file: /tmp/bot_errors.csv
              format: csv
              encoding: utf-8
              delete_on_start: true
            duplicates:
              file: /tmp/bot_duplicates.csv
              format: csv
              encoding: utf-8
              delete_on_start: true
            conversation:
              file: /tmp/bot-conversation.csv
              format: csv
              delete_on_start: true
        sets:
            files: $BOT_ROOT/sets
            extension: .txt
            directories: false
        maps:
            files: $BOT_ROOT/maps
            extension: .txt
            directories: false
        denormal: $BOT_ROOT/config/denormal.txt
        normal: $BOT_ROOT/config/normal.txt
        gender: $BOT_ROOT/config/gender.txt
        person: $BOT_ROOT/config/person.txt
        person2: $BOT_ROOT/config/person2.txt
        properties: $BOT_ROOT/config/properties.txt
        rdf:
            files:  $BOT_ROOT/rdf
            extension: .txt
            directories: true
        preprocessors: $BOT_ROOT/config/preprocessors.conf
        postprocessors: $BOT_ROOT/config/postprocessors.conf
        regex_templates: $BOT_ROOT/config/regex-templates.txt
        variables: $BOT_ROOT/config/default-variables.txt

    services:
        REST:
            classname: programy.services.rest.GenericRESTService
            method: GET
            host: 0.0.0.0
        Pannous:
            classname: programy.services.pannous.PannousService
            url: http://weannie.pannous.com/api
        Pandora:
            classname: programy.services.pandora.PandoraService
            url: http://www.pandorabots.com/pandora/talk-xml
        Wikipedia:
            classname: programy.services.wikipediaservice.WikipediaService
        DuckDuckGo:
            classname: programy.services.duckduckgo.DuckDuckGoService
            url: http://api.duckduckgo.com

    security:
        authentication:
            classname: programy.security.authenticate.passthrough.BasicPassThroughAuthenticationService
            denied_srai: AUTHENTICATION_FAILED
        authorisation:
            classname: programy.security.authorise.usergroupsauthorisor.BasicUserGroupAuthorisationService
            denied_srai: AUTHORISATION_FAILED
            usergroups: $BOT_ROOT/config/roles.yaml

    dynamic:
        variables:
            gettime: programy.dynamic.variables.datetime.GetTime
        sets:
            numeric: programy.dynamic.sets.numeric.IsNumeric
            roman:   programy.dynamic.sets.roman.IsRomanNumeral
        maps:
            romantodec: programy.dynamic.maps.roman.MapRomanToDecimal
            dectoroman: programy.dynamic.maps.roman.MapDecimalToRoman
"""

REST_CONFIG="""
rest:
  host: 0.0.0.0
  port: 5000
  debug: false
  workers: 4
"""

WEBCHAT_CONFIG = """
webchat:
  host: 0.0.0.0
  port: 8080
  debug: false
"""

TWITTER_CONFIG = """
twitter:
  polling: true
  polling_interval: 49
  streaming: false
  use_status: true
  use_direct_message: true
  auto_follow: true
  storage: file
  storage_location: $BOT_ROOT/storage/twitter.data
  welcome_message: Thanks for following me, send me a message and I'll try and help
"""

XMPP_CONFIG = """
xmpp:
  server: talk.google.com
  port: 5222
  xep_0030: true
  xep_0004: true
  xep_0060: true
  xep_0199: true
"""

SOCKET_CONFIG = """
socket:
  host: 127.0.0.1
  port: 9999
  queue: 5
  debug: true
"""

INITIAL_PROPERTIES="""
name:Y-Bot
birthdate:%s

grammar_version:0.0.1
app_version: 0.0.1

pannous: true
pandora: true
wikipedia: true
duckduckgo: true
newsapi: true
weather: true
mapping: true
geocode: true

jsenabled: false
"""

CONSOLE_SHELL_SCRIPT = """
#! /bin/sh
clear
%s
python3 -m programy.clients.console --config ./config.yaml --cformat yaml --logging ./logging.yaml
"""

WEBCHAT_SHELL_SCRIPT = """
#! /bin/sh
clear
%s
python3 -m programy.clients.webchat.chatsrv --config ./config.yaml --cformat yaml --logging ./logging.yaml
"""

REST_SHELL_SCRIPT = """
#! /bin/sh
clear
%s
python3 -m programy.clients.rest --config ./config.yaml --cformat yaml --logging ./logging.yaml
"""

XMPP_SHELL_SCRIPT = """
#! /bin/sh
clear
%s
python3 -m programy.clients.xmpp --config ./config.yaml --cformat yaml --logging ./logging.yaml
"""

TWITTER_SHELL_SCRIPT = """
#! /bin/sh
clear
%s
python3 -m programy.clients.twitter --config ./config.yaml --cformat yaml --logging ./logging.yaml
"""

SOCKET_SHELL_SCRIPT = """
#! /bin/sh
clear
%s
python3 -m programy.clients.socket --config ./config.yaml --cformat yaml --logging ./logging.yaml
"""

CONSOLE_WINDOWS_CMD = """
@echo off
CLS
mkdir .\temp
%s
python .-m programy.clients.comsole --config .\config.windows.yaml --cformat yaml --logging .\logging.windows.yaml
"""

WEBCHAT_WINDOWS_CMD = """
@echo off
CLS
mkdir .\temp
%s
python .-m programy.clients.webchat.chatsrv --config .\config.windows.yaml --cformat yaml --logging .\logging.windows.yaml
"""

REST_WINDOWS_CMD = """
@echo off
CLS
mkdir .\temp
%s
python .-m programy.clients.rest --config .\config.windows.yaml --cformat yaml --logging .\logging.windows.yaml
"""

XMPP_WINDOWS_CMD = """
@echo off
CLS
mkdir .\temp
%s
python .-m programy.clients.xmpp --config .\config.windows.yaml --cformat yaml --logging .\logging.windows.yaml
"""

TWITTER_WINDOWS_CMD = """
@echo off
CLS
mkdir .\temp
%s
python .-m programy.clients.twitter --config .\config.windows.yaml --cformat yaml --logging .\logging.windows.yaml
"""

SOCKET_WINDOWS_CMD = """
@echo off
CLS
mkdir .\temp
%s
python .-m programy.clients.socket --config .\config.windows.yaml --cformat yaml --logging .\logging.windows.yaml
"""


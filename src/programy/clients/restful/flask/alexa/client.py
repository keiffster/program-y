#https://developer.amazon.com/blogs/post/Tx14R0IYYGH3SKT/Flask-Ask-A-New-Python-Framework-for-Rapid-Alexa-Skills-Kit-Development
#https://blog.craftworkz.co/flask-ask-a-tutorial-on-a-simple-and-easy-way-to-build-complex-alexa-skills-426a6b3ff8bc
#https://developer.amazon.com/alexa/console/ask/test/amzn1.ask.skill.93b9463d-3706-4454-830a-aeb0232241d4/development/en_GB/

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
from programy.utils.logging.ylogger import YLogger

import logging
from flask import Flask
from flask_ask import Ask, question, question, session

from programy.clients.restful.flask.client import FlaskRestBotClient
from programy.clients.restful.flask.alexa.config import AlexaConfiguration


class AlexaBotClient(FlaskRestBotClient):

    def __init__(self, argument_parser=None):
        FlaskRestBotClient.__init__(self, 'alexa', argument_parser)

        YLogger.debug(self, "Alexa Client is running....")

        print("Alexa Client loaded")

        logging.getLogger("flask_ask").setLevel(self.configuration.ask_debug_level)

    def get_launch_message(self):
        return "Welcome, I am the Boracle, ask me something"

    def ask_question(self, userid, question):
        response = ""
        try:
            client_context = self.create_client_context(userid)
            response = client_context.bot.ask_question(client_context, question, responselogger=self)
        except Exception as e:
            print("Error asking Alexa: ", e)
        return response

if __name__ == "__main__":

    ALEXA_CLIENT = None

    print("Initiating Alexa Client...")
    APP = Flask(__name__)

    print("Initiating Ask Client...")
    ask = Ask(APP, "/")

    @ask.launch
    def launch_boracle():
        response = APP.get_launch_message()
        return question(response)

    @ask.intent("AskBoracle")
    def ask_boracle(text):
        response = APP.ask_question('alexa', text)
        return question(response)

    @ask.intent("AskWho")
    def ask_who(text):
        question = "WHO " + text
        response = APP.ask_question('alexa', question)
        return question(response)

    @ask.intent("AskWhat")
    def ask_what(text):
        question = "WHAT " + text
        response = APP.ask_question('alexa', question)
        return question(response)

    @ask.intent("AskWhy")
    def ask_why(text):
        question = "WHY " + text
        response = APP.ask_question('alexa', question)
        return question(response)

    @ask.intent("AskWhere")
    def ask_where(text):
        question = "WHERE " + text
        response = APP.ask_question('alexa', question)
        return question(response)

    @ask.intent("AskWhen")
    def ask_when(text):
        question = "WHEN " + text
        response = APP.ask_question('alexa', question)
        return question(response)

    @ask.intent("AskHow")
    def ask_how(text):
        question = "HOW " + text
        response = APP.ask_question('alexa', question)
        return question(response)

    @ask.intent("AskIf")
    def ask_if(text):
        question = "IF " + text
        response = APP.ask_question('alexa', question)
        return question(response)

    @ask.intent("AskCould")
    def ask_could(text):
        question = "COULD " + text
        response = APP.ask_question('alexa', question)
        return question(response)

    @ask.intent("AskWould")
    def ask_could(text):
        question = "WOULD " + text
        response = APP.ask_question('alexa', question)
        return question(response)

    ALEXA_CLIENT = AlexaBotClient()
    ALEXA_CLIENT.run(APP)


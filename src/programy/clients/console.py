"""
Copyright (c) 2016-17 Keith Sterling http://www.keithsterling.com

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated
documentation files (the "Software"), to deal in the Software without restriction, including without limitation
the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software,
and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO
THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT,
TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
"""

import logging

from programy.clients.client import BotClient
from programy.config.sections.client.console import ConsoleConfiguration
from programy.context import BotQuestionContext

import pyttsx3
import speech_recognition as sr

class ConsoleBotClient(BotClient):

    def __init__(self, argument_parser=None):
        self.clientid = "Console"
        BotClient.__init__(self, argument_parser)

    def set_environment(self):
        self.bot.brain.properties.add_property("env", "Console")

    def get_client_configuration(self):
        return ConsoleConfiguration()

    def add_client_arguments(self, parser):
        parser.add_argument('--context', dest='context', action='store_true', help='displays additional conversation context')

    def parse_args(self, arguments, parsed_args):
        arguments.context = parsed_args.context

    def run(self):
        if self.arguments.noloop is False:
            logging.info("Entering conversation loop...")
            running = True
            self.display_response(self.bot.get_version_string)
            self.display_response(self.bot.brain.post_process_response(self.bot, self.clientid, self.bot.initial_question))
            while running is True:
                try:
                    question = self.get_question()

                    context = None
                    if self.arguments.context is True:
                        context = BotQuestionContext()

                    response = self.bot.ask_question(self.clientid, question, bot_question_context=context)

                    if response is None:
                        response = self.bot.ask_question(self.clientid, 'default aiml response')
                        self.display_response(response)
                        self.log_unknown_response(question)

                    else:
                        self.display_response(response)

                        if context is not None:
                            context.display(output_func=print)

                        self.log_response(question, response)

                except KeyboardInterrupt:
                    running = False
                    self.display_response(self.bot.exit_response)
                except Exception as excep:
                    logging.exception(excep)
                    logging.error("Oops something bad happened !")
                    self.display_response(self.bot.default_response)
                    self.log_unknown_response(question)

    def get_question(self, input_func=input):
        ask = "%s "%self.bot.prompt
        return input_func(ask)

    def display_response(self, response, output_func=print):
        output_func(response)

if __name__ == '__main__':
    def run():
        print("Loading, please wait...")
        console_app = ConsoleBotClient()
        console_app.run()
    run()

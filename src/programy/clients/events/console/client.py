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

import logging

from programy.clients.events.client import EventBotClient
from programy.clients.events.console.config import ConsoleConfiguration

class ConsoleBotClient(EventBotClient):

    def __init__(self, argument_parser=None):
        self.running = False
        EventBotClient.__init__(self, "Console", argument_parser)

    def get_description(self):
        return 'ProgramY AIML2.0 Console Client'

    def get_client_configuration(self):
        return ConsoleConfiguration()

    def add_client_arguments(self, parser=None):
        return

    def parse_args(self, arguments, parsed_args):
        return

    def get_question(self, client_context, input_func=input):
        ask = "%s " % client_context.bot.prompt
        return input_func(ask)

    def display_startup_messages(self, client_context):
        self.display_response(client_context.bot.get_version_string)
        initial_question = client_context.bot.get_initial_question(client_context)
        self.display_response(initial_question)

    def display_response(self, response, output_func=print):
        output_func(response)

    def process_question_answer(self, client_context):
        question = self.get_question(client_context)
        response = client_context.bot.ask_question(client_context , question, responselogger=self)
        self.display_response(response)
        return question

    def wait_and_answer(self):
        running = True
        try:
            client_context = self.create_client_context(self._configuration.client_configuration.default_userid)
            self.process_question_answer(client_context)
        except KeyboardInterrupt as keye:
            running = False
            client_context = self.create_client_context(self._configuration.client_configuration.default_userid)
            self.display_response(client_context.bot.get_exit_response(client_context))
        except Exception as excep:
            logging.exception(excep)
            if logging.getLogger().isEnabledFor(logging.ERROR):
                logging.error("Oops something bad happened !")
        return running

    def run(self):

        if self.arguments.noloop is False:
            if logging.getLogger().isEnabledFor(logging.INFO):
                logging.info("Entering conversation loop...")

            client_context = self.create_client_context(self._configuration.client_configuration.default_userid)
            self.display_startup_messages(client_context)

            running = True
            while running is True:
                running = self.wait_and_answer()

        else:
            if logging.getLogger().isEnabledFor(logging.DEBUG):
                logging.debug("noloop set to True, exiting...")


if __name__ == '__main__':

    def run():
        print("Loading, please wait...")
        console_app = ConsoleBotClient()
        console_app.run()

    run()

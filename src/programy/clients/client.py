"""
Copyright (c) 2016-17 Keith Sterling http://www.keithsterling.com

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated
documentation files (the "Software"), to deal in the Software without restriction, including without limitation
the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software,
and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions
of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO
THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT,
TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
"""

import os
import logging
import logging.config
import yaml

from programy.config.file.factory import ConfigurationFactory
from programy.clients.args import CommandLineClientArguments
from programy.bot import Bot
from programy.brain import Brain
from programy.config.programy import ProgramyConfiguration

class BotClient(object):

    def __init__(self, argument_parser=None):
        self._arguments = self.parse_arguments(argument_parser=argument_parser)
        self.initiate_logging(self.arguments)
        self.load_configuration(self.arguments)

        self._brain = Brain(self.configuration.brain_configuration)
        self.bot = Bot(self._brain, self.configuration.bot_configuration)

        self.set_environment()

    @property
    def arguments(self):
        return self._arguments

    def get_description(self):
        return 'ProgramY AIML2.0 Console Client'

    def add_client_arguments(self, parser=None):
        # Nothing to add
        pass

    def parse_arguments(self, argument_parser):
        client_args = CommandLineClientArguments(self, parser=argument_parser)
        client_args.parse_args()
        return client_args

    def initiate_logging(self, arguments):
        if arguments.logging is not None:
            with open(arguments.logging, 'r+') as yml_data_file:
                logging_config = yaml.load(yml_data_file)
                logging.config.dictConfig(logging_config)
                logging.info("Now logging under configuration")
        else:
            print("Warning. No logging configuration file defined, using defaults...")

    def get_client_configuration(self):
        """
        By overriding this class in you Configuration file, you can add new configurations
        and stil use the dynamic loader capabilities
        :return: Client configuration object
        """
        raise NotImplemented("You must override this and return a config string")

    def load_configuration(self, arguments):
        if arguments.bot_root is None:
            if arguments.config_filename is not None:
                arguments.bot_root = os.path.dirname(arguments.config_filename)
            else:
                arguments.bot_root = "."
            print("No bot root argument set, defaulting to [%s]" % arguments.bot_root)

        if arguments.config_filename is not None:
            self.configuration = ConfigurationFactory.load_configuration_from_file(self.get_client_configuration(), arguments.config_filename, arguments.config_format, arguments.bot_root)
        else:
            print ("No configuration file specified, using defaults only !")
            self.configuration = ProgramyConfiguration(self.get_client_configuration())

    def set_environment(self):
        self.bot.brain.properties.add_property("env", "Unknown")

    def run(self):
        pass

    def log_unknown_response(self, question):
        pass

    def log_response(self, question, answer):
        pass

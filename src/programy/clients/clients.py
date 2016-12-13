"""
Copyright (c) 2016 Keith Sterling

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
import yaml
import argparse
import logging.config
import os
from programy.config import ConfigurationFactory, ClientConfiguration
from programy.bot import Bot
from programy.brain import Brain

class ClientArguments(object):

    def __init__(self):
        self.parser = argparse.ArgumentParser(description='ProgramY AIML2.0 Console Client')
        self.add_arguments()

    def add_arguments(self):
        self.parser.add_argument('--bot_root', dest='bot_root', help='root folder for all bot configuration data')
        self.parser.add_argument('--config', dest='config', help='configuration file location')
        self.parser.add_argument('--cformat', dest='cformat', help='configuration file format (yaml|json|ini)')
        self.parser.add_argument('--logging', dest='logging', help='logging configuration file')
        self.parser.add_argument('--debug', dest='debug', action='store_true', help='run in debug mode')
        self.parser.add_argument('--noloop', dest='noloop', action='store_true', help='do not enter conversation loop')

    def parse_args(self):
        self.args = self.parser.parse_args()

    @property
    def bot_root(self):
        return self.args.bot_root

    @bot_root.setter
    def bot_root(self, root):
        self.args.bot_root = root

    @property
    def logging(self):
        return self.args.logging

    @property
    def config_filename(self):
        return self.args.config

    @property
    def config_format(self):
        return self.args.cformat

    @property
    def debug(self):
        return self.args.debug

    @property
    def noloop(self):
        return self.args.noloop


class BotClient(object):

    def __init__(self):
        self.arguments = self.parse_arguements ()
        self.initiate_logging(self.arguments)
        self.load_configuration(self.arguments)
        self.initiate_bot(self.configuration)

    def parse_arguements(self):
        client_args = ClientArguments()
        client_args.parse_args()
        return client_args

    def initiate_logging(self, arguments):
        if arguments.logging is not None:
            with open(arguments.logging, 'r+') as yml_data_file:
                logging_config = yaml.load(yml_data_file)
                logging.config.dictConfig(logging_config) #['logging'])
                logging.info("Now logging under configuration")
        else:
            print ("Warning. No logging configuration file defined, using defaults...")

    def get_client_configuration(self):
        """
        By overriding this class in you Configuration file, you can add new configurations
        and stil use the dynamic loader capabilities
        :return: Client configuration object
        """
        return ClientConfiguration()

    def load_configuration(self, arguments):
        if arguments.bot_root is None:
            arguments.bot_root = os.path.dirname(arguments.config_filename)
            print ("No bot root argument set, defaulting to [%s]" % arguments.bot_root)

        self.configuration = self.get_client_configuration()

        ConfigurationFactory.load_configuration_from_file(self.configuration, arguments.config_filename, arguments.config_format, arguments.bot_root)

    def initiate_bot(self, configuration):
        self._brain = Brain (configuration.brain_configuration)
        self.bot = Bot(self._brain, configuration.bot_configuration)
        self.set_environment()

    def set_environment(self):
        self.bot.brain.properties.add_property("env", "Unknown")

    def run(self):
        pass

    def log_unknown_response(self, question):
        pass

    def log_response(self, question, answer):
        pass


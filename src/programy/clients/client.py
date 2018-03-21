"""
Copyright (c) 2016-2018 Keith Sterling http://www.keithsterling.com

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
import logging.config
import yaml

from programy.utils.logging.ylogger import YLogger

from programy.config.file.factory import ConfigurationFactory
from programy.clients.args import CommandLineClientArguments
from programy.bot import Bot
from programy.config.programy import ProgramyConfiguration
from programy.context import ClientContext
from programy.utils.license.keys import LicenseKeys


class ResponseLogger(object):

    def log_unknown_response(self, question):
        return

    def log_response(self, question, answer):
        return


class BotFactory(object):

    def __init__(self, client, configuration):
        self._client = client
        self._bots = {}
        self.loads_bots(configuration)

    def loads_bots(self, configuration):
        for config in configuration.configurations:
            bot = Bot(config, client=self._client)
            self._bots[bot.id] = bot

    # TODO Replace this with a bot selector
    def select_bot(self):
        return next (iter (self._bots.values()))


class BotClient(ResponseLogger):

    def __init__(self, id, argument_parser=None):
        self._id = id

        self._arguments = self.parse_arguments(argument_parser=argument_parser)

        self.initiate_logging(self.arguments)

        self._configuration = None
        self.load_configuration(self.arguments)
        self.parse_configuration()

        self._license_keys = LicenseKeys()
        self.load_license_keys()
        self.get_license_keys()

        self._bot_factory = BotFactory(self, self.configuration.client_configuration)

    def ylogger_type(self):
        return "client"

    @property
    def configuration(self):
        return self._configuration

    @property
    def id(self):
        return self._id

    @property
    def arguments(self):
        return self._arguments

    @property
    def license_keys(self):
        return self._license_keys

    def get_description(self):
        raise NotImplementedError("You must override this and return a client description")

    def add_client_arguments(self, parser=None):
        # Nothing to add
        return

    def parse_configuration(self):
        # Nothing to add
        return

    def parse_args(self, arguments, parsed_args):
        # Nothing to add
        return

    def parse_arguments(self, argument_parser):
        client_args = CommandLineClientArguments(self, parser=argument_parser)
        client_args.parse_args(self)
        return client_args

    def load_license_keys(self):
        if self.configuration is not None:
            if self.configuration.client_configuration.license_keys is not None:
                self._license_keys.load_license_key_file(self.configuration.client_configuration.license_keys)
            else:
                YLogger.warning(self, "No client configuration setting for license_keys")
        else:
            YLogger.warning(self, "No configuration defined when loading license keys")

    def get_license_keys(self):
        return

    def initiate_logging(self, arguments):
        if arguments.logging is not None:
            with open(arguments.logging, 'r+', encoding="utf-8") as yml_data_file:
                logging_config = yaml.load(yml_data_file)
                logging.config.dictConfig(logging_config)
                YLogger.info(self, "Now logging under configuration")
        else:
            print("Warning. No logging configuration file defined, using defaults...")

    def get_client_configuration(self):
        """
        By overriding this class in you Configuration file, you can add new configurations
        and stil use the dynamic loader capabilities
        :return: Client configuration object
        """
        raise NotImplementedError("You must override this and return a subclassed client configuration")

    def load_configuration(self, arguments):
        if arguments.bot_root is None:
            if arguments.config_filename is not None:
                arguments.bot_root = os.path.dirname(arguments.config_filename)
            else:
                arguments.bot_root = "."
            print("No bot root argument set, defaulting to [%s]" % arguments.bot_root)

        if arguments.config_filename is not None:
            self._configuration = ConfigurationFactory.load_configuration_from_file(self.get_client_configuration(),
                                                                                   arguments.config_filename,
                                                                                   arguments.config_format,
                                                                                   arguments.bot_root)
        else:
            print("No configuration file specified, using defaults only !")
            self._configuration = ProgramyConfiguration(self.get_client_configuration())

    def create_client_context(self, userid):
        client_context = ClientContext(self, userid)
        client_context.bot = self._bot_factory.select_bot()
        client_context.brain = client_context.bot._brain_factory.select_brain()
        return client_context

    def run(self):
        raise NotImplementedError("You must override this and implement the logic to run the client")


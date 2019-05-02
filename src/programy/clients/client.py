"""
Copyright (c) 2016-2019 Keith Sterling http://www.keithsterling.com

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
from programy.config.programy import ProgramyConfiguration
from programy.context import ClientContext
from programy.utils.license.keys import LicenseKeys
from programy.utils.substitutions.substitues import Substitutions
from programy.scheduling.scheduler import ProgramyScheduler
from programy.clients.render.text import TextRenderer
from programy.utils.classes.loader import ClassLoader
from programy.storage.factory import StorageFactory
from programy.utils.email.sender import EmailSender
from programy.triggers.manager import TriggerManager
from programy.triggers.system import SystemTriggers
from programy.clients.ping.responder import PingResponder
from programy.clients.botfactory import BotFactory
from programy.clients.response import ResponseLogger


class BotClient(ResponseLogger):

    def __init__(self, id, argument_parser=None):
        self._id = id
        self._license_keys = LicenseKeys()
        self._storage = None
        self._scheduler = None
        self._email = None
        self._trigger_mgr = None
        self._configuration = None
        self._ping_responder = None

        self._questions = 0

        self._arguments = self.parse_arguments(argument_parser=argument_parser)

        self.initiate_logging(self.arguments)

        self._subsitutions = Substitutions()
        if self.arguments.substitutions is not None:
            self._subsitutions.load_substitutions(self.arguments.substitutions)

        self.load_configuration(self.arguments)
        self.parse_configuration()

        self.load_storage()

        self._bot_factory = BotFactory(self, self.configuration.client_configuration)

        self.load_license_keys()
        self.get_license_keys()
        self._configuration.client_configuration.check_for_license_keys(self._license_keys)

        self.load_scheduler()

        self.load_renderer()

        self.load_email()

        self.load_trigger_manager()

        self.load_ping_responder()

    def ylogger_type(self):
        return "client"

    @property
    def num_questions(self):
        return self._questions

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

    @property
    def scheduler(self):
        return self._scheduler

    @property
    def storage_factory(self):
        return self._storage

    @property
    def bot_factory(self):
        return self._bot_factory

    @property
    def renderer(self):
        return self._renderer

    @property
    def trigger_manager(self):
        return self._trigger_mgr

    @property
    def ping_responder(self):
        return self._ping_responder

    def get_description(self):
        if self.configuration is not None:
            if self.configuration.client_configuration is not None:
                return self.configuration.client_configuration.description
        return "Bot Client"

    def get_question_counts(self):
        return self.bot_factory.get_question_counts()

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
        if self.storage_factory.entity_storage_engine_available(StorageFactory.LICENSE_KEYS) is True:
            storage_engine = self.storage_factory.entity_storage_engine(StorageFactory.LICENSE_KEYS)
            keys_store = storage_engine.license_store()
            keys_store.load(self._license_keys)
        else:
            YLogger.warning(self, "No storage factory setting for license_keys")

    def get_license_keys(self):
        return

    def initiate_logging(self, arguments):
        if arguments.logging is not None:
            try:
                with open(arguments.logging, 'r+', encoding="utf-8") as yml_data_file:
                    logging_config = yaml.load(yml_data_file, Loader=yaml.FullLoader)
                    logging.config.dictConfig(logging_config)
                    YLogger.info(self, "Now logging under configuration")

            except Exception as excep:
                YLogger.exception(self, "Failed to open logging configuration [%s]", excep, arguments.logging)
        else:
            print("Warning. No logging configuration file defined, using defaults...")

    def get_client_configuration(self):
        """
        By overriding this class in you Configuration file, you can add new configurations
        and stil use the dynamic loader capabilities
        :return: Client configuration object
        """
        raise NotImplementedError("You must override this and return a subclassed client configuration")

    def load_configuration(self, arguments, subs: Substitutions = None):
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
                                                                                    arguments.bot_root,
                                                                                    subs)
        else:
            print("No configuration file specified, using defaults only !")
            self._configuration = ProgramyConfiguration(self.get_client_configuration())

    def load_scheduler(self):
        if self.configuration.client_configuration.scheduler is not None:
            YLogger.debug(None, "Loading Scheduler")
            self._scheduler = ProgramyScheduler(self, self.configuration.client_configuration.scheduler)
            self._scheduler.start()

    def load_email(self):
        if self._configuration.client_configuration.email is not None:
            YLogger.debug(None, "Loading Email Manager")
            self._email = EmailSender(self._configuration.client_configuration.email)

    def load_trigger_manager(self):
        if self._configuration.client_configuration.triggers is not None:
            YLogger.debug(None, "Loading Trigger Manager")
            self._trigger_mgr = TriggerManager.load_trigger_manager(self._configuration.client_configuration.triggers)

    def load_storage(self):
        self._storage = StorageFactory()
        if self.configuration.client_configuration.storage is not None:
            YLogger.debug(None, "Loading Storage Factory")
            self._storage.load_engines_from_config(self.configuration.client_configuration.storage)
        else:
            print("No storage defined!")

    def load_renderer(self):
        try:
            if self.get_client_configuration().renderer is not None:
                YLogger.debug(None, "Loading Renderer")
                clazz = ClassLoader.instantiate_class(self.get_client_configuration().renderer.renderer)
                self._renderer = clazz(self)
                return

        except Exception as e:
            YLogger.exception(None, "Failed to load config specified renderer", e)

        self._renderer = self.get_default_renderer()

    def get_default_renderer(self):
        return TextRenderer(self)

    def create_client_context(self, userid):
        client_context = ClientContext(self, userid)
        client_context.bot = self._bot_factory.select_bot()
        client_context.brain = client_context.bot._brain_factory.select_brain()
        return client_context

    def load_ping_responder(self):

        self._ping_responder = PingResponder(self)

        self._ping_responder.register_with_healthchecker()

    def startup(self):
        if self._trigger_mgr is not None:
            self._trigger_mgr.trigger(event=SystemTriggers.SYSTEM_STARTUP)

        if self._ping_responder is not None:
            PingResponder.init_ping_response(self._ping_responder)

    def shutdown(self):
        if self._trigger_mgr is not None:
            self._trigger_mgr.trigger(event=SystemTriggers.SYSTEM_SHUTDOWN)

        if self._ping_responder is not None:
            self._ping_responder.shutdown_ping_service()

    def process_question(self, client_context, question):
        raise NotImplementedError("You must override this and implement the logic to create a response to the question")

    def render_response(self, client_context, response):
        raise NotImplementedError("You must override this and implement the logic to process the response by rendering"
                                  " using a RCS renderer")

    def process_response(self, client_context, response):
        raise NotImplementedError("You must override this and implement the logic to display the response to the user")

    def run(self):
        raise NotImplementedError("You must override this and implement the logic to run the client")


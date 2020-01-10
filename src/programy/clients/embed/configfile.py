"""
Copyright (c) 2016-2020 Keith Sterling http://www.keithsterling.com

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
import os
import sys
import json
import yaml
from programy.clients.events.console.client import ConsoleBotClient
from programy.config.file.yaml_file import YamlConfigurationFile
from programy.config.programy import ProgramyConfiguration
from programy.clients.args import CommandLineClientArguments
from programy.utils.substitutions.substitues import Substitutions
from programy.clients.events.console.config import ConsoleConfiguration


class EmbeddedConfigFileBot(ConsoleBotClient):

    def __init__(self, config_filename, logging_filename=None):
        self._config_filename = config_filename

        filepath = os.path.dirname(__file__) + os.sep
        if logging_filename is not None:
            self._logging_filename = logging_filename
        else:
            self._logging_filename = filepath + 'basicbot/logging.yaml'

        ConsoleBotClient.__init__(self, "Console")

    def _render_callback(self):
        return False

    def parse_arguments(self, argument_parser):
        client_args = CommandLineClientArguments(self, parser=None)
        if self._logging_filename is not None:
            client_args._logging = self._logging_filename
        return client_args

    def load_configuration(self, arguments, subs: Substitutions = None):
        client_config = self.get_client_configuration()
        self._configuration = ProgramyConfiguration(client_config)

        yaml_file = YamlConfigurationFile()
        yaml_file.load_from_file(self._config_filename, client_config, ".")

    @staticmethod
    def generate_default_config_file(format):
        config = ConsoleConfiguration()
        data = {config.section_name: {}}
        config.to_yaml(data[config.section_name], True)
        if format == 'json':
            print(json.dumps(data, indent=4))

        elif format == 'yaml':
            print(yaml.dump(data, sort_keys=False))

        else:
            print ("Invalid data format 'json' or 'yaml' only!")

if __name__ == '__main__':

    if sys.argv[1] == 'run':
        config_file = sys.argv[2]
        logging_file = None
        if len(sys.argv) == 4:
            logging_file = sys.argv[3]

        print("Loading Bot Brain....please wait!")
        my_bot = EmbeddedConfigFileBot(config_file, logging_file)

        client_context = my_bot.create_client_context("testuser")
        response = my_bot.process_question(client_context, "Hello")
        print("Asked 'Hello', Response '%s'" % response)

    elif sys.argv[1] == 'config':
        EmbeddedConfigFileBot.generate_default_config_file(sys.argv[2])


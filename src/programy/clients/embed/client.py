"""
Copyright (c) 2016-2019 Keith Sterling http://www.keithsterling.com

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
import sys
from programy.clients.events.console.client import ConsoleBotClient
from programy.config.file.yaml_file import YamlConfigurationFile
from programy.config.programy import ProgramyConfiguration
from programy.clients.args import CommandLineClientArguments


class MyEmbeddedBot(ConsoleBotClient):

    def __init__(self, config_filename):
        self._config_filename = config_filename
        ConsoleBotClient.__init__(self, "Console")

    def parse_arguments(self, argument_parser):
        client_args = CommandLineClientArguments(self, parser=None)
        return client_args

    def load_configuration(self, arguments):

        client_config = self.get_client_configuration()
        self._configuration = ProgramyConfiguration(client_config)

        yaml_file = YamlConfigurationFile()
        yaml_file.load_from_file(self._config_filename, client_config, ".")


if __name__ == '__main__':

    my_bot = MyEmbeddedBot(sys.argv[1])

    client_context = my_bot.create_client_context("testuser")

    response = my_bot.process_question(client_context, "Hello")

    print("Response = ", response)


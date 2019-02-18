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

import logging
import argparse


class ClientArguments(object):

    def __init__(self, client, parser=None):
        self._bot_root = "."
        self._logging = logging.DEBUG
        self._config_name = "config.yaml"
        self._config_format = "yaml"
        self._no_loop = False
        self._substitutions = None

    def parse_args(self, client):
        pass

    @property
    def bot_root(self):
        return self._bot_root

    @bot_root.setter
    def bot_root(self, root):
        self._bot_root = root

    @property
    def logging(self):
        return self._logging

    @property
    def config_filename(self):
        return self._config_name

    @property
    def config_format(self):
        return self._config_format

    @property
    def noloop(self):
        return self._no_loop

    @property
    def substitutions(self):
        return self._substitutions


class CommandLineClientArguments(ClientArguments):

    def __init__(self, client, parser=None):
        self.args = None
        self._bot_root = None
        self._logging = None
        self._config_name = None
        self._config_format = None
        self._no_loop = False
        self._substitutions = None

        ClientArguments.__init__(self, client)
        if parser is None:
            self.parser = argparse.ArgumentParser()
        else:
            self.parser = parser

        self.parser.add_argument('--bot_root', dest='bot_root', help='root folder for all bot configuration data')
        self.parser.add_argument('--config', dest='config', help='configuration file location')
        self.parser.add_argument('--substitutions', dest='substitutions', help='values to substitute in the config file')
        self.parser.add_argument('--cformat', dest='cformat', help='configuration file format (yaml|json|ini)')
        self.parser.add_argument('--logging', dest='logging', help='logging configuration file')
        self.parser.add_argument('--noloop', dest='noloop', action='store_true', help='do not enter conversation loop')

        client.add_client_arguments(self.parser)

    def parse_args(self, client):
        self.args = self.parser.parse_args()
        self._bot_root = self.args.bot_root
        self._logging = self.args.logging
        self._config_name = self.args.config
        self._config_format = self.args.cformat
        self._no_loop = self.args.noloop
        self._substitutions = self.args.substitutions
        client.parse_args(self, self.args)

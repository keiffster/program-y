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
import argparse
import yaml

from programy.clients.events.console.config import ConsoleConfiguration
from programy.clients.events.tcpsocket.config import SocketConfiguration
from programy.clients.polling.slack.config import SlackConfiguration
from programy.clients.polling.telegram.config import TelegramConfiguration
from programy.clients.polling.twitter.config import TwitterConfiguration
from programy.clients.polling.xmpp.config import XmppConfiguration
from programy.clients.restful.config import RestConfiguration
from programy.clients.restful.flask.facebook.config import FacebookConfiguration
from programy.clients.restful.flask.kik.config import KikConfiguration
from programy.clients.restful.flask.line.config import LineConfiguration
from programy.clients.restful.flask.twilio.config import TwilioConfiguration
from programy.clients.restful.flask.viber.config import ViberConfiguration
from programy.clients.restful.sanic.config import SanicRestConfiguration
from programy.utils.console.console import outputLog


class ConfigurationWriter:

    def __init__(self):
        pass    # pragma: no cover

    def add_to_config(self, config_data, configuration, defaults=True):
        config_data[configuration.id] = {}
        configuration.to_yaml(config_data[configuration.id], defaults)

    def execute(self, args):

        config_data = {}

        if args is None:
            raise Exception("Args empty")

        if args.clients is None:
            raise Exception("No clients defined")

        if 'all' in args.clients or 'console' in args.clients:
            self.add_to_config(config_data, ConsoleConfiguration(), args.defaults)

        if 'all' in args.clients or 'socket' in args.clients:
            self.add_to_config(config_data, SocketConfiguration(), args.defaults)

        if 'all' in args.clients or 'slack' in args.clients:
            self.add_to_config(config_data, SlackConfiguration(), args.defaults)

        if 'all' in args.clients or 'telegram' in args.clients:
            self.add_to_config(config_data, TelegramConfiguration(), args.defaults)

        if 'all' in args.clients or 'twitter' in args.clients:
            self.add_to_config(config_data, TwitterConfiguration(), args.defaults)

        if 'all' in args.clients or 'xmpp' in args.clients:
            self.add_to_config(config_data, XmppConfiguration(), args.defaults)

        if 'all' in args.clients or 'rest' in args.clients:
            self.add_to_config(config_data, RestConfiguration(name="rest"))

        if 'all' in args.clients or 'facebook' in args.clients:
            self.add_to_config(config_data, FacebookConfiguration(), args.defaults)

        if 'all' in args.clients or 'kik' in args.clients:
            self.add_to_config(config_data, KikConfiguration(), args.defaults)

        if 'all' in args.clients or 'line' in args.clients:
            self.add_to_config(config_data, LineConfiguration(), args.defaults)

        if 'all' in args.clients or 'twilio' in args.clients:
            self.add_to_config(config_data, TwilioConfiguration(), args.defaults)

        if 'all' in args.clients or 'viber' in args.clients:
            self.add_to_config(config_data, ViberConfiguration(), args.defaults)

        if 'all' in args.clients or 'sanic' in args.clients:
            self.add_to_config(config_data, SanicRestConfiguration(name="sanic"))

        client_config = ConsoleConfiguration()

        bot_config = client_config.configurations[0]

        self.add_to_config(config_data, bot_config, args.defaults)

        brain_config = bot_config.configurations[0]

        self.add_to_config(config_data, brain_config, args.defaults)

        self.write_yaml(args.file, config_data)

    def write_yaml(self, filename, data):
        outputLog(self, "Writing new config file to [%s]" % filename)
        try:
            with open(filename, 'w') as outfile:
                yaml.dump(data, outfile, default_flow_style=False)

        except Exception as excep:
            outputLog(self, "Failed to write new config file [%s] - [%s]" % (filename, str(excep)))

    @staticmethod
    def create_arguments():
        parser = argparse.ArgumentParser(description='Program-Y Configuration Writer')

        parser.add_argument('-f', '--file', default="config.yaml", help="Name of file to create")
        parser.add_argument('-c', '--clients', nargs='+',
                            help="Name of client config to create, use multiple times or all")
        parser.add_argument('-d', '--defaults', action='store_true',
                            help="Create all config settings with default values")

        return parser

    @staticmethod
    def run(args=None):
        parser = ConfigurationWriter.create_arguments()
        try:
            app = ConfigurationWriter()

            if args is None:
                app.execute(parser.parse_args())

            else:
                app.execute(args)

        except Exception as excep:
            outputLog(None, "Error: [%s]" % str(excep))
            parser.print_help()


if __name__ == '__main__':      # pragma: no cover
    ConfigurationWriter.run()   # pragma: no cover

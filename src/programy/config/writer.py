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


class ConfigurationWriter(object):

    def add_to_config(self, config_data, configuration, defaults=True):
        config_data[configuration.id] = {}
        configuration.to_yaml(config_data[configuration.id], defaults)

    def execute(self, args):

        config_data = {}

        if args is None:
            raise Exception ("Args empty")

        if args.clients is None:
            raise Exception ("No clients defined")

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

        bot_config = client_config._bot_configs[0]

        self.add_to_config(config_data, bot_config, args.defaults)

        brain_config = bot_config._brain_configs[0]

        self.add_to_config(config_data, brain_config, args.defaults)

        self.write_yaml(args.file, config_data)

    def write_yaml(self, filename, data):
        print("Writing new config file to", filename)
        try:
            with open(filename, 'w') as outfile:
                yaml.dump(data, outfile, default_flow_style=False)

        except Exception as excep:
           print("Failed to write new config file [%s]", filename)

    @staticmethod
    def create_arguments():
        parser = argparse.ArgumentParser(description='Program-Y Configuration Writer')

        parser.add_argument('-f', '--file', default="config.yaml", help="Name of file to create" )
        parser.add_argument('-c', '--clients', nargs='+', help="Name of client config to create, use multiple times or all" )
        parser.add_argument('-d', '--defaults', action='store_true', help="Create all config settings with default values" )

        return parser

    @staticmethod
    def run():
        parser = ConfigurationWriter.create_arguments()
        try:
            app = ConfigurationWriter()
            app.execute(parser.parse_args())
        except Exception as e:
            raise(e)
            parser.print_help()

if __name__ == '__main__':

    ConfigurationWriter.run ()



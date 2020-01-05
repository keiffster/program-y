import unittest

from programy.bot import Bot
from programy.clients.polling.xmpp.client import XmppBotClient
from programy.clients.polling.xmpp.config import XmppConfiguration
from programy.clients.polling.xmpp.xmpp import XmppClient
from programy.config.bot.bot import BotConfiguration
from programy.clients.render.text import TextRenderer
from programytest.clients.arguments import MockArgumentParser


class MockBot(Bot):

    def __init__(self, config):
        Bot.__init__(self, config)
        self._answer = ""

    def ask_question(self, clientid: str, text: str, srai=False, responselogger=None):
        return self._answer


class MockLicenseKeys(object):

    def __init__(self, keys=None):
        if keys is not None:
            self.keys = keys
        else:
            self.keys = {}

    def get_key(self, key):
        return self.keys[key]


class MockXmppClient(XmppClient):

    def __init__(self, bot_client, jid, password):
        self.registered = False
        self.server_url = None
        self.port_no = 0
        self.block = False
        self.event_handlers = []
        self.registered_plugins = []
        self.response = None
        self.should_connect = True
        XmppClient.__init__(self, bot_client, jid, password)

    def add_event_handler(self, name, pointer):
        self.event_handlers.append(name)

    def register_xep_plugins(self, configuration):
        self.registered = True
        super(MockXmppClient, self).register_xep_plugins(configuration)

    def run(self, server, port, block=True):
        self.server_url = server
        self.port_no = port
        self.block = block

    def register_plugin(self, name):
        self.registered_plugins.append(name)

    def send_response(self, msg, response):
        self.response = response

    def connect(self, address=tuple(), reattempt=True,
                use_tls=True, use_ssl=False):
        return self.should_connect


class MockXmppBotClient(XmppBotClient):

    def __init__(self, argument_parser=None):
        XmppBotClient.__init__(self, argument_parser)
        self.mock_xmpp_client = None

    def get_client_configuration(self):
        config = XmppConfiguration()
        config._server = "Server"
        config._port = 8080
        config._xep_0030 = True
        config._xep_0004 = True
        config._xep_0060 = True
        config._xep_0199 = True
        return config

    def get_license_keys(self):
        self._username = "XMPPUSERNAME"
        self._password = "XMPPPASSWORD"

    def create_client(self, username, password):
        self.mock_xmpp_client = MockXmppClient(self, username, password)
        return self.mock_xmpp_client

    def create_bot(self):
        self._bots.append(MockBot(BotConfiguration()))


class XmppBotClientTests(unittest.TestCase):

    def test_xmpp_bot_client_init(self):
        arguments = MockArgumentParser()
        client = MockXmppBotClient(arguments)
        self.assertIsNotNone(client)
        self.assertIsNotNone(client.get_client_configuration())
        self.assertIsInstance(client.get_client_configuration(), XmppConfiguration)
        self.assertEqual('ProgramY AIML2.0 Client', client.get_description())
        self.assertEqual('XMPPUSERNAME', client._username)
        self.assertEqual('XMPPPASSWORD', client._password)
        self.assertEqual("Server", client._server)
        self.assertEqual(8080, client._port)

        self.assertFalse(client._render_callback())
        self.assertIsInstance(client.renderer, TextRenderer)

    def test_connect(self):
        arguments = MockArgumentParser()
        client = MockXmppBotClient(arguments)
        self.assertIsNotNone(client)
        client._xmpp_client = MockXmppClient(client,  "username", "password")
        client.connect()
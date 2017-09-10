import unittest

from programy.clients.xmpp import XmppBotClient, XmppClient
from programy.config.sections.client.xmpp import XmppConfiguration

from programytest.clients.arguments import MockArgumentParser

class MockBot(object):

    def __init__(self):
        self.license_keys = {}
        self.answer = None

    def ask_question(self, userid, text):
        return self.answer

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
        XmppClient.__init__(self, bot_client, jid, password)
        self.registered = False
        self.server_url = None
        self.port_no = 0
        self.block = False

    def register_plugins(self, configuration):
        self.registered = True

    def run(self, server, port, block=True):
        self.server_url = server
        self.port_no = port
        self.block = block

class MockXmppBotClient(XmppBotClient):

    def __init__(self, argument_parser=None):
        XmppBotClient.__init__(self, argument_parser)
        self.mock_xmpp_client = None

    def create_client(self, username, password):
        self.mock_xmpp_client = MockXmppClient(self, username, password)
        return self.mock_xmpp_client

class XmppBotClientTests(unittest.TestCase):

    def test_xmpp_client_init(self):
        arguments = MockArgumentParser()
        client = XmppBotClient(arguments)
        self.assertIsNotNone(client)
        self.assertIsNotNone(client.get_client_configuration())
        self.assertIsInstance(client.get_client_configuration(), XmppConfiguration)

    def test_get_username_password(self):
        arguments = MockArgumentParser()
        client = XmppBotClient(arguments)
        self.assertIsNotNone(client)

        bot = MockBot()
        bot.license_keys = MockLicenseKeys({"XMPP_USERNAME": "Username", "XMPP_PASSWORD": "Password"})

        username, password = client.get_username_password(bot.license_keys)
        self.assertIsNotNone(username)
        self.assertEquals("Username", username)
        self.assertIsNotNone(password)
        self.assertEquals("Password", password)

    def test_get_server_port(self):
        arguments = MockArgumentParser()
        client = XmppBotClient(arguments)
        self.assertIsNotNone(client)

        client.configuration.client_configuration._server = "Server"
        client.configuration.client_configuration._port = 8080

        server, port = client.get_server_port(client.configuration)
        self.assertIsNotNone(server)
        self.assertEqual("Server", server)
        self.assertEqual(8080, port)

    def test_run(self):

        arguments = MockArgumentParser()
        client = MockXmppBotClient(arguments)
        self.assertIsNotNone(client)

        client.configuration.client_configuration._server = "Server"
        client.configuration.client_configuration._port = 8080

        client.bot = MockBot()
        client.bot.license_keys = MockLicenseKeys({"XMPP_USERNAME": "Username", "XMPP_PASSWORD": "Password"})

        client.run()

        self.assertTrue(client.mock_xmpp_client.registered)
        self.assertEqual("Server", client.mock_xmpp_client.server_url)
        self.assertEqual(8080, client.mock_xmpp_client.port_no)
        self.assertTrue(client.mock_xmpp_client.block)

import unittest

from programy.clients.xmpp import XmppBotClient, XmppClient
from programy.config.sections.client.xmpp import XmppConfiguration

from programytest.clients.arguments import MockArgumentParser

class MockBot(object):

    def __init__(self):
        self.license_keys = {}
        self.answer = None

    def ask_question(self, userid, text, responselogger=None):
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
        self.registered = False
        self.server_url = None
        self.port_no = 0
        self.block = False
        self.event_handlers = []
        self.registered_plugins = []
        self.response = None
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

class MockXmppBotClient(XmppBotClient):

    def __init__(self, argument_parser=None):
        XmppBotClient.__init__(self, argument_parser)
        self.mock_xmpp_client = None

    def create_client(self, username, password):
        self.mock_xmpp_client = MockXmppClient(self, username, password)
        return self.mock_xmpp_client


class XmppClientTests(unittest.TestCase):

    def test_xmpp_client_init(self):
        arguments = MockArgumentParser()
        bot_client = XmppBotClient(arguments)
        self.assertIsNotNone(bot_client)
        xmpp_client = MockXmppClient(bot_client, "userid", "password")
        self.assertIsNotNone(xmpp_client)
        self.assertEqual(bot_client, xmpp_client.bot_client)
        self.assertTrue(bool("session_start" in xmpp_client.event_handlers))
        self.assertTrue(bool("message" in xmpp_client.event_handlers))

    def test_is_valid_message(self):
        arguments = MockArgumentParser()
        bot_client = XmppBotClient(arguments)
        self.assertIsNotNone(bot_client)
        xmpp_client = MockXmppClient(bot_client, "userid", "password")

        self.assertTrue(xmpp_client.is_valid_message({"type": "chat"}))
        self.assertTrue(xmpp_client.is_valid_message({"type": "normal"}))

    def test_get_question(self):
        arguments = MockArgumentParser()
        bot_client = XmppBotClient(arguments)
        self.assertIsNotNone(bot_client)
        xmpp_client = MockXmppClient(bot_client, "userid", "password")

        self.assertEqual("this is text", xmpp_client.get_question({"body": "this is text"}))

    def test_get_userid(self):
        arguments = MockArgumentParser()
        bot_client = XmppBotClient(arguments)
        self.assertIsNotNone(bot_client)
        xmpp_client = MockXmppClient(bot_client, "userid", "password")

        self.assertEqual("user123", xmpp_client.get_userid({"from": "user123"}))

    def test_register_plugins(self):
        arguments = MockArgumentParser()
        bot_client = XmppBotClient(arguments)
        self.assertIsNotNone(bot_client)
        xmpp_client = MockXmppClient(bot_client, "userid", "password")

        bot_client.configuration.client_configuration._xep_0030 = True
        bot_client.configuration.client_configuration._xep_0004 = True
        bot_client.configuration.client_configuration._xep_0060 = True
        bot_client.configuration.client_configuration._xep_0199 = True

        xmpp_client.register_xep_plugins(bot_client.configuration)

        self.assertTrue(bool("xep_0030" in xmpp_client.registered_plugins))
        self.assertTrue(bool("xep_0004" in xmpp_client.registered_plugins))
        self.assertTrue(bool("xep_0060" in xmpp_client.registered_plugins))
        self.assertTrue(bool("xep_0199" in xmpp_client.registered_plugins))

    def test_message(self):
        arguments = MockArgumentParser()
        bot_client = XmppBotClient(arguments)
        self.assertIsNotNone(bot_client)
        xmpp_client = MockXmppClient(bot_client, "userid", "password")

        bot_client._bot = MockBot()
        bot_client.bot.answer = "Hiya"

        xmpp_client.message({"type": "chat", "from": "user123", "body": "Hello"})
        self.assertIsNotNone(xmpp_client.response)
        self.assertEqual("Hiya", xmpp_client.response)

class XmppBotClientTests(unittest.TestCase):

    def test_xmpp_bot_client_init(self):
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

        client._bot = MockBot()
        client.bot.license_keys = MockLicenseKeys({"XMPP_USERNAME": "Username", "XMPP_PASSWORD": "Password"})

        client.run()

        self.assertTrue(client.mock_xmpp_client.registered)
        self.assertEqual("Server", client.mock_xmpp_client.server_url)
        self.assertEqual(8080, client.mock_xmpp_client.port_no)
        self.assertTrue(client.mock_xmpp_client.block)

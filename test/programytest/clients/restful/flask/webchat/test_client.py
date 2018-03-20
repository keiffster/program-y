"""

import unittest
import unittest.mock

from programy.clients.restful.flask.webchat.client import WebChatBotClient
from programy.clients.restful.flask.webchat.config import WebChatConfiguration

from programytest.clients.arguments import MockArgumentParser


class MockWebChatBotClient(WebChatBotClient):

    def __init__(self):
        WebChatBotClient.__init__(self)


class WebChatBotClientTests(unittest.TestCase):

    def test_webchat_client_init(self):
        arguments = MockArgumentParser()
        client = MockWebChatBotClient(arguments)
        self.assertIsNotNone(client)

        self.assertIsInstance(client.get_client_configuration(), WebChatConfiguration)

"""
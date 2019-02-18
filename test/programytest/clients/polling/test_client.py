
import unittest.mock

from programy.clients.polling.client import PollingBotClient
from programy.clients.config import ClientConfigurationData

from programytest.clients.arguments import MockArgumentParser


class MockPollingBotClient(PollingBotClient):

    def __init__(self, id, argument_parser=None):
        PollingBotClient.__init__(self, id, argument_parser)
        self.slept = False

    def get_client_configuration(self):
        return ClientConfigurationData("polling")

    def sleep(self, time):
        self.slept = True


class MockRunningPollingBotClient(PollingBotClient):

    def __init__(self, id, argument_parser=None):
        PollingBotClient.__init__(self, id, argument_parser)
        self._connect = True
        self._poll = False

        self._connected = False
        self._messaged = False
        self._polled = False

    def get_client_configuration(self):
        return ClientConfigurationData("polling")

    def connect(self):
        self._connected = True
        return self._connect

    def display_connected_message(self):
        self._messaged = True

    def poll_and_answer(self):
        self._polled = True
        return self._poll


class PollingBotClientTests(unittest.TestCase):

    def test_init_raw(self):
        arguments = MockArgumentParser()
        with self.assertRaises(NotImplementedError):
            client = PollingBotClient("testpolling", arguments)

    def test_init_actual(self):
        arguments = MockArgumentParser()
        client = MockPollingBotClient("testpolling", arguments)
        self.assertIsNotNone(client)

        self.assertTrue(client.connect())

        with self.assertRaises(NotImplementedError):
            client.poll_and_answer()

        self.assertFalse(client.slept)
        client.sleep(100)
        self.assertTrue(client.slept)

    def test_running(self):
        arguments = MockArgumentParser()
        client = MockRunningPollingBotClient("testpolling", arguments)
        self.assertIsNotNone(client)

        client.run()

        self.assertTrue(client._connected)
        self.assertTrue(client._messaged)
        self.assertTrue(client._polled)
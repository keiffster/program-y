import unittest.mock

from programy.clients.events.client import EventBotClient
from programy.clients.config import ClientConfigurationData

from programytest.clients.arguments import MockArgumentParser


class MockEventBotClient(EventBotClient):

    def __init__(self, id, argument_parser=None):
        EventBotClient.__init__(self, id, argument_parser)

    def get_client_configuration(self):
        return ClientConfigurationData("events")

    def load_license_keys(self):
        pass


class MockRunningEventBotClient(EventBotClient):

    def __init__(self, id, argument_parser=None):
        EventBotClient.__init__(self, id, argument_parser)
        self.prior = False
        self.ran = False
        self.post = False

    def get_client_configuration(self):
        return ClientConfigurationData("events")

    def load_license_keys(self):
        pass

    def prior_to_run_loop(self):
        self.prior = True

    def wait_and_answer(self):
        self.ran = True

    def post_run_loop(self):
        self.post = True


class EventBotClientTests(unittest.TestCase):

    def test_init_raw(self):
        arguments = MockArgumentParser()
        with self.assertRaises(NotImplementedError):
            client = EventBotClient("testevents", arguments)

    def test_init_actual(self):
        arguments = MockArgumentParser()
        client = MockEventBotClient("testevents", arguments)
        self.assertIsNotNone(client)

        with self.assertRaises(NotImplementedError):
            client.wait_and_answer()

    def test_init_running(self):
        arguments = MockArgumentParser()
        client = MockRunningEventBotClient("testevents", arguments)
        self.assertIsNotNone(client)

        client.run()

        self.assertTrue(client.prior)
        self.assertTrue(client.ran)
        self.assertTrue(client.post)

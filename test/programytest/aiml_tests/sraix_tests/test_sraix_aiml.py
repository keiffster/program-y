import unittest
import unittest.mock
import os

from programy.context import ClientContext

from programytest.aiml_tests.client import TestClient
from programy.services.service import Service
from programy.config.brain.service import BrainServiceConfiguration
from programy.services.service import ServiceFactory


class SraixTestClient(TestClient):

    def __init__(self):
        TestClient.__init__(self)

    def load_configuration(self, arguments):
        super(SraixTestClient, self).load_configuration(arguments)
        self.configuration.client_configuration.configurations[0].configurations[0].files.aiml_files._files = [os.path.dirname(__file__)]


class MockGenericRESTService(Service):

    def __init__(self, config: BrainServiceConfiguration):
        Service.__init__(self, config)

    def ask_question(self, client_context, question: str):
        return "ANSWER"


class SraixAIMLTests(unittest.TestCase):

    def setUp(self):
        client = SraixTestClient()
        self._client_context = client.create_client_context("testid")

        config = unittest.mock.Mock()
        ServiceFactory.services['REST'] = MockGenericRESTService(config)

    def test_basic_sraix_test(self):
        response = self._client_context.bot.ask_question(self._client_context, "GENERIC REST TEST")
        self.assertIsNotNone(response)
        self.assertEqual(response, 'ANSWER')

    def test_unknown_sraix_test(self):
        response = self._client_context.bot.ask_question(self._client_context, "UNKNOWN REST TEST")
        self.assertIsNotNone(response)
        self.assertEqual(response, '')

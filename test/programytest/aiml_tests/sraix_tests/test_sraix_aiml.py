import os
import unittest
import unittest.mock

from programy.services.config import ServiceConfiguration
from programy.services.base import Service
from programytest.client import TestClient


class SraixTestClient(TestClient):

    def __init__(self):
        TestClient.__init__(self)

    def load_storage(self):
        super(SraixTestClient, self).load_storage()
        self.add_default_stores()
        self.add_categories_store([os.path.dirname(__file__)])


class MockGenericRESTService(Service):

    def __init__(self, config: ServiceConfiguration):
        Service.__init__(self, config)

    def ask_question(self, client_context, question: str):
        return "ANSWER"


class SraixAIMLTests(unittest.TestCase):

    def setUp(self):
        client = SraixTestClient()
        self._client_context = client.create_client_context("testid")

        config = ServiceConfiguration(service_type="library")
        self._client_context.brain.service_handler.add_service('REST',  MockGenericRESTService(config))

    def test_basic_sraix_test(self):
        response = self._client_context.bot.ask_question(self._client_context, "GENERIC REST TEST")
        self.assertIsNotNone(response)
        self.assertEqual(response, 'ANSWER.')

    def test_unknown_sraix_test(self):
        response = self._client_context.bot.ask_question(self._client_context, "UNKNOWN REST TEST")
        self.assertIsNotNone(response)
        self.assertEqual(response, '')

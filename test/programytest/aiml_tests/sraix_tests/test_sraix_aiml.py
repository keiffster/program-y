import unittest
import os

from programy.context import ClientContext

from programytest.aiml_tests.client import TestClient


class SraixTestClient(TestClient):

    def __init__(self):
        TestClient.__init__(self)

    def load_configuration(self, arguments):
        super(SraixTestClient, self).load_configuration(arguments)
        self.configuration.client_configuration.configurations[0].configurations[0].files.aiml_files._files = [os.path.dirname(__file__)]


class SraixAIMLTests(unittest.TestCase):

    def setUp(self):
        client = SraixTestClient()
        self._client_context = client.create_client_context("testid")

    #TODO Add tests here !!!

import unittest
import os
from test.aiml_tests.client import TestClient
from programy.config import BrainFileConfiguration

class SraixTestClient(TestClient):

    def __init__(self):
        TestClient.__init__(self)

    def load_configuration(self, arguments):
        super(SraixTestClient, self).load_configuration(arguments)
        self.configuration.brain_configuration._aiml_files = BrainFileConfiguration(os.path.dirname(__file__)+"/../aiml_tests/test_files/sraix", ".aiml", False)

class SraixAIMLTests(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        SraixAIMLTests.test_client = SraixTestClient()



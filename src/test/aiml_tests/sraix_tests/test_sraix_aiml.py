import unittest
import os
from test.aiml_tests.client import TestClient
from programy.config.sections.brain.file import BrainFileConfiguration

class SraixTestClient(TestClient):

    def __init__(self):
        TestClient.__init__(self)

    def load_configuration(self, arguments):
        super(SraixTestClient, self).load_configuration(arguments)
        self.configuration.brain_configuration.files.aiml_files._files = os.path.dirname(__file__)

class SraixAIMLTests(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        SraixAIMLTests.test_client = SraixTestClient()



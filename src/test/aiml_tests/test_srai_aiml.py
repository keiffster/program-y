import unittest
import os
from test.aiml_tests.client import TestClient
from programy.config import BrainFileConfiguration

class SraiTestClient(TestClient):

    def __init__(self):
        TestClient.__init__(self)

    def load_configuration(self, arguments):
        super(SraiTestClient, self).load_configuration(arguments)
        self.configuration.brain_configuration._aiml_files = BrainFileConfiguration(os.path.dirname(__file__)+"/../aiml_tests/test_files/srai", ".aiml", False)

class SraiAIMLTests(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        SraiAIMLTests.test_client = SraiTestClient()

    def test_srai_response(self):
        response = SraiAIMLTests.test_client.bot.ask_question("test", "HELLO")
        self.assertIsNotNone(response)
        self.assertEqual(response, 'HI THERE')

    def test_single_srai(self):
        response = SraiAIMLTests.test_client.bot.ask_question("test",  "HI")
        self.assertIsNotNone(response)
        self.assertEqual(response, 'HI THERE')

    def test_multiple_srai(self):
        response = SraiAIMLTests.test_client.bot.ask_question("test", "MORNING")
        self.assertIsNotNone(response)
        self.assertEqual(response, 'WELL HI THERE AND HI THERE AGAIN')

    def test_nested_srai(self):
        response = SraiAIMLTests.test_client.bot.ask_question("test", "FAREWELL")
        self.assertIsNotNone(response)
        self.assertEqual(response, 'SEEYA MATE')

    def test_predicate_set_srai(self):
        response = SraiAIMLTests.test_client.bot.ask_question("test", "TEST PREDICATE SET")
        self.assertIsNotNone(response)
        self.assertEqual('Global1 set to Value1 and Local1 set to  and Local2 set to Value3', response )

    def test_srai_with_star(self):
        response = SraiAIMLTests.test_client.bot.ask_question("test", "TEST MULTI SRAI KEITH STERLING")
        self.assertIsNotNone(response)
        self.assertEqual('TEST1 KEITH TEST1 TEST2 STERLING TEST2', response)

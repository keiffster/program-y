import unittest
import os
from test.aiml_tests.client import TestClient
from programy.config.brain import BrainFileConfiguration
import logging

class SraiTestClient(TestClient):

    def __init__(self):
        TestClient.__init__(self)

    def load_configuration(self, arguments):
        super(SraiTestClient, self).load_configuration(arguments)
        self.configuration.brain_configuration._aiml_files = BrainFileConfiguration(files=os.path.dirname(__file__))

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

    def test_srai_with_included_star(self):
        response = SraiAIMLTests.test_client.bot.ask_question("test", "TEST INCLUDED SRAI KEITH STERLING")
        self.assertIsNotNone(response)
        self.assertEqual('TEST1 KEITH TEST2 STERLING TEST2 TEST1', response)

    def test_xlength_xadd_0_1(self):
        response = SraiAIMLTests.test_client.bot.ask_question("test", "XADD 0 XS 1")
        self.assertIsNotNone(response)
        self.assertEqual('1', response)

    def test_xlength_xadd_1_1(self):
        response = SraiAIMLTests.test_client.bot.ask_question("test", "XADD 1 XS 1")
        self.assertIsNotNone(response)
        self.assertEqual('2', response)

    def test_length_no_string(self):
        response = SraiAIMLTests.test_client.bot.ask_question("test", "XLENGTH")
        self.assertIsNotNone(response)
        self.assertEqual('0', response)

    def test_xxlength_1char_string(self):
        SraiAIMLTests.test_client.dump_bot_brain_tree()
        response = SraiAIMLTests.test_client.bot.ask_question("test", "XXLENGTH X XS 0")
        self.assertIsNotNone(response)
        self.assertEqual('1', response)

    def test_xxlength_3char_string(self):
        response = SraiAIMLTests.test_client.bot.ask_question("test", "XXLENGTH X Y Z XS 0")
        self.assertIsNotNone(response)
        self.assertEqual('3', response)


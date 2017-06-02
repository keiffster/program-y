import unittest
import os
from test.aiml_tests.client import TestClient
from programy.config.brain import BrainFileConfiguration

class BasicTestClient(TestClient):

    def __init__(self):
        TestClient.__init__(self)

    def load_configuration(self, arguments):
        super(BasicTestClient, self).load_configuration(arguments)
        self.configuration.brain_configuration._aiml_files = BrainFileConfiguration(files=os.path.dirname(__file__))

class PriorityAIMLTests(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        PriorityAIMLTests.test_client = BasicTestClient()

    def test_priority_solo(self):
        response = PriorityAIMLTests.test_client.bot.ask_question("test",  "PRIORITY0")
        self.assertIsNotNone(response)
        self.assertEqual(response, 'PRIORITY0 TEST SUCCESS')

    def test_priority_first(self):
        response = PriorityAIMLTests.test_client.bot.ask_question("test",  "PRIORITY1 TEST")
        self.assertIsNotNone(response)
        self.assertEqual(response, 'PRIORITY1 TEST SUCCESS')

    def test_priority_first_multi(self):
        response = PriorityAIMLTests.test_client.bot.ask_question("test", "PRIORITY2 TEST1")
        self.assertIsNotNone(response)
        self.assertEqual(response, 'PRIORITY2 TEST1 SUCCESS')

        response = PriorityAIMLTests.test_client.bot.ask_question("test", "PRIORITY2 TEST2")
        self.assertIsNotNone(response)
        self.assertEqual(response, 'PRIORITY2 TEST2 SUCCESS')

    def test_priority_middle(self):
        response = PriorityAIMLTests.test_client.bot.ask_question("test", "THIS IS PRIORITY3 TEST")
        self.assertIsNotNone(response)
        self.assertEqual(response, 'PRIORITY3 TEST SUCCESS')

    def test_priority_middle_multi(self):
        response = PriorityAIMLTests.test_client.bot.ask_question("test", "THIS IS PRIORITY4 TEST1")
        self.assertIsNotNone(response)
        self.assertEqual(response, 'PRIORITY4 TEST1 SUCCESS')

        response = PriorityAIMLTests.test_client.bot.ask_question("test", "THIS IS PRIORITY4 TEST2")
        self.assertIsNotNone(response)
        self.assertEqual(response, 'PRIORITY4 TEST2 SUCCESS')

    def test_priority_last(self):
        response = PriorityAIMLTests.test_client.bot.ask_question("test", "THIS TEST IS PRIORITY5")
        self.assertIsNotNone(response)
        self.assertEqual(response, 'PRIORITY5 TEST SUCCESS')

    def test_priority_last_multi(self):
        response = PriorityAIMLTests.test_client.bot.ask_question("test", "THIS TEST1 IS PRIORITY6")
        self.assertIsNotNone(response)
        self.assertEqual(response, 'PRIORITY6 TEST1 SUCCESS')

        response = PriorityAIMLTests.test_client.bot.ask_question("test", "THIS TEST2 IS PRIORITY6")
        self.assertIsNotNone(response)
        self.assertEqual(response, 'PRIORITY6 TEST2 SUCCESS')
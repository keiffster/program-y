import unittest
import os
from programytest.aiml_tests.client import TestClient
from programy.config.sections.brain.file import BrainFileConfiguration

class TopicTestClient(TestClient):

    def __init__(self):
        TestClient.__init__(self)

    def load_configuration(self, arguments):
        super(TopicTestClient, self).load_configuration(arguments)
        self.configuration.brain_configuration.files.aiml_files._file = os.path.dirname(__file__) + os.sep + "yesno_test.aiml"
        self.configuration.brain_configuration.files.set_files._files = [os.path.dirname(__file__)]
        self.configuration.brain_configuration.files.set_files._extension = ".txt"

class YesNoAIMLTests(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        YesNoAIMLTests.test_client = TopicTestClient()

    def test_ask_yes_no(self):
        YesNoAIMLTests.test_client.bot.brain.dump_tree()

        response = YesNoAIMLTests.test_client.bot.ask_question("test", "yes")
        self.assertIsNotNone(response)
        self.assertEqual(response, 'Default Yes')

        response = YesNoAIMLTests.test_client.bot.ask_question("test", "no")
        self.assertIsNotNone(response)
        self.assertEqual(response, 'Default No')

        response = YesNoAIMLTests.test_client.bot.ask_question("test", "Hello")
        self.assertIsNotNone(response)
        self.assertEqual(response, 'Hi there, you good?')

        response = YesNoAIMLTests.test_client.bot.ask_question("test", "yes thanks")
        self.assertIsNotNone(response)
        self.assertEqual(response, 'Thats great')

        response = YesNoAIMLTests.test_client.bot.ask_question("test", "Hello")
        self.assertIsNotNone(response)
        self.assertEqual(response, 'Hi there, you good?')

        response = YesNoAIMLTests.test_client.bot.ask_question("test", "no not really")
        self.assertIsNotNone(response)
        self.assertEqual(response, 'Oh dear')

        response = YesNoAIMLTests.test_client.bot.ask_question("test", "yes")
        self.assertIsNotNone(response)
        self.assertEqual(response, 'Default Yes')

        response = YesNoAIMLTests.test_client.bot.ask_question("test", "no")
        self.assertIsNotNone(response)
        self.assertEqual(response, 'Default No')


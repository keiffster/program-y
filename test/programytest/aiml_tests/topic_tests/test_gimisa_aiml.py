import unittest
import os
from programytest.aiml_tests.client import TestClient
from programy.config.sections.brain.file import BrainFileConfiguration

class TopicTestClient(TestClient):

    def __init__(self):
        TestClient.__init__(self)

    def load_configuration(self, arguments):
        super(TopicTestClient, self).load_configuration(arguments)
        self.configuration.brain_configuration.files.aiml_files._file = os.path.dirname(__file__) + os.sep + "gimisa_test.aiml"
        self.configuration.brain_configuration.files.set_files._files = [os.path.dirname(__file__)]
        self.configuration.brain_configuration.files.set_files._extension = ".txt"

class GimisaAIMLTests(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        GimisaAIMLTests.test_client = TopicTestClient()

    def test_ask_blender_twice(self):

        response = GimisaAIMLTests.test_client.bot.ask_question("test", "render")
        self.assertIsNotNone(response)
        self.assertEqual(response, 'The definition of render is the first definition of render')

        response = GimisaAIMLTests.test_client.bot.ask_question("test", "render")
        self.assertIsNotNone(response)
        self.assertEqual(response, 'The definition of render is the second definition of render')

        response = GimisaAIMLTests.test_client.bot.ask_question("test", "render")
        self.assertIsNotNone(response)
        self.assertEqual(response, 'The definition of render is the second definition of render')



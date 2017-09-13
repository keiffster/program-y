import unittest
import os
from programytest.aiml_tests.client import TestClient
from programy.config.sections.brain.file import BrainFileConfiguration

class MultipleSentencesTestClient(TestClient):

    def __init__(self):
        TestClient.__init__(self)

    def load_configuration(self, arguments):
        super(MultipleSentencesTestClient, self).load_configuration(arguments)
        self.configuration.brain_configuration.files.aiml_files._files = [os.path.dirname(__file__)]

class MultipleSentencesAIMLTests(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        MultipleSentencesAIMLTests.test_client = MultipleSentencesTestClient()

    def test_multiple_questions(self):
        MultipleSentencesAIMLTests.test_client.bot.brain.dump_tree()
        response = MultipleSentencesAIMLTests.test_client.bot.ask_question("test", "TICKET SET 01453675. TICKET ANALYSE")
        self.assertIsNotNone(response)
        self.assertEqual("TICKET SET TO 01453675. ANALYSING TICKET", response)



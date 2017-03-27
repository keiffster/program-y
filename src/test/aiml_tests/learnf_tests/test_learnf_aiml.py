import unittest
import os
import os.path
from test.aiml_tests.client import TestClient
from programy.config.brain import BrainFileConfiguration

class LearnfTestClient(TestClient):

    def __init__(self):
        TestClient.__init__(self)

    def load_configuration(self, arguments):
        super(LearnfTestClient, self).load_configuration(arguments)
        self.configuration.brain_configuration._aiml_files = BrainFileConfiguration(os.path.dirname(__file__), ".aiml", False)

class LearnfAIMLTests(unittest.TestCase):

    def setUp(self):
        LearnfAIMLTests.test_client = LearnfTestClient()
        LearnfAIMLTests.test_client.bot.brain._configuration._aiml_files = BrainFileConfiguration("/tmp", ".aiml", False)
        self.learnf_path = "%s/learnf%s" % (LearnfAIMLTests.test_client.bot.brain._configuration._aiml_files.files, LearnfAIMLTests.test_client.bot.brain._configuration._aiml_files.extension)
        if os.path.exists(self.learnf_path):
            os.remove(self.learnf_path)

    def test_my_name_is_fred(self):
        self.assertFalse(os.path.exists(self.learnf_path))

        response = LearnfAIMLTests.test_client.bot.ask_question("test", "MY NAME IS FRED")
        self.assertIsNotNone(response)
        self.assertEqual(response, "OK, I will remember your name is FRED")
        self.check_file_contents()

        response = LearnfAIMLTests.test_client.bot.ask_question("test", "WHAT IS MY NAME")
        self.assertIsNotNone(response)
        self.assertEqual(response, "YOUR NAME IS FRED")

    def test_john_played_cricket(self):
        self.assertFalse(os.path.exists(self.learnf_path))

        response = LearnfAIMLTests.test_client.bot.ask_question("test", "JOHN PLAYED CRICKET")
        self.assertIsNotNone(response)
        self.assertEqual(response, "Ok. I will remember this")
        self.check_file_contents()

        response = LearnfAIMLTests.test_client.bot.ask_question("test", "WHAT DID JOHN PLAY")
        self.assertIsNotNone(response)
        self.assertEqual(response, "JOHN PLAYED CRICKET")

    def check_file_contents(self):
        self.assertTrue(os.path.exists(self.learnf_path))

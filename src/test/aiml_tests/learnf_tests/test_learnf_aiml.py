import unittest
import os
import os.path
import xml.etree.ElementTree as ET

from test.aiml_tests.client import TestClient

from programy.config.brain import BrainFileConfiguration

class LearnfTestClient(TestClient):

    def __init__(self):
        TestClient.__init__(self)

    def load_configuration(self, arguments):
        super(LearnfTestClient, self).load_configuration(arguments)
        self.configuration.brain_configuration._aiml_files = BrainFileConfiguration(files=os.path.dirname(__file__))

class LearnfAIMLTests(unittest.TestCase):

    def setUp(self):
        LearnfAIMLTests.test_client = LearnfTestClient()
        LearnfAIMLTests.test_client.bot.brain._configuration._aiml_files = BrainFileConfiguration(files="/tmp")
        self.learnf_path = "%s/learnf%s" % (LearnfAIMLTests.test_client.bot.brain._configuration._aiml_files.files, LearnfAIMLTests.test_client.bot.brain._configuration._aiml_files.extension)
        if os.path.exists(self.learnf_path):
            os.remove(self.learnf_path)

    def test_my_name_is_fred(self):
        self.assertFalse(os.path.exists(self.learnf_path))

        response = LearnfAIMLTests.test_client.bot.ask_question("test", "MY NAME IS FRED")
        self.assertIsNotNone(response)
        self.assertEqual(response, "OK, I will remember your name is FRED")
        self.check_file_contents("WHAT IS MY NAME", "*", "*", "YOUR NAME IS FRED")

        response = LearnfAIMLTests.test_client.bot.ask_question("test", "WHAT IS MY NAME")
        self.assertIsNotNone(response)
        self.assertEqual(response, "YOUR NAME IS FRED")

    def test_john_played_cricket(self):
        self.assertFalse(os.path.exists(self.learnf_path))

        response = LearnfAIMLTests.test_client.bot.ask_question("test", "JOHN PLAYED CRICKET")
        self.assertIsNotNone(response)
        self.assertEqual(response, "Ok. I will remember this")
        self.check_file_contents("WHAT DID JOHN PLAY", "*", "*", "JOHN PLAYED CRICKET")

        response = LearnfAIMLTests.test_client.bot.ask_question("test", "WHAT DID JOHN PLAY")
        self.assertIsNotNone(response)
        self.assertEqual(response, "JOHN PLAYED CRICKET")

    def check_file_contents(self, pattern, topic, that, template):
        self.assertTrue(os.path.exists(self.learnf_path))

        tree = ET.parse(self.learnf_path)
        aiml = tree.getroot()

        categories = aiml.findall('category')
        self.assertEquals(1, len(categories))

        patterns = categories[0].findall('pattern')
        self.assertEquals(1, len(patterns))
        self.assertEquals(patterns[0].text, pattern)

        topics = categories[0].findall('topic')
        self.assertEquals(1, len(topics))
        self.assertEquals(topics[0].text, topic)

        thats = categories[0].findall('that')
        self.assertEquals(1, len(thats))
        self.assertEquals(thats[0].text, that)

        templates = categories[0].findall('template')
        self.assertEquals(1, len(templates))
        self.assertEquals(templates[0].text, template)

import unittest
import os
import os.path
import xml.etree.ElementTree as ET
import shutil

from programytest.client import TestClient


class LearnfTestClient(TestClient):

    def __init__(self):
        self._learnf_path = os.path.dirname(__file__) + os.sep + 'learnf'
        TestClient.__init__(self)

    def load_storage(self):
        super(LearnfTestClient, self).load_storage()
        self.add_default_stores()
        self.add_categories_store([os.path.dirname(__file__)])
        self.add_learnf_store([self._learnf_path])

    def load_configuration(self, arguments):
        super(LearnfTestClient, self).load_configuration(arguments)
        self.configuration.client_configuration.configurations[0].configurations[0].overrides._allow_learn_aiml = True
        self.configuration.client_configuration.configurations[0].configurations[0].overrides._allow_learnf_aiml = True


class LearnfAIMLTests(unittest.TestCase):

    def setUp(self):
        client = LearnfTestClient()
        self._client_context = client.create_client_context("testid")

    def tearDown(self):
        shutil.rmtree(self._client_context.client._learnf_path)

    def test_my_name_is_fred(self):
        response = self._client_context.bot.ask_question(self._client_context, "MY NAME IS FRED")
        self.assertIsNotNone(response)
        self.assertEqual(response, "OK, I will remember your name is FRED.")
        self.check_file_contents("WHAT IS MY NAME", "*", "*", "YOUR NAME IS FRED")

        response = self._client_context.bot.ask_question(self._client_context, "WHAT IS MY NAME")
        self.assertIsNotNone(response)
        self.assertEqual(response, "YOUR NAME IS FRED.")

    def test_multiple_my_name_is_fred_asks(self):
        response = self._client_context.bot.ask_question(self._client_context, "MY NAME IS FRED")
        self.assertIsNotNone(response)
        self.assertEqual(response, "OK, I will remember your name is FRED.")

        response = self._client_context.bot.ask_question(self._client_context, "MY NAME IS FRED")
        self.assertIsNotNone(response)
        self.assertEqual(response, "OK, I will remember your name is FRED.")

        self.check_file_contents("WHAT IS MY NAME", "*", "*", "YOUR NAME IS FRED")

    def test_john_played_cricket(self):
        response = self._client_context.bot.ask_question(self._client_context, "JOHN PLAYED CRICKET")
        self.assertIsNotNone(response)
        self.assertEqual(response, "Ok. I will remember this.")

        self.check_file_contents("WHAT DID JOHN PLAY", "*", "*", "JOHN PLAYED CRICKET")

        response = self._client_context.bot.ask_question(self._client_context, "WHAT DID JOHN PLAY")
        self.assertIsNotNone(response)
        self.assertEqual(response, "JOHN PLAYED CRICKET.")

    def check_file_contents(self, pattern, topic, that, template):
        learnf_file = self._client_context.client._learnf_path + os.sep + "testid.aiml"

        self.assertTrue(os.path.exists(learnf_file))

        tree = ET.parse(learnf_file)
        aiml = tree.getroot()

        categories = aiml.findall('category')
        self.assertEqual(1, len(categories))

        patterns = categories[0].findall('pattern')
        self.assertEqual(1, len(patterns))
        self.assertEqual(patterns[0].text, pattern)

        topics = categories[0].findall('topic')
        self.assertEqual(1, len(topics))
        self.assertEqual(topics[0].text, topic)

        thats = categories[0].findall('that')
        self.assertEqual(1, len(thats))
        self.assertEqual(thats[0].text, that)

        templates = categories[0].findall('template')
        self.assertEqual(1, len(templates))
        self.assertEqual(templates[0].text, template)

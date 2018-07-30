import unittest
import os
import os.path
import xml.etree.ElementTree as ET

from programytest.client import TestClient


class LearnfTestClient(TestClient):

    def __init__(self):
        TestClient.__init__(self)

    def load_storage(self):
        super(LearnfTestClient, self).load_storage()
        self.add_default_stores()
        self.add_categories_store([os.path.dirname(__file__)])

    def load_configuration(self, arguments):
        super(LearnfTestClient, self).load_configuration(arguments)
        self.configuration.client_configuration.configurations[0].configurations[0].overrides._allow_learn_aiml = True
        self.configuration.client_configuration.configurations[0].configurations[0].overrides._allow_learnf_aiml = True


class LearnfAIMLTests(unittest.TestCase):

    def setUp(self):
        client = LearnfTestClient()
        self._client_context = client.create_client_context("testid")

        self.tearDown()

    def test_my_name_is_fred(self):
        response = self._client_context.bot.ask_question(self._client_context, "MY NAME IS FRED")
        self.assertIsNotNone(response)
        self.assertEqual(response, "OK, I will remember your name is FRED")
        #self.check_file_contents("WHAT IS MY NAME", "*", "*", "YOUR NAME IS FRED")

        response = self._client_context.bot.ask_question(self._client_context, "WHAT IS MY NAME")
        self.assertIsNotNone(response)
        self.assertEqual(response, "YOUR NAME IS FRED")

    def test_john_played_cricket(self):
        response = self._client_context.bot.ask_question(self._client_context, "JOHN PLAYED CRICKET")
        self.assertIsNotNone(response)
        self.assertEqual(response, "Ok. I will remember this")
        #self.check_file_contents("WHAT DID JOHN PLAY", "*", "*", "JOHN PLAYED CRICKET")

        response = self._client_context.bot.ask_question(self._client_context, "WHAT DID JOHN PLAY")
        self.assertIsNotNone(response)
        self.assertEqual(response, "JOHN PLAYED CRICKET")

    def check_file_contents(self, pattern, topic, that, template):
        self.assertTrue(os.path.exists(self.learnf_file))

        tree = ET.parse(self.learnf_file)
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

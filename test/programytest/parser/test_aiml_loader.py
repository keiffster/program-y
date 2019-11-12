import unittest
import os
from programy.parser.aiml_parser import AIMLLoader
from programy.dialog.sentence import Sentence
from programytest.client import TestClient


class AIMLLoaderTestClient(TestClient):

    def __init__(self):
        TestClient.__init__(self)

    def load_storage(self):
        super(AIMLLoaderTestClient, self).load_storage()
        self.add_default_stores()


class AIMLLoaderTests(unittest.TestCase):

    def setUp(self):
        self._client = AIMLLoaderTestClient()
        self._client_context = self._client.create_client_context("testid")

    def test_init(self):
        loader = AIMLLoader(self._client_context.brain.aiml_parser)
        self.assertIsNotNone(loader)
        self.assertEquals(self._client_context.brain.aiml_parser, loader.parser)

    def test_load_file_contents(self):
        loader = AIMLLoader(self._client_context.brain.aiml_parser)
        filename = os.path.dirname(__file__) + os.sep + "./valid.aiml"
        loader.load_file_contents("TEST", filename)

        context = self._client_context.brain.aiml_parser.match_sentence(self._client_context, Sentence(self._client_context, "HELLO"), "*", "*")
        self.assertIsNotNone(context)
        self.assertTrue(context.matched())

    def test_load_file_contents_invalid_filename(self):
        loader = AIMLLoader(self._client_context.brain.aiml_parser)
        filename = "XXXX.aiml"
        loader.load_file_contents("TEST", filename)

        context = self._client_context.brain.aiml_parser.match_sentence(self._client_context, Sentence(self._client_context, "HELLO"), "*", "*")
        self.assertIsNone(context)

import unittest
from programy.processors.pre.lemmatize import LemmatizePreProcessor

from programytest.client import TestClient


class LemmatizerTests(unittest.TestCase):

    def setUp(self):
        self.client = TestClient()

    def test_to_lemmatizer(self):
        processor = LemmatizePreProcessor()

        context = self.client.create_client_context("testid")

        result = processor.process(context, "My octopi are chasing my mice")
        self.assertIsNotNone(result)
        self.assertEqual("my octopus are chasing my mouse", result)

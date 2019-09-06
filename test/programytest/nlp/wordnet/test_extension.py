import unittest

from programy.nlp.wordnet.extension import WordNetExtension

from programytest.client import TestClient


class WordNetExtensionTests(unittest.TestCase):

    def setUp(self):
        client = TestClient()
        self.context = client.create_client_context("testid")

    def test_get_definition(self):
        extension = WordNetExtension()
        self.assertIsNotNone(extension)
        self.assertEquals("feline mammal usually having thick soft fur and no ability to roar: domestic cats; wildcats", extension.execute(self.context, "CAT"))

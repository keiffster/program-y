import unittest

from programy.nlp.synsets.extension import SynsetsExtension

from programytest.client import TestClient


class SynsetsExtensionTests(unittest.TestCase):

    def setUp(self):
        client = TestClient()
        self.context = client.create_client_context("testid")

    def test_is_similar_default_weight(self):
        extension = SynsetsExtension()
        self.assertIsNotNone(extension)
        self.assertEquals("TRUE", extension.execute(self.context, "SIMILAR OCTOPUS SHRIMP"))

    def test_is_similar_low_weight(self):
        extension = SynsetsExtension()
        self.assertIsNotNone(extension)
        self.assertEquals("TRUE", extension.execute(self.context, "SIMILAR OCTOPUS SHRIMP 0 DOT 1"))

    def test_is_similar_height_weight(self):
        extension = SynsetsExtension()
        self.assertIsNotNone(extension)
        self.assertEquals("FALSE", extension.execute(self.context, "SIMILAR OCTOPUS SHRIMP 0 DOT 9"))

    def test_is_similars_words(self):
        extension = SynsetsExtension()
        self.assertIsNotNone(extension)
        self.assertEquals("TRUE HACK MACHINE_POLITICIAN CAB CHOP", extension.execute(self.context, "SIMILARS WORDS HACK"))

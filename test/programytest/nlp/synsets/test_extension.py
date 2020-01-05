import unittest

from programy.nlp.synsets.extension import SynsetsExtension
from programytest.client import TestClient


class MockSynsetsExtension(SynsetsExtension):

    def __init__(self):
        SynsetsExtension.__init__(self)

    def _get_similarities(self, word1, word2, weight):
        raise Exception("Mock exception")


class SynsetsExtensionTests(unittest.TestCase):

    def setUp(self):
        client = TestClient()
        self.context = client.create_client_context("testid")

    def test_similar_bad_grammar(self):
        extension = SynsetsExtension()
        self.assertIsNotNone(extension)

        self.assertEqual("FALSE", extension.execute(self.context, "SIMILAR"))
        self.assertEqual("FALSE", extension.execute(self.context, "SIMILAR WORD1"))
        self.assertEqual("FALSE", extension.execute(self.context, "SIMILAR WORD1 WORD2 WORD3"))
        self.assertEqual("FALSE", extension.execute(self.context, "SIMILAR OCTOPUS SHRIMP 0 DOT 9 WORD7"))
        self.assertEqual("FALSE", extension.execute(self.context, "SIMILARS OTHER GENTLY"))
        self.assertEqual("FALSE", extension.execute(self.context, "OTHER OTHER GENTLY"))

    def test_is_similar_default_weight(self):
        extension = SynsetsExtension()
        self.assertIsNotNone(extension)
        self.assertEqual("TRUE", extension.execute(self.context, "SIMILAR OCTOPUS SHRIMP"))

    def test_is_similar_low_weight(self):
        extension = SynsetsExtension()
        self.assertIsNotNone(extension)
        self.assertEqual("TRUE", extension.execute(self.context, "SIMILAR OCTOPUS SHRIMP 0 DOT 1"))

    def test_is_similar_height_weight(self):
        extension = SynsetsExtension()
        self.assertIsNotNone(extension)
        self.assertEqual("FALSE", extension.execute(self.context, "SIMILAR OCTOPUS SHRIMP 0 DOT 9"))

    def test_is_similar_exception(self):
        extension = MockSynsetsExtension()
        self.assertIsNotNone(extension)
        self.assertEqual("FALSE", extension.execute(self.context, "SIMILAR WORD1 WORD2"))

    def test_similars_bad_grammar(self):
        extension = SynsetsExtension()
        self.assertIsNotNone(extension)

        self.assertEqual("FALSE", extension.execute(self.context, "SIMILARS WORDS HACK WORD4"))
        self.assertEqual("FALSE", extension.execute(self.context, "SIMILARS OTHER HACK WORD4"))

    def test_is_similars_words(self):
        extension = SynsetsExtension()
        self.assertIsNotNone(extension)
        self.assertEqual("TRUE HACK MACHINE_POLITICIAN CAB CHOP", extension.execute(self.context, "SIMILARS WORDS HACK"))

    def test_is_similars_verbs(self):
        extension = SynsetsExtension()
        self.assertIsNotNone(extension)
        self.assertEqual("TRUE RUN SCAT OPERATE FUNCTION RANGE CAMPAIGN PLAY TEND PREVAIL CARRY GUIDE PLY HUNT RACE MOVE MELT LADDER", extension.execute(self.context, "SIMILARS VERBS RUNNING"))

    def test_is_similars_nouns(self):
        extension = SynsetsExtension()
        self.assertIsNotNone(extension)
        self.assertEqual("TRUE CAR CABLE_CAR", extension.execute(self.context, "SIMILARS NOUNS CAR"))

    def test_is_similars_adjectives(self):
        extension = SynsetsExtension()
        self.assertIsNotNone(extension)
        self.assertEqual("TRUE LARGE BOMBASTIC BIG", extension.execute(self.context, "SIMILARS ADJECTIVES LARGE"))

    def test_is_similars_adverbs(self):
        extension = SynsetsExtension()
        self.assertIsNotNone(extension)
        self.assertEqual("TRUE GENTLY LIGHTLY", extension.execute(self.context, "SIMILARS ADVERBS GENTLY"))


import unittest

from programy.processors.pre.wordtagger import WordTaggerPreProcessor
from programytest.client import TestClient


class MockClientContext(object):

    def __init__(self, bot):
        self.bot = bot


class MockWordTaggerPreProcessor(WordTaggerPreProcessor):

    def __init__(self):
        WordTaggerPreProcessor.__init__(self)

    def _word_tag(self, context, word_string):
        raise Exception("Mock Exception")


class TranslatorPreProcessorTest(unittest.TestCase):

    def setUp(self):
        self.client = TestClient()

    def test_pre_process_word_tagger_sentence(self):
        processor = WordTaggerPreProcessor()

        context = self.client.create_client_context("testid")

        string = processor.process(context, "Python is a high-level, general-purpose programming language.")
        self.assertIsNotNone(string)
        self.assertEqual("Python NNP is VBZ a DT high-level JJ general-purpose JJ programming NN language NN", string)

    def test_pre_process_word_tagger_word(self):
        processor = WordTaggerPreProcessor()

        context = self.client.create_client_context("testid")

        string = processor.process(context, "Python")
        self.assertIsNotNone(string)
        self.assertEqual("Python NN", string)

    def test_pre_process_word_tagger_exception(self):
        processor = MockWordTaggerPreProcessor()

        context = self.client.create_client_context("testid")

        self.assertEqual("Python", processor.process(context, "Python"))

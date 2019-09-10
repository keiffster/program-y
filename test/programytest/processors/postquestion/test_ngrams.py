import unittest
from programy.processors.postquestion.ngrams import NGramsPostQuestionProcessor

from programytest.client import TestClient


class MockBrain(object):

    def __init__(self, question, response, client_context):
        self._question = question
        self._response = response
        self._client_context = client_context
        self.tokenizer = None
        self.id = "testid"

    def ask_question(self, clientid, sentence, srai=False):
        question = sentence.text(self._client_context)
        if question == self._question:
            return self._response
        else:
            return None


class NGramsTests(unittest.TestCase):

    def test_ngrams_success(self):
        client = TestClient()
        client_context = client.create_client_context("user1")
        tokenizer = client_context.brain.tokenizer
        client_context._brain = MockBrain("is hugo rifkind", "NGramms Are Go", client_context)
        client_context._brain.tokenizer = tokenizer

        processor = NGramsPostQuestionProcessor()

        result = processor.process(client_context, "Where in the world is hugo rifkind")
        self.assertIsNotNone(result)
        self.assertEqual("NGramms Are Go", result)

    def test_ngrams_failure(self):
        client = TestClient()
        client_context = client.create_client_context("user1")
        tokenizer = client_context.brain.tokenizer
        client_context._brain = MockBrain("Something else", "NGramms Are Go", client_context)
        client_context._brain.tokenizer = tokenizer

        processor = NGramsPostQuestionProcessor()

        result = processor.process(client_context, "Where in the world is hugo rifkind")
        self.assertIsNone(result)

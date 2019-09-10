import unittest
from programy.processors.postquestion.stopwords import StopWordsPostQuestionProcessor

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


class StopWordsTests(unittest.TestCase):

    def test_stopwords_success(self):
        client = TestClient()
        client_context = client.create_client_context("user1")
        tokenizer = client_context.brain.tokenizer
        client_context._brain = MockBrain("This cat", "Stopwords are working", client_context)
        client_context._brain.tokenizer = tokenizer

        processor = StopWordsPostQuestionProcessor()

        result = processor.process(client_context, "This is a cat")
        self.assertIsNotNone(result)
        self.assertEqual("Stopwords are working", result)

    def test_stopwords_failure(self):
        client = TestClient()
        client_context = client.create_client_context("user1")
        tokenizer = client_context.brain.tokenizer
        client_context._brain = MockBrain("Something else", "Stopwords are working", client_context)
        client_context._brain.tokenizer = tokenizer

        processor = StopWordsPostQuestionProcessor()

        result = processor.process(client_context, "This is a cat")
        self.assertIsNone(result)

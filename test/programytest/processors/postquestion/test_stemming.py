import unittest
from programy.processors.postquestion.stemming import StemmingPostQuestionProcessor

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


class StemmingTests(unittest.TestCase):

    def test_stemming_success(self):
        client = TestClient()
        client_context = client.create_client_context("user1")
        tokenizer = client_context.brain.tokenizer
        client_context._brain = MockBrain("My troubl with cat", "Stemming is working", client_context)
        client_context._brain.tokenizer = tokenizer

        processor = StemmingPostQuestionProcessor()

        result = processor.process(client_context, "My troubles with cats")
        self.assertIsNotNone(result)
        self.assertEqual("Stemming is working", result)

    def test_stemming_failure(self):
        client = TestClient()
        client_context = client.create_client_context("user1")
        tokenizer = client_context.brain.tokenizer
        client_context._brain = MockBrain("Something else", "Stemming is working", client_context)
        client_context._brain.tokenizer = tokenizer

        processor = StemmingPostQuestionProcessor()

        result = processor.process(client_context, "My troubles with cats")
        self.assertIsNone(result)

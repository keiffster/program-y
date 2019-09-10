import unittest
from programy.processors.postquestion.lemmatize import LemmatizePostQuestionProcessor

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


class LemmatizerTests(unittest.TestCase):

    def test_lemmatizer_success(self):
        client = TestClient()
        client_context = client.create_client_context("user1")
        tokenizer = client_context.brain.tokenizer
        client_context._brain = MockBrain("my octopus are chasing my mouse", "Lemmatize working", client_context)
        client_context._brain.tokenizer = tokenizer

        processor = LemmatizePostQuestionProcessor()

        result = processor.process(client_context, "My octopi are chasing my mice")
        self.assertIsNotNone(result)
        self.assertEqual("Lemmatize working", result)

    def test_lemmatizer_failure(self):
        client = TestClient()
        client_context = client.create_client_context("user1")
        tokenizer = client_context.brain.tokenizer
        client_context._brain = MockBrain("Something else", "Lemmatize working", client_context)
        client_context._brain.tokenizer = tokenizer

        processor = LemmatizePostQuestionProcessor()

        result = processor.process(client_context, "My octopi are chasing my mice")
        self.assertIsNone(result)

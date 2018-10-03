import unittest
import os

from programytest.client import TestClient


class MultipleSentencesTestClient(TestClient):

    def __init__(self):
        TestClient.__init__(self)

    def load_storage(self):
        super(MultipleSentencesTestClient, self).load_storage()
        self.add_default_stores()
        self.add_categories_store([os.path.dirname(__file__)])


class MultipleSentencesAIMLTests(unittest.TestCase):

    def setUp(self):
        client = MultipleSentencesTestClient()
        self._client_context = client.create_client_context("testid")

    def test_multiple_questions(self):
        response = self._client_context.bot.ask_question(self._client_context, "TICKET SET 01453675. TICKET ANALYSE")
        self.assertIsNotNone(response)
        self.assertEqual("TICKET SET TO 01453675. ANALYSING TICKET.", response)



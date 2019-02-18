import unittest
import os

from programytest.client import TestClient


class SurveyTestsClient(TestClient):

    def __init__(self):
        TestClient.__init__(self, debug=True)

    def load_storage(self):
        super(SurveyTestsClient, self).load_storage()
        self.add_default_stores()
        self.add_categories_store([os.path.dirname(__file__)])


class SurveyAIMLTests(unittest.TestCase):

    def setUp (self):
        client = SurveyTestsClient()
        self._client_context = client.create_client_context("testid")

    def test_survey(self):
        # Question 1
        response = self._client_context.bot.ask_question(self._client_context, "START SURVEY")
        self.assertIsNotNone(response)
        self.assertEqual(response, 'Question 1. What do you like about AIML?')

        response = self._client_context.bot.ask_question(self._client_context, "Its really cool")
        self.assertIsNotNone(response)
        self.assertEqual(response, 'Thanks, now Question 2. What do you dislike about AIML?')

        response = self._client_context.bot.ask_question(self._client_context, "Too many undocmented features by the creators")
        self.assertIsNotNone(response)
        self.assertEqual(response, 'Thanks, thats the end of the survey.')

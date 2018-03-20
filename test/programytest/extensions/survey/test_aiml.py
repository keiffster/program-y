import unittest
import os

from programy.context import ClientContext

from programytest.aiml_tests.client import TestClient


class SurveyTestsClient(TestClient):

    def __init__(self):
        TestClient.__init__(self, debug=True)

    def load_configuration(self, arguments):
        super(SurveyTestsClient, self).load_configuration(arguments)
        self.configuration.client_configuration.configurations[0].configurations[0].files.aiml_files._files=[os.path.dirname(__file__)]


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
        self.assertEqual(response, 'Thanks, thats the end of the survey')

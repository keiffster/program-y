import unittest
import os
from test.aiml_tests.client import TestClient
from programy.config.sections.brain.file import BrainFileConfiguration


class SurveyTestsClient(TestClient):

    def __init__(self):
        TestClient.__init__(self, debug=True)

    def load_configuration(self, arguments):
        super(SurveyTestsClient, self).load_configuration(arguments)
        self.configuration.brain_configuration.files.aiml_files._files = files=os.path.dirname(__file__)

class SurveyAIMLTests(unittest.TestCase):

    def setUp (self):
        SurveyAIMLTests.test_client = SurveyTestsClient()

    def test_survey(self):
        # Question 1
        response = SurveyAIMLTests.test_client.bot.ask_question("testif", "START SURVEY")
        self.assertIsNotNone(response)
        self.assertEqual(response, 'Question 1. What do you like about AIML?')

        response = SurveyAIMLTests.test_client.bot.ask_question("testif", "Its really cool")
        self.assertIsNotNone(response)
        self.assertEqual(response, 'Thanks, now Question 2. What do you dislike about AIML?')

        response = SurveyAIMLTests.test_client.bot.ask_question("testif", "Too many undocmented features by the creators")
        self.assertIsNotNone(response)
        self.assertEqual(response, 'Thanks, thats the end of the survey')

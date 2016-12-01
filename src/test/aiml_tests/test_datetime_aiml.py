import unittest
import os
from test.aiml_tests.client import TestClient
from programy.config import BrainFileConfiguration

class BasicTestClient(TestClient):

    def __init__(self):
        TestClient.__init__(self)

    def load_configuration(self, arguments):
        super(BasicTestClient, self).load_configuration(arguments)
        self.configuration.brain_configuration._aiml_files = BrainFileConfiguration(os.path.dirname(__file__)+"/../aiml_tests/test_files/datetime", ".aiml", False)

class DateTimeAIMLTests(unittest.TestCase):

    DEFAULT_DATETIME_REGEX = "^.*.{3}\s*.{3}\s*\d{1,}\s\d{2}:\d{2}:\d{2}\s\d{4}"

    @classmethod
    def setUpClass(cls):
        DateTimeAIMLTests.test_client = BasicTestClient()

    def test_date(self):
        response = DateTimeAIMLTests.test_client.bot.ask_question("test",  "TEST DATE")
        self.assertIsNotNone(response)
        self.assertRegex(response, DateTimeAIMLTests.DEFAULT_DATETIME_REGEX)

    def test_interval(self):
        response = DateTimeAIMLTests.test_client.bot.ask_question("test", "TEST INTERVAL")
        self.assertIsNotNone(response)
        self.assertEqual(response, "2")

    def test_season(self):
        response = DateTimeAIMLTests.test_client.bot.ask_question("test", "SEASON")
        self.assertIsNotNone(response)
        self.assertEqual(response, "Winter")

    def test_age(self):

        DateTimeAIMLTests.test_client.bot.brain.properties.add_property('birthdate', "September 9, 2016")

        response = DateTimeAIMLTests.test_client.bot.ask_question("test", "AGE")
        self.assertIsNotNone(response)
        self.assertEqual(response, "I am 2 months old.")

    def test_age_in_years(self):

        DateTimeAIMLTests.test_client.bot.brain.properties.add_property('birthdate', "September 9, 2016")

        response = DateTimeAIMLTests.test_client.bot.ask_question("test", "AGE IN YEARS")
        self.assertIsNotNone(response)
        self.assertEqual(response, "0")

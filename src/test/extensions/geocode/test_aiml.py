import unittest
import os
from test.aiml_tests.client import TestClient
from programy.config.brain import BrainFileConfiguration


class GeoCodeTestsClient(TestClient):

    def __init__(self):
        TestClient.__init__(self, debug=True)

    def load_configuration(self, arguments):
        super(GeoCodeTestsClient, self).load_configuration(arguments)
        self.configuration.brain_configuration._aiml_files = BrainFileConfiguration(os.path.dirname(__file__)+"/../../../../aiml/extensions/geocode", ".aiml", False)

class GeoCodeAIMLTests(unittest.TestCase):

    def setUp (self):
        GeoCodeAIMLTests.test_client = GeoCodeTestsClient()

    def test_postcode1(self):
        response = GeoCodeAIMLTests.test_client.bot.ask_question("testif", "POSTCODE KY39UR")
        self.assertIsNotNone(response)
        self.assertEqual(response, 'LATITUDE DEC 56 FRAC 0720397 LONGITUDE DEC -3 FRAC 1752001')

    def test_postcode2(self):
        response = GeoCodeAIMLTests.test_client.bot.ask_question("testif", "POSTCODE KY3 9UR")
        self.assertIsNotNone(response)
        self.assertEqual(response, 'LATITUDE DEC 56 FRAC 0720397 LONGITUDE DEC -3 FRAC 1752001')

    def test_location(self):
        response = GeoCodeAIMLTests.test_client.bot.ask_question("testif", "LOCATION KINGHORN")
        self.assertIsNotNone(response)
        self.assertEqual(response, 'LATITUDE DEC 56 FRAC 071231 LONGITUDE DEC -3 FRAC 174329')

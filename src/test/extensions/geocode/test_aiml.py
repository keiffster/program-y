import unittest
import os
from test.aiml_tests.client import TestClient
from programy.config.sections.brain.file import BrainFileConfiguration


class GeoCodeTestsClient(TestClient):

    def __init__(self):
        TestClient.__init__(self, debug=True)

    def load_configuration(self, arguments):
        super(GeoCodeTestsClient, self).load_configuration(arguments)
        self.configuration.brain_configuration.files.aiml_files._files = files=os.path.dirname(__file__)

class GeoCodeAIMLTests(unittest.TestCase):

    def setUp (self):
        GeoCodeAIMLTests.test_client = GeoCodeTestsClient()

        latlong     = os.path.dirname(__file__) +  os.sep + "google_latlong.json"

        GeoCodeAIMLTests.test_client.bot.license_keys.load_license_key_data("""
        GOOGLE_LATLONG = %s
        """%(latlong))

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
        self.assertEqual(response, 'LATITUDE DEC 56 FRAC 0720397 LONGITUDE DEC -3 FRAC 1752001')

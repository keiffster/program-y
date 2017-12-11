import unittest
import os
from programytest.aiml_tests.client import TestClient

class BasicTestClient(TestClient):

    def __init__(self):
        TestClient.__init__(self)

    def load_configuration(self, arguments):
        super(BasicTestClient, self).load_configuration(arguments)
        self.configuration.brain_configuration.files.aiml_files._files = [os.path.dirname(__file__)]

class UnicodeAIMLTests(unittest.TestCase):

    def setUp(cls):
        UnicodeAIMLTests.test_client = BasicTestClient()

    def test_cantonese_unicode(self):
        response = UnicodeAIMLTests.test_client.bot.ask_question('test',  u'喂')
        self.assertIsNotNone(response)
        self.assertEqual(response, u'你好')

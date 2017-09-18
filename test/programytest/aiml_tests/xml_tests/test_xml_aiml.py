import unittest
import os

from programytest.aiml_tests.client import TestClient

class XMLTestClient(TestClient):

    def __init__(self):
        TestClient.__init__(self)

    def load_configuration(self, arguments):
        super(XMLTestClient, self).load_configuration(arguments)
        self.configuration.brain_configuration.files.aiml_files._files = [os.path.dirname(__file__)]

class XMLAIMLTests(unittest.TestCase):

    def setUp(self):
        XMLAIMLTests.test_client = XMLTestClient()

    def test_basic_xml(self):
        response = XMLAIMLTests.test_client.bot.ask_question("test",  "HELLO")
        self.assertEqual(response, "I said <b>how are you</b> ?")

    def test_html_link(self):
        response = XMLAIMLTests.test_client.bot.ask_question("test",  "PICTURE")
        self.assertEqual(response, 'You can see my picture at <a href="http://someurl/image.png">Here</a>')

    def test_html_link_with_star(self):
        response = XMLAIMLTests.test_client.bot.ask_question("test",  "GOOGLE AIML")
        self.assertEqual(response, '<a target="_new" href="http://www.google.com/search?q=AIML">Google Search</a>')

    def test_html_br(self):
        response = XMLAIMLTests.test_client.bot.ask_question("test",  "TEST1")
        self.assertEqual(response, 'Line1\n\t\t\tLine2')

        response = XMLAIMLTests.test_client.bot.ask_question("test",  "TEST2")
        self.assertEqual(response, 'Line1 <br></br> Line2')

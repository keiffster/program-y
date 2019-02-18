import unittest
import os

from programytest.client import TestClient


class XMLTestClient(TestClient):

    def __init__(self):
        TestClient.__init__(self)

    def load_storage(self):
        super(XMLTestClient, self).load_storage()
        self.add_default_stores()
        self.add_categories_store([os.path.dirname(__file__)])


class XMLAIMLTests(unittest.TestCase):

    def setUp(self):
        client = XMLTestClient()
        self._client_context = client.create_client_context("testid")

    def test_basic_xml(self):
        response = self._client_context.bot.ask_question(self._client_context,  "HELLO")
        self.assertEqual(response, "I said <b>how are you</b> ?")

    def test_html_link(self):
        response = self._client_context.bot.ask_question(self._client_context,  "PICTURE")
        self.assertEqual(response, 'You can see my picture at <a href="http://someurl/image.png">Here</a>.')

    def test_html_link_with_star(self):
        response = self._client_context.bot.ask_question(self._client_context,  "GOOGLE AIML")
        self.assertEqual(response, '<a target="_new" href="http://www.google.com/search?q=AIML">Google Search</a>.')

    def test_html_br(self):
        response = self._client_context.bot.ask_question(self._client_context,  "TEST1")
        self.assertEqual(response, 'Line1\n\t\t\tLine2.')

        response = self._client_context.bot.ask_question(self._client_context,  "TEST2")
        self.assertEqual(response, 'Line1 <br></br> Line2.')

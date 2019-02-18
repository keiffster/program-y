import unittest
import os

from programytest.client import TestClient


class UtuxmtTestClient(TestClient):

    def __init__(self):
        TestClient.__init__(self)

    def load_storage(self):
        super(UtuxmtTestClient, self).load_storage()
        self.add_default_stores()
        self.add_categories_store([os.path.dirname(__file__)])


class XMLAIMLTests(unittest.TestCase):

    def setUp(self):
        client = UtuxmtTestClient()
        self._client_context = client.create_client_context("testid")

    def test_command1(self):
        response = self._client_context.bot.ask_question(self._client_context,  "command1")
        self.assertEqual(response, '<myTag1 name="myTag1"></myTag1> <myTag2 name="myTag2"></myTag2> Message from `command1`.')

    def test_command2(self):
        response = self._client_context.bot.ask_question(self._client_context,  "command2")
        self.assertEqual(response, 'Message from pattern `command2` <myTag1 name="myTag1"></myTag1> <myTag2 name="myTag2"></myTag2>.')

    def test_command3(self):
        response = self._client_context.bot.ask_question(self._client_context,  "command3")
        self.assertEqual(response, 'Command3 <myTag1 name="myTag1"></myTag1> <myTag2 name="myTag2"></myTag2> Message from pattern `command3`.')

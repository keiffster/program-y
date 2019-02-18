import unittest
import os

from programytest.client import TestClient


class GimisaTopicTestClient(TestClient):

    def __init__(self):
        TestClient.__init__(self)

    def load_storage(self):
        super(GimisaTopicTestClient, self).load_storage()
        self.add_default_stores()
        self.add_single_categories_store(os.path.dirname(__file__) + os.sep + "gimisa_test.aiml")
        self.add_sets_store([os.path.dirname(__file__)])

class GimisaAIMLTests(unittest.TestCase):

    def setUp(self):
        client = GimisaTopicTestClient()
        self._client_context = client.create_client_context("testid")

    def test_ask_blender_twice(self):
        response = self._client_context.bot.ask_question(self._client_context, "render")
        self.assertIsNotNone(response)
        self.assertEqual(response, 'Some definition of render as per professor ....')

        response = self._client_context.bot.ask_question(self._client_context, "hello")
        self.assertIsNotNone(response)
        self.assertEqual(response, 'Hi .. setting topic to blender....')

        response = self._client_context.bot.ask_question(self._client_context, "render")
        self.assertIsNotNone(response)
        self.assertEqual(response, 'The definition of render in blender is.')


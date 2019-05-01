import unittest
import os

from programytest.client import TestClient


class SraiTestClient(TestClient):

    def __init__(self):
        TestClient.__init__(self)

    def load_storage(self):
        super(SraiTestClient, self).load_storage()
        self.add_default_stores()
        self.add_categories_store([os.path.dirname(__file__)])


class SraiAIMLTests(unittest.TestCase):

    def setUp(self):
        client = SraiTestClient()
        self._client_context = client.create_client_context("testid")

        self._client_context.bot.brain.dynamics.add_dynamic_set('number', "programy.dynamic.sets.numeric.IsNumeric", None)

    def test_srai_response(self):
        response = self._client_context.bot.ask_question(self._client_context, "HELLO")
        self.assertIsNotNone(response)
        self.assertEqual(response, 'HI THERE.')

    def test_single_srai(self):
        response = self._client_context.bot.ask_question(self._client_context,  "HI")
        self.assertIsNotNone(response)
        self.assertEqual(response, 'HI THERE.')

    def test_multiple_srai(self):
        response = self._client_context.bot.ask_question(self._client_context, "MORNING")
        self.assertIsNotNone(response)
        self.assertEqual(response, 'WELL HI THERE AND HI THERE AGAIN.')

    def test_nested_srai(self):
        response = self._client_context.bot.ask_question(self._client_context, "FAREWELL")
        self.assertIsNotNone(response)
        self.assertEqual(response, 'SEEYA MATE.')

    def test_predicate_set_srai(self):
        response = self._client_context.bot.ask_question(self._client_context, "TEST PREDICATE SET")
        self.assertIsNotNone(response)
        self.assertEqual('Global1 set to Value1 and Local1 set to unknown and Local2 set to Value3.', response )

    def test_srai_with_star(self):
        response = self._client_context.bot.ask_question(self._client_context, "TEST MULTI SRAI KEITH STERLING")
        self.assertIsNotNone(response)
        self.assertEqual('TEST1 KEITH TEST1 TEST2 STERLING TEST2.', response)

    def test_srai_with_included_star(self):
        response = self._client_context.bot.ask_question(self._client_context, "TEST INCLUDED SRAI KEITH STERLING")
        self.assertIsNotNone(response)
        self.assertEqual('TEST1 KEITH TEST2 STERLING TEST2 TEST1.', response)

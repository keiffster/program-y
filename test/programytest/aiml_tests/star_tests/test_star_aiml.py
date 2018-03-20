import unittest
import os

from programy.context import ClientContext

from programytest.aiml_tests.client import TestClient


class StarTestClient(TestClient):

    def __init__(self):
        TestClient.__init__(self)

    def load_configuration(self, arguments):
        super(StarTestClient, self).load_configuration(arguments)
        self.configuration.client_configuration.configurations[0].configurations[0].files.aiml_files._files = [os.path.dirname(__file__)]


class StarAIMLTests(unittest.TestCase):

    def setUp(self):
        client = StarTestClient()
        self._client_context = client.create_client_context("testid")

        self._client_context.brain.dynamics.add_dynamic_set('number', "programy.dynamic.sets.numeric.IsNumeric", None)

    def test_star_first(self):
        response = self._client_context.bot.ask_question(self._client_context,  "SAY HEY")
        self.assertIsNotNone(response)
        self.assertEqual(response, 'STAR IS SAY')

    def test_star_first_multi_words(self):
        response = self._client_context.bot.ask_question(self._client_context,  "THE MAN SAYS HEY")
        self.assertIsNotNone(response)
        self.assertEqual(response, 'STAR IS THE MAN SAYS')

    def test_star_last(self):
        response = self._client_context.bot.ask_question(self._client_context,  "HELLO KEIFFBOT")
        self.assertIsNotNone(response)
        self.assertEqual(response, 'HI KEIFFBOT')

    def test_star_last_multi_words(self):
        response = self._client_context.bot.ask_question(self._client_context,  "HELLO KEIFFBOT MATE")
        self.assertIsNotNone(response)
        self.assertEqual(response, 'HI KEIFFBOT MATE')

    def test_multi_star(self):
        response = self._client_context.bot.ask_question(self._client_context, "WELL HI THERE")
        self.assertIsNotNone(response)
        self.assertEqual(response, 'YOU SAID WELL AND THERE')

    def test_multi_star_mulit_words(self):
        response = self._client_context.bot.ask_question(self._client_context, "WELL THEN HI THERE MATE")
        self.assertIsNotNone(response)
        self.assertEqual(response, 'YOU SAID WELL THEN AND THERE MATE')

    def test_star_middle(self):
        response = self._client_context.bot.ask_question(self._client_context, "GOODBYE KEIFF SEEYA")
        self.assertIsNotNone(response)
        self.assertEqual(response, 'LATER KEIFF')

    def test_star_middle_mulit_words(self):
        response = self._client_context.bot.ask_question(self._client_context, "GOODBYE KEIFF MATE SEEYA")
        self.assertIsNotNone(response)
        self.assertEqual(response, 'LATER KEIFF MATE')

    def test_multiple_stars_2(self):
        response = self._client_context.bot.ask_question(self._client_context, "MULTIPLE STARS MATCH THIS THAT")
        self.assertIsNotNone(response)
        self.assertEqual(response, 'YOU MATCHED FIRST AS THIS AND SECOND AS THAT')

    def test_multiple_stars_4(self):
        response = self._client_context.bot.ask_question(self._client_context, "MULTI STARS ONE TWO THREE FOUR")
        self.assertIsNotNone(response)
        self.assertEqual(response, 'FOUR THREE TWO ONE')

    def test_star_with_set(self):
        response = self._client_context.bot.ask_question(self._client_context, "STAR WITH SET 666")
        self.assertIsNotNone(response)
        self.assertEqual(response, 'SET IS 666')

    def test_multi_stars_with_set(self):
        response = self._client_context.bot.ask_question(self._client_context, "STAR WITH SETS 666 999")
        self.assertIsNotNone(response)
        self.assertEqual(response, 'SETS ARE 666 AND 999')

    def test_mixed_stars_and_sets(self):
        response = self._client_context.bot.ask_question(self._client_context, "MIXED STARS AND SETS 11 22 33 44 55")
        self.assertIsNotNone(response)
        self.assertEqual(response, 'STARS ARE 11 AND 22 AND 33 AND 44 AND 55')

    def test_recursion_one_star(self):
        response = self._client_context.bot.ask_question(self._client_context, "RECURSIVE TEST")
        self.assertIsNotNone(response)
        self.assertEqual(response, 'ENDED')

    def test_recursion_two_stars(self):
        response = self._client_context.bot.ask_question(self._client_context, "RECURSIVE TEST THIS")
        self.assertIsNotNone(response)
        self.assertEqual(response, 'RECURSED ENDED')

    def test_recursion_four_stars(self):
        response = self._client_context.bot.ask_question(self._client_context, "RECURSIVE TEST THIS THAT OTHER")
        self.assertIsNotNone(response)
        self.assertEqual(response, 'RECURSED RECURSED RECURSED ENDED')

    def test_star_case(self):
        response = self._client_context.bot.ask_question(self._client_context, "STAR CASE TEST1")
        self.assertIsNotNone(response)
        self.assertEqual(response, 'TEST1')

        response = self._client_context.bot.ask_question(self._client_context, "STAR CASE test2")
        self.assertIsNotNone(response)
        self.assertEqual(response, 'test2')

        response = self._client_context.bot.ask_question(self._client_context, "STAR CASE TesT3")
        self.assertIsNotNone(response)
        self.assertEqual(response, 'TesT3')

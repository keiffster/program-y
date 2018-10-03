import unittest
import os

from programytest.client import TestClient


class BasicTestClient(TestClient):

    def __init__(self):
        TestClient.__init__(self)

    def load_storage(self):
        super(BasicTestClient, self).load_storage()
        self.add_default_stores()
        self.add_categories_store([os.path.dirname(__file__)])


class BasicAIMLTests(unittest.TestCase):

    def setUp(self):
        client = BasicTestClient()
        self._client_context = client.create_client_context("testid")

    def test_basic_basic_text(self):
        response = self._client_context.bot.ask_question(self._client_context,  "NO RESPONSE")
        self.assertEqual(response, '')

    def test_basic_one_word(self):
        response = self._client_context.bot.ask_question(self._client_context,  "HELLO")
        self.assertEqual(response, "HELLO, WORLD.")

    def test_basic_two_words(self):
        response = self._client_context.bot.ask_question(self._client_context,  "HELLO THERE")
        self.assertEqual(response, "HOW ARE YOU.")

    def test_basic_three_words(self):
        response = self._client_context.bot.ask_question(self._client_context,  "HELLO THERE NOW")
        self.assertEqual(response, "HOW ARE YOU NOW.")

    def test_basic_no_match(self):
        response = self._client_context.bot.ask_question(self._client_context, "HELLO YOU")
        self.assertEqual(response, '')

    def test_star_after_no_match(self):
        response = self._client_context.bot.ask_question(self._client_context,  "HI")
        self.assertEqual(response, '')

    def test_star_after_no_match_single(self):
        response = self._client_context.bot.ask_question(self._client_context, "HI THERE")
        self.assertEqual(response, "HI, HOW ARE YOU.")

    def test_star_after_no_match_multiple(self):
        response = self._client_context.bot.ask_question(self._client_context, "HI THERE MATE")
        self.assertEqual(response, "HI, HOW ARE YOU.")

    def test_star_before_no_match(self):
        response = self._client_context.bot.ask_question(self._client_context, "HEY")
        self.assertEqual(response, '')

    def test_star_before_single(self):
        response = self._client_context.bot.ask_question(self._client_context, "WELL HEY")
        self.assertEqual(response, "HEY, HOW ARE YOU.")

    def test_star_before_multiple(self):
        response = self._client_context.bot.ask_question(self._client_context, "WELL NOW HEY")
        self.assertEqual(response, "HEY, HOW ARE YOU.")

    def test_star_before2(self):
        response = self._client_context.bot.ask_question(self._client_context, "HELLO THERE HEY")
        self.assertEqual(response, "HEY, HOW ARE YOU.")

    def test_hash_after(self):
        response = self._client_context.bot.ask_question(self._client_context, "HOWDY")
        self.assertEqual(response, "HOWDY PARTNER.")

        response = self._client_context.bot.ask_question(self._client_context, "HOWDY MATE")
        self.assertEqual(response, "HOWDY PARTNER.")

        response = self._client_context.bot.ask_question(self._client_context, "HOWDY THERE MATE")
        self.assertEqual(response, "HOWDY PARTNER.")

    def test_hash_before(self):
        response = self._client_context.bot.ask_question(self._client_context, "YO")
        self.assertEqual(response, "YO, HOW ARE YOU.")

        response = self._client_context.bot.ask_question(self._client_context, "HEY YO")
        self.assertEqual(response, "YO, HOW ARE YOU.")

        response = self._client_context.bot.ask_question(self._client_context, "HEY NOW YO")
        self.assertEqual(response, "YO, HOW ARE YOU.")

        response = self._client_context.bot.ask_question(self._client_context, "HELLO THERE YO")
        self.assertEqual(response, "YO, HOW ARE YOU.")

    def test_star_star_no_match(self):
        response = self._client_context.bot.ask_question(self._client_context, "GOODBYE")
        self.assertEqual(response, '')

    def test_star_star_still_no_match(self):
        response = self._client_context.bot.ask_question(self._client_context, "GOODBYE MATE")
        self.assertEqual(response, '')

    def test_star_star_match(self):
        response = self._client_context.bot.ask_question(self._client_context, "WELL GOODBYE MATE")
        self.assertEqual(response, "BYE BYE.")

    def test_star_hash_no_match(self):
        response = self._client_context.bot.ask_question(self._client_context, "SEEYA")
        self.assertEqual(response, '')

    def test_star_hash_still_no_match(self):
        response = self._client_context.bot.ask_question(self._client_context, "SEEYA MATE")
        self.assertEqual(response, '')

    def test_star_no_hash_match(self):
        response = self._client_context.bot.ask_question(self._client_context, "WELL SEEYA")
        self.assertEqual(response, "BYE THE NOW.")

    def test_star_hash_match(self):
        response = self._client_context.bot.ask_question(self._client_context, "WELL SEEYA MATE")
        self.assertEqual(response, "BYE THE NOW.")

    def test_hash_hash(self):
        response = self._client_context.bot.ask_question(self._client_context, "LATER")
        self.assertEqual(response, "LATERZ.")

        response = self._client_context.bot.ask_question(self._client_context, "LATER MATE")
        self.assertEqual(response, "LATERZ.")

        response = self._client_context.bot.ask_question(self._client_context, "WELL LATER")
        self.assertEqual(response, "LATERZ.")

        response = self._client_context.bot.ask_question(self._client_context, "WELL LATER MATE")
        self.assertEqual(response, "LATERZ.")

    def test_hash_star_no_match(self):
        response = self._client_context.bot.ask_question(self._client_context, "FAREWELL")
        self.assertEqual(response, '')

    def test_hash_star_hash_only(self):
        response = self._client_context.bot.ask_question(self._client_context, "WELL FAREWELL")
        self.assertEqual(response, '')

    def test_hash_star_no_hash_and_star(self):
        response = self._client_context.bot.ask_question(self._client_context, "WELL FAREWELL MATE")
        self.assertEqual(response, "UNTIL TOMORROW.")

    def test_hash_star_hash_and_star(self):
        response = self._client_context.bot.ask_question(self._client_context, "FAREWELL MATE")
        self.assertEqual(response, "UNTIL TOMORROW.")

    def test_hash_middle(self):
        response = self._client_context.bot.ask_question(self._client_context, "MORNING MATE")
        self.assertEqual(response, 'GOOD MORNING.')

        response = self._client_context.bot.ask_question(self._client_context, "MORNING THERE MATE")
        self.assertEqual(response, 'GOOD MORNING.')

        response = self._client_context.bot.ask_question(self._client_context, "MORNING MY GOOD MATE")
        self.assertEqual(response, 'GOOD MORNING.')

    def test_hash_middle_with_extra(self):
        response = self._client_context.bot.ask_question(self._client_context, "MORNING MATE AHOY")
        self.assertEqual(response, '')

        response = self._client_context.bot.ask_question(self._client_context, "MORNING MY MATE AHOY")
        self.assertEqual(response, '')

    def test_star_middle_no_match(self):
        response = self._client_context.bot.ask_question(self._client_context, "EVENING CHUM")
        self.assertEqual(response, '')

    def test_star_middle_still_no_match(self):
        response = self._client_context.bot.ask_question(self._client_context, "EVENING THERE CHUM HALLO")
        self.assertEqual(response, '')

    def test_star_middle_match_single(self):
        response = self._client_context.bot.ask_question(self._client_context, "EVENING THERE CHUM")
        self.assertEqual(response, 'GOOD EVENING.')

    def test_star_middle_match_multi(self):
        response = self._client_context.bot.ask_question(self._client_context, "EVENING THERE MY CHUM")
        self.assertEqual(response, 'GOOD EVENING.')


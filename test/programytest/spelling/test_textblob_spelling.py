import unittest

from programy.spelling.textblob_spelling import TextBlobSpellingChecker
from programy.spelling.base import SpellingChecker
from programy.config.bot.spelling import BotSpellingConfiguration

from programytest.client import TestClient


class TextBlobSpellingCheckerTests(unittest.TestCase):

    def test_spellchecker(self):
        client = TestClient()

        checker = TextBlobSpellingChecker()
        self.assertIsNotNone(checker)
        checker.initialise(client)

        self.assertEqual("Have", checker.correct("Havve"))
        self.assertEqual("I have good spelling!", checker.correct("I havv good speling!"))
        self.assertEqual("That is your location", checker.correct("Waht is your locetion"))

    def test_initiate_spellchecker(self):

        spelling_config = BotSpellingConfiguration()
        spelling_config._load = True
        spelling_config._classname = "programy.spelling.textblob_spelling.TextBlobSpellingChecker"

        client = TestClient()
        storage_factory = client.storage_factory

        spell_checker = SpellingChecker.initiate_spellchecker(spelling_config, storage_factory)

        self.assertIsNotNone(spell_checker)


import unittest

from programy.spelling.autocorrection import AutoCorrectSpellingChecker
from programy.spelling.base import SpellingChecker
from programy.config.bot.spelling import BotSpellingConfiguration

from programytest.client import TestClient


class AutoCorrectSpellingCheckerTests(unittest.TestCase):

    def test_spellchecker(self):
        client = TestClient()

        checker = AutoCorrectSpellingChecker()
        self.assertIsNotNone(checker)
        checker.initialise(client)

        self.assertEqual("THIS", checker.correct("THIS"))
        self.assertEqual("THIS", checker.correct("This"))
        self.assertEqual("THIS", checker.correct("this"))

        self.assertEqual("LOCATION", checker.correct("LOCETION"))
        self.assertEqual("LOCATION", checker.correct("Locetion"))
        self.assertEqual("LOCATION", checker.correct("locetion"))

        self.assertEqual("WHAT IS YOUR LOCATION", checker.correct("Waht is your locetion"))

    def test_initiate_spellchecker(self):

        spelling_config = BotSpellingConfiguration()
        spelling_config._load = True
        spelling_config._classname = "programy.spelling.autocorrection.AutoCorrectSpellingChecker"

        client = TestClient()
        storage_factory = client.storage_factory

        spell_checker = SpellingChecker.initiate_spellchecker(spelling_config, storage_factory)

        self.assertIsNotNone(spell_checker)


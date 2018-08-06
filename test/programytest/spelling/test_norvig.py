import unittest

from programy.spelling.base import SpellingChecker
from programy.spelling.norvig import NorvigSpellingChecker
from programy.config.bot.spelling import BotSpellingConfiguration

from programytest.client import TestClient

class NorvigSpellingCheckerTests(unittest.TestCase):

    def test_spellchecker(self):
        client = TestClient()

        client.add_license_keys_store()
        client.add_spelling_store()

        checker = NorvigSpellingChecker()
        self.assertIsNotNone(checker)
        checker.initialise(client.storage_factory)

        self.assertEqual("THIS", checker.correct("THIS"))
        self.assertEqual("THIS", checker.correct("This"))
        self.assertEqual("THIS", checker.correct("this"))

        self.assertEqual("LOCATION", checker.correct("LOCETION"))
        self.assertEqual("LOCATION", checker.correct("Locetion"))
        self.assertEqual("LOCATION", checker.correct("locetion"))

    def test_initiate_spellchecker(self):

        spelling_config = BotSpellingConfiguration()
        spelling_config._load = True
        spelling_config._classname = "programy.spelling.norvig.NorvigSpellingChecker"

        client = TestClient()
        storage_factory = client.storage_factory

        spell_checker = SpellingChecker.initiate_spellchecker(spelling_config, storage_factory)

        self.assertIsNotNone(spell_checker)


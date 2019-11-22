import unittest

from programy.config.bot.spelling import BotSpellingConfiguration
from programy.spelling.base import SpellingChecker
from programy.spelling.norvig import NorvigSpellingChecker
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

    def test_probability(self):
        checker = NorvigSpellingChecker()
        self.assertEquals(0.0, checker._probability("WORD"))

        checker.add_corpus("WORD")
        self.assertEquals(1.0, checker._probability("WORD"))

    def test_edits(self):
        checker = NorvigSpellingChecker()
        checker.add_corpus("THIS IS A WORD AND SO IS THIS")

        edits1 = checker._edits1('AND')
        list1 = list(edits1)
        list1.sort()
        self.assertEquals(list1[0], 'AAD')

        edits2 = checker._edits2('AND')
        list2 = [x for x in edits2]
        list2.sort()
        self.assertEquals('A', list2[0])

    def test_initiate_spellchecker(self):

        spelling_config = BotSpellingConfiguration()
        spelling_config._load = True
        spelling_config._classname = "programy.spelling.norvig.NorvigSpellingChecker"

        client = TestClient()
        storage_factory = client.storage_factory

        spell_checker = SpellingChecker.initiate_spellchecker(spelling_config, storage_factory)

        self.assertIsNotNone(spell_checker)

    def test_initiate_spellchecker_no_storage(self):

        spelling_config = BotSpellingConfiguration()
        spelling_config._load = True
        spelling_config._classname = "programy.spelling.norvig.NorvigSpellingChecker"

        client = TestClient()
        storage_factory = client.storage_factory

        spell_checker = SpellingChecker.initiate_spellchecker(spelling_config, storage_factory)

        self.assertIsNotNone(spell_checker)

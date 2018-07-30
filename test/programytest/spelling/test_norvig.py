import unittest

from programy.spelling.norvig import NorvigSpellingChecker

from programytest.client import TestClient

class NorvigSpellingCheckerTests(unittest.TestCase):

    def test_spellchecker(self):
        client = TestClient()

        client.add_license_keys_store()
        client.add_spelling_store()

        checker = NorvigSpellingChecker()
        self.assertIsNotNone(checker)
        checker.initialise(client)

        self.assertEqual("THIS", checker.correct("THIS"))
        self.assertEqual("THIS", checker.correct("This"))
        self.assertEqual("THIS", checker.correct("this"))

        self.assertEqual("LOCATION", checker.correct("LOCETION"))
        self.assertEqual("LOCATION", checker.correct("Locetion"))
        self.assertEqual("LOCATION", checker.correct("locetion"))

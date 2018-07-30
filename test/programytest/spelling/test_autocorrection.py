import unittest

from programy.spelling.autocorrection import AutoCorrectSpellingChecker

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
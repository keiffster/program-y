import unittest

from programy.utils.spelling.checker import SpellingChecker

class SpellingCheckerTests(unittest.TestCase):

    def test_spellchecker(self):
        checker = SpellingChecker()
        self.assertIsNotNone(checker)

        self.assertEqual("THIS", checker.correct("THIS"))
        self.assertEqual("THIS", checker.correct("This"))
        self.assertEqual("THIS", checker.correct("this"))

        self.assertEqual("LOCATION", checker.correct("LOCETION"))
        self.assertEqual("LOCATION", checker.correct("Locetion"))
        self.assertEqual("LOCATION", checker.correct("locetion"))

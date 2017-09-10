import unittest

from programy.spelling.norvig import NorvigSpellingChecker

class NorvigSpellingCheckerTests(unittest.TestCase):

    def test_spellchecker(self):
        checker = NorvigSpellingChecker()
        self.assertIsNotNone(checker)

        self.assertEqual("THIS", checker.correct("THIS"))
        self.assertEqual("THIS", checker.correct("This"))
        self.assertEqual("THIS", checker.correct("this"))

        self.assertEqual("LOCATION", checker.correct("LOCETION"))
        self.assertEqual("LOCATION", checker.correct("Locetion"))
        self.assertEqual("LOCATION", checker.correct("locetion"))

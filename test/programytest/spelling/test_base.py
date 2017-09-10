import unittest

from programy.spelling.base import SpellingChecker

class SpellingCheckerTests(unittest.TestCase):

    def test_ensure_not_implemented(self):

        checker = SpellingChecker()
        self.assertIsNotNone(checker)
        with self.assertRaises(Exception):
            checker.correct("Test This")
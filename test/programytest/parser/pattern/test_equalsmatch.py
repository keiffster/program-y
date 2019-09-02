import unittest

from programy.parser.pattern.equalsmatch import EqualsMatch


class EqualsMatchTests(unittest.TestCase):

    def test_equals_match(self):
        equals_match = EqualsMatch(True, 1, "Hello World")
        self.assertIsNotNone(equals_match)
        self.assertTrue(equals_match.matched)
        self.assertEqual(1, equals_match.word_no)
        self.assertEqual("Hello World", equals_match.matched_phrase)
        self.assertEqual("True, 1, Hello World", equals_match.to_string())

    def test_equals_match_no_match_phrase(self):
        equals_match = EqualsMatch(False, 3)
        self.assertIsNotNone(equals_match)
        self.assertFalse(equals_match.matched)
        self.assertEqual(3, equals_match.word_no)
        self.assertEqual(None, equals_match.matched_phrase)
        self.assertEqual("False, 3, ''", equals_match.to_string())

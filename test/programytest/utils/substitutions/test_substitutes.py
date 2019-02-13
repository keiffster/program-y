import unittest
import os

from programy.utils.substitutions.substitues import Substitutions


class SubstitutionsTests(unittest.TestCase):

    def test_basics(self):

        sub = Substitutions()

        sub.add_substitute("$FIRSTNAME", "Fred")
        sub.add_substitute("$SURNAME", "West")
        sub.add_substitute("$WIFE", "Mary")

        self.assertTrue(sub.has_substitute("$FIRSTNAME"))
        self.assertFalse(sub.has_substitute("$FRED"))

        self.assertEquals("Fred", sub.get_substitute("$FIRSTNAME"))
        self.assertEquals("West", sub.get_substitute("$SURNAME"))
        self.assertEquals("Mary", sub.get_substitute("$WIFE"))

        with self.assertRaises(ValueError):
            sub.get_substitute("$NUMBER")

        sub.empty()

        self.assertFalse(sub.has_substitute("$FIRSTNAME"))
        self.assertFalse(sub.has_substitute("$SURNAME"))
        self.assertFalse(sub.has_substitute("$WIFE"))

    def test_load(self):

        sub = Substitutions()

        sub.load_substitutions(os.path.dirname(__file__) + os.sep + "subs.txt")

        self.assertEquals("Fred", sub.get_substitute("$FIRSTNAME"))
        self.assertEquals("West", sub.get_substitute("$SURNAME"))
        self.assertEquals("Mary", sub.get_substitute("$WIFE"))

        with self.assertRaises(ValueError):
            sub.get_substitute("$NUMBER")

    def test_substitutions(self):

        sub = Substitutions()

        sub.load_substitutions(os.path.dirname(__file__) + os.sep + "subs.txt")

        self.assertEquals("My name is Fred West", sub.replace("My name is $FIRSTNAME $SURNAME"))
        self.assertEquals("My name is FredWest", sub.replace("My name is $FIRSTNAME$SURNAME"))


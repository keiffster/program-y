import os
import unittest

from programy.utils.substitutions.substitues import Substitutions


class SubstitutionsTests(unittest.TestCase):

    def test_basics(self):

        sub = Substitutions()

        sub.add_substitute("$FIRSTNAME", "Fred")
        sub.add_substitute("$SURNAME", "West")
        sub.add_substitute("$WIFE", "Mary")

        self.assertTrue(sub.has_substitute("$FIRSTNAME"))
        self.assertFalse(sub.has_substitute("$FRED"))

        self.assertEqual("Fred", sub.get_substitute("$FIRSTNAME"))
        self.assertEqual("West", sub.get_substitute("$SURNAME"))
        self.assertEqual("Mary", sub.get_substitute("$WIFE"))

        with self.assertRaises(ValueError):
            sub.get_substitute("$NUMBER")

        sub.empty()

        self.assertFalse(sub.has_substitute("$FIRSTNAME"))
        self.assertFalse(sub.has_substitute("$SURNAME"))
        self.assertFalse(sub.has_substitute("$WIFE"))

    def test_load(self):

        sub = Substitutions()

        sub.load_substitutions(os.path.dirname(__file__) + os.sep + "subs.txt")

        self.assertEqual("Fred", sub.get_substitute("$FIRSTNAME"))
        self.assertEqual("West", sub.get_substitute("$SURNAME"))
        self.assertEqual("Mary", sub.get_substitute("$WIFE"))

        with self.assertRaises(ValueError):
            sub.get_substitute("$NUMBER")

    def test_load_bad_subs(self):

        sub = Substitutions()

        sub.load_substitutions(os.path.dirname(__file__) + os.sep + "bad_subs.txt")

        with self.assertRaises(ValueError):
            _ = sub.get_substitute("$FIRSTNAME")

    def test_substitutions(self):

        sub = Substitutions()

        sub.load_substitutions(os.path.dirname(__file__) + os.sep + "subs.txt")

        self.assertEquals("Two words", sub.get_substitute("$MULTIPLE"))

        self.assertEqual("My name is Fred West", sub.replace("My name is $FIRSTNAME $SURNAME"))
        self.assertEqual("My name is FredWest", sub.replace("My name is $FIRSTNAME$SURNAME"))

    def test_substitutions_no_file(self):

        sub = Substitutions()

        sub.load_substitutions(None)

    def test_add_duplicate(self):

        sub = Substitutions()

        sub.add_substitute("$FIRSTNAME", "Fred")
        sub.add_substitute("$FIRSTNAME", "Fred")

        self.assertTrue(sub.has_substitute("$FIRSTNAME"))

    def test_add_duplicate(self):

        sub = Substitutions()

        sub.add_substitute("$FIRSTNAME", "Fred")
        sub.add_substitute("$FIRSTNAME", "Fred")

        self.assertTrue(sub.has_substitute("$FIRSTNAME"))

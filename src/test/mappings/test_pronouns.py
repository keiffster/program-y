import unittest

from programy.mappings.pronouns import PronounsCollection


class PronounsTests(unittest.TestCase):

    def test_collection(self):
        collection = PronounsCollection()
        self.assertIsNotNone(collection)

        count = collection.load_from_text("""
            he
            she
            it
            they
            we
           """)
        self.assertEqual(count, 5)
        self.assertTrue(collection.is_pronoun("he"))

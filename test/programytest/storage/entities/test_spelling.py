import unittest
import unittest.mock

from programy.storage.entities.spelling import SpellingStore


class SpellingStoreTests(unittest.TestCase):

    def test_load_spelling(self):
        store = SpellingStore()
        with self.assertRaises(NotImplementedError):
            spell_checker = unittest.mock.Mock()
            store.load_spelling(spell_checker)

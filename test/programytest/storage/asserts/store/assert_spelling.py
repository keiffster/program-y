import unittest
import os
import os.path

from programy.spelling.norvig import NorvigSpellingChecker


class SpellingStoreAsserts(unittest.TestCase):

    def assert_upload_from_file(self, store):
        store.empty()

        store.upload_from_file(os.path.dirname(__file__) + os.sep + "data" + os.sep + "spelling" + os.sep + "corpus.txt")

        spelling_checker = NorvigSpellingChecker()
        store.load_spelling(spelling_checker)

        self.assertEqual("THESE ARE SOME WORDS", spelling_checker.correct("Thise ara sime wards"))
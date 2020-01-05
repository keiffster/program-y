import os
import os.path
import unittest
from programy.spelling.norvig import NorvigSpellingChecker


class SpellingStoreAsserts(unittest.TestCase):

    def assert_upload_from_file(self, store, verbose):
        store.empty()

        store.upload_from_file(os.path.dirname(__file__) + os.sep + "data" + os.sep + "spelling" + os.sep + "corpus.txt", verbose=verbose)

        spelling_checker = NorvigSpellingChecker()

        self.assertEquals(0, len(spelling_checker.words))
        self.assertEquals(0, spelling_checker.sum_of_words)

        store.load_spelling(spelling_checker)

        self.assertEquals(9, len(spelling_checker.words))
        self.assertEquals(9, spelling_checker.sum_of_words)

        self.assertEqual("THESE ARE SOME WORDS", spelling_checker.correct("Thise ara sime wards"))

    def assert_upload_from_file_no_corpus(self, store, verbose):
        store.empty()

        spelling_checker = NorvigSpellingChecker()
        store.load_spelling(spelling_checker)

        spelling_checker = NorvigSpellingChecker()

        self.assertEquals(0, len(spelling_checker.words))
        self.assertEquals(0, spelling_checker.sum_of_words)

        store.load_spelling(spelling_checker)

        self.assertEquals(0, len(spelling_checker.words))
        self.assertEquals(0, spelling_checker.sum_of_words)

    def assert_upload_from_file_exception(self, store, verbose):
        store.empty()

        spelling_checker = NorvigSpellingChecker()
        store.load_spelling(spelling_checker)

        store.upload_from_file(os.path.dirname(__file__) + os.sep + "data" + os.sep + "spelling" + os.sep + "corpus.txt", verbose=verbose)

        spelling_checker = NorvigSpellingChecker()

        self.assertEquals(0, len(spelling_checker.words))
        self.assertEquals(0, spelling_checker.sum_of_words)

        store.load_spelling(spelling_checker)

        self.assertEquals(0, len(spelling_checker.words))
        self.assertEquals(0, spelling_checker.sum_of_words)

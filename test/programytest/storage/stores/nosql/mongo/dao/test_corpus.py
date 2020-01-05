import unittest

from programy.storage.stores.nosql.mongo.dao.corpus import Corpus


class CorpusTests(unittest.TestCase):

    def test_init_no_id(self):
        corpus = Corpus(words=["keiffster", "ABCDEF123", "PASSWORD123"])

        self.assertIsNotNone(corpus)
        self.assertIsNone(corpus.id)
        self.assertEqual(["keiffster", "ABCDEF123", "PASSWORD123"], corpus.words)

        self.assertEqual({'words': ['keiffster', 'ABCDEF123', 'PASSWORD123']}, corpus.to_document())

    def test_init_with_id(self):
        corpus = Corpus(words=["keiffster", "ABCDEF123", "PASSWORD123"])
        corpus.id = '666'

        self.assertIsNotNone(corpus)
        self.assertIsNotNone(corpus.id)
        self.assertEqual(["keiffster", "ABCDEF123", "PASSWORD123"], corpus.words)

        self.assertEqual({'_id': '666', 'words': ['keiffster', 'ABCDEF123', 'PASSWORD123']}, corpus.to_document())

    def test_from_document_no_id(self):
        corpus1 = Corpus.from_document({'words': ['keiffster', 'ABCDEF123', 'PASSWORD123']})
        self.assertIsNotNone(corpus1)
        self.assertIsNone(corpus1.id)
        self.assertEqual(['keiffster', 'ABCDEF123', 'PASSWORD123'], corpus1.words)

    def test_from_document_with_id(self):
        corpus2 = Corpus.from_document({'_id': '666', 'words': ['keiffster', 'ABCDEF123', 'PASSWORD123']})
        self.assertIsNotNone(corpus2)
        self.assertEqual("666", corpus2.id)
        self.assertEqual(['keiffster', 'ABCDEF123', 'PASSWORD123'], corpus2.words)

    def test_from_document_no_words(self):
        corpus2 = Corpus.from_document({'_id': '666'})
        self.assertIsNotNone(corpus2)
        self.assertEqual("666", corpus2.id)
        self.assertEqual([], corpus2.words)

    def test_repr(self):
        corpus1 = Corpus.from_document({'words': ['keiffster', 'ABCDEF123', 'PASSWORD123']})

        self.assertEquals("<Corpus(id='n/a')>", str(corpus1))

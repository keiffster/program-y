
import unittest

from programy.storage.stores.sql.dao.corpus import Corpus

class CorpusTests(unittest.TestCase):
    
    def test_init(self):
        corpus1 = Corpus(word="wordup")
        self.assertIsNotNone(corpus1)
        self.assertEqual("<Corpus(id='n/a', word='wordup'>", str(corpus1))
        
        corpus2 = Corpus(id=1, word="wordup")
        self.assertIsNotNone(corpus2)
        self.assertEqual("<Corpus(id='1', word='wordup'>", str(corpus2))

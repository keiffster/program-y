
import unittest

from programy.storage.stores.sql.dao.duplicate import Duplicate

class CategoryTests(unittest.TestCase):
    
    def test_init(self):
        duplicate1 = Duplicate(duplicate='duplicate', file='file', start='100', end='200')
        self.assertIsNotNone(duplicate1)
        self.assertEqual("<Duplicate(id='n/a', duplicate='duplicate', file='file', start='100', end='200')>", str(duplicate1))
        
        duplicate2 = Duplicate(id=1, duplicate='duplicate', file='file', start='100', end='200')
        self.assertIsNotNone(duplicate2)
        self.assertEqual("<Duplicate(id='1', duplicate='duplicate', file='file', start='100', end='200')>", str(duplicate2))

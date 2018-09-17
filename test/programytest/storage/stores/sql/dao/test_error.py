
import unittest

from programy.storage.stores.sql.dao.error import Error

class ErrorTests(unittest.TestCase):
    
    def test_init(self):
        error1 = Error(error='error', file='file', start='100', end='200')
        self.assertIsNotNone(error1)
        self.assertEqual("<Error(id='n/a', error='error', file='file', start='100', end='200')>", str(error1))
        
        error2 = Error(id='1', error='error', file='file', start='100', end='200')
        self.assertIsNotNone(error2)
        self.assertEqual("<Error(id='1', error='error', file='file', start='100', end='200')>", str(error2))

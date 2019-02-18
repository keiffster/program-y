
import unittest

from programy.storage.stores.sql.dao.linked import LinkedAccount

class LinkedAccountTests(unittest.TestCase):
    
    def test_init(self):
        linked1 = LinkedAccount(primary_user='primary', linked_user='linked')
        self.assertIsNotNone(linked1)
        self.assertEqual("<Linked(id='n/a', primary_user='primary', linked_user='linked')>", str(linked1))
        
        linked2 = LinkedAccount(id=1, primary_user='primary', linked_user='linked')
        self.assertIsNotNone(linked2)
        self.assertEqual("<Linked(id='1', primary_user='primary', linked_user='linked')>", str(linked2))

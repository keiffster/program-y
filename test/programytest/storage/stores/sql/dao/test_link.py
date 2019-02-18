
import unittest

from programy.storage.stores.sql.dao.link import Link

class LinkTests(unittest.TestCase):
    
    def test_init(self):
        link1 = Link(primary_user='user', generated_key='%key1', provided_key='key2', expired=True, expires='29/02/1968', retry_count=0)
        self.assertIsNotNone(link1)
        self.assertEqual("<Linked(id='n/a', primary_user='user', provided_key='key2', generated_key='%key1', expired='True', expires='29/02/1968', retry_count='0')>", str(link1))
        
        link2 = Link(id=1, primary_user='user', generated_key='%key1', provided_key='key2', expired=True, expires='29/02/1968', retry_count=0)
        self.assertIsNotNone(link2)
        self.assertEqual("<Linked(id='1', primary_user='user', provided_key='key2', generated_key='%key1', expired='True', expires='29/02/1968', retry_count='0')>", str(link2))


import unittest

from programy.storage.stores.sql.dao.twitter import Twitter

class TwitterTests(unittest.TestCase):
    
    def test_init(self):
        twitter1 = Twitter(last_direct_message_id='66', last_status_id='99')
        self.assertIsNotNone(twitter1)
        self.assertEqual("<Twitter(id='n/a', last_direct_message_id='66', last_status_id='99')>", str(twitter1))
        
        twitter2 = Twitter(id=1, last_direct_message_id='66', last_status_id='99')
        self.assertIsNotNone(twitter2)
        self.assertEqual("<Twitter(id='1', last_direct_message_id='66', last_status_id='99')>", str(twitter2))

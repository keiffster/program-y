
import unittest

from programy.storage.stores.sql.dao.user import User

class UserTests(unittest.TestCase):
    
    def test_init(self):
        user1 = User(userid='user', client='client')
        self.assertIsNotNone(user1)
        self.assertEqual("<User(id='n/a', userid='user', client='client')>", str(user1))

        user2 = User(id=1, userid='user', client='client')
        self.assertIsNotNone(user2)
        self.assertEqual("<User(id='1', userid='user', client='client')>", str(user2))

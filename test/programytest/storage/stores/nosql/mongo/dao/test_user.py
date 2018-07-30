import unittest

from programy.storage.stores.nosql.mongo.dao.user import User

class UserTests(unittest.TestCase):

    def test_init(self):
        user = User("keiffster", "console")

        self.assertIsNotNone(user)
        self.assertIsNone(user.id)
        self.assertEquals("keiffster", user.userid)
        self.assertEquals("console", user.client)


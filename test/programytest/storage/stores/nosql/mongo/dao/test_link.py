import unittest

from programy.storage.stores.nosql.mongo.dao.link import Link

class LinkTests(unittest.TestCase):

    def test_init(self):
        link = Link("keiffster", "ABCDEF123", "PASSWORD123")

        self.assertIsNotNone(link)
        self.assertIsNone(link.id)
        self.assertEquals("keiffster", link.primary_user)
        self.assertEquals("ABCDEF123", link.generated_key)
        self.assertEquals("PASSWORD123", link.provided_key)


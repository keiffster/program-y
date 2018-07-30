import unittest

from programy.storage.stores.nosql.mongo.dao.linked import LinkedAccount

class LinkedAccountTests(unittest.TestCase):

    def test_init(self):
        linkedaccount = LinkedAccount("keiffster", "@keiffster")

        self.assertIsNotNone(linkedaccount)
        self.assertIsNone(linkedaccount.id)
        self.assertEquals("keiffster", linkedaccount.primary_userid)
        self.assertEquals("@keiffster", linkedaccount.linked_userid)


import unittest

from programy.storage.stores.nosql.mongo.dao.link import Link

class LinkTests(unittest.TestCase):

    def test_init_no_id_no_expiration(self):
        link = Link("keiffster", "PASSWORD123", "ABCDEF123")

        self.assertIsNotNone(link)
        self.assertIsNone(link.id)
        self.assertEqual("keiffster", link.primary_user)
        self.assertEqual("ABCDEF123", link.generated_key)
        self.assertEqual("PASSWORD123", link.provided_key)

        self.assertEqual({'expired': False, 'expires': None, 'generated_key': 'ABCDEF123', 'primary_user': 'keiffster', 'provided_key': 'PASSWORD123', 'retry_count': 0}, link.to_document())

    def test_init_no_id_no(self):
        link = Link("keiffster", "PASSWORD123", "ABCDEF123", expired=False, expires="12/12/2012")

        self.assertIsNotNone(link)
        self.assertIsNone(link.id)
        self.assertEqual("keiffster", link.primary_user)
        self.assertEqual("ABCDEF123", link.generated_key)
        self.assertEqual("PASSWORD123", link.provided_key)
        self.assertEqual(False, link.expired)
        self.assertEqual("12/12/2012", link.expires)
        self.assertEqual(0, link.retry_count)

        self.assertEqual({'expired': False, 'expires': "12/12/2012", 'generated_key': 'ABCDEF123', 'primary_user': 'keiffster', 'provided_key': 'PASSWORD123', 'retry_count': 0}, link.to_document())

    def test_init(self):
        link = Link("keiffster", "PASSWORD123", "ABCDEF123", expired=False, expires="12/12/2012")
        link.id = "666"

        self.assertIsNotNone(link)
        self.assertEqual("666", link.id)
        self.assertEqual("keiffster", link.primary_user)
        self.assertEqual("ABCDEF123", link.generated_key)
        self.assertEqual("PASSWORD123", link.provided_key)
        self.assertEqual(False, link.expired)
        self.assertEqual("12/12/2012", link.expires)
        self.assertEqual(0, link.retry_count)

        self.assertEqual({'_id': '666', 'expired': False, 'expires': "12/12/2012", 'generated_key': 'ABCDEF123', 'primary_user': 'keiffster', 'provided_key': 'PASSWORD123', 'retry_count': 0}, link.to_document())

    def test_from_document(self):
        data1 = {"primary_user": "user1", "generated_key": "ABCDEFG", "provided_key": "1234567890", "expired": False, "expires": "12/12/2012", 'retry_count': 0}
        link1 = Link.from_document(data1)
        self.assertIsNotNone(link1)
        self.assertEqual("user1", link1.primary_user)
        self.assertEqual("ABCDEFG", link1.generated_key)
        self.assertEqual("1234567890", link1.provided_key)
        self.assertEqual(False, link1.expired)
        self.assertEqual("12/12/2012", link1.expires)
        self.assertEqual(0, link1.retry_count)

        data2 = {"_id": "666", "primary_user": "user1", "generated_key": "ABCDEFG", "provided_key": "1234567890", "expired": False, "expires": "12/12/2012", 'retry_count': 0}
        link2 = Link.from_document(data2)
        self.assertIsNotNone(link2)
        self.assertEqual("user1", link2.primary_user)
        self.assertEqual("ABCDEFG", link2.generated_key)
        self.assertEqual("1234567890", link2.provided_key)
        self.assertEqual(False, link2.expired)
        self.assertEqual("12/12/2012", link2.expires)
        self.assertEqual(0, link1.retry_count)
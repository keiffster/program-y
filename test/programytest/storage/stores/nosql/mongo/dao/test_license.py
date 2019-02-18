import unittest

from programy.storage.stores.nosql.mongo.dao.license import LicenseKey


class LicenseKeyTests(unittest.TestCase):

    def test_init_no_id(self):
        license = LicenseKey(name='name', key='key')

        self.assertIsNotNone(license)
        self.assertIsNone(license.id)
        self.assertEqual('name', license.name)
        self.assertEqual('key', license.key)
        self.assertEqual({'key': 'key', 'name': 'name'}, license.to_document())

    def test_init_with_id(self):
        license = LicenseKey(name='name', key='key')
        license.id = '666'

        self.assertIsNotNone(license)
        self.assertIsNotNone(license.id)
        self.assertEqual('666', license.id)
        self.assertEqual('name', license.name)
        self.assertEqual('key', license.key)
        self.assertEqual({'_id': '666', 'key': 'key', 'name': 'name'}, license.to_document())

    def test_from_document(self):
        license1 = LicenseKey.from_document({'key': 'key', 'name': 'name'})
        self.assertIsNotNone(license1)
        self.assertIsNone(license1.id)
        self.assertEqual('name', license1.name)
        self.assertEqual('key', license1.key)

        license2 = LicenseKey.from_document({'_id': '666', 'key': 'key', 'name': 'name'})
        self.assertIsNotNone(license2)
        self.assertIsNotNone(license2.id)
        self.assertEqual('666', license2.id)
        self.assertEqual('666', license2.id)
        self.assertEqual('name', license2.name)
        self.assertEqual('key', license2.key)

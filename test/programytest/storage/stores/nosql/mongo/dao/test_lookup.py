import unittest

from programy.storage.stores.nosql.mongo.dao.lookup import Lookup


class LookupTests(unittest.TestCase):

    def test_init_no_id(self):
        lookup = Lookup(key='key1', value='value1')

        self.assertIsNotNone(lookup)
        self.assertIsNone(lookup.id)
        self.assertEqual('key1', lookup.key)
        self.assertEqual('value1', lookup.value)
        self.assertEqual({'key': 'key1', 'value': 'value1'}, lookup.to_document())

    def test_init_with_id(self):
        lookup = Lookup(key='key1', value='value1')
        lookup.id = '666'

        self.assertIsNotNone(lookup)
        self.assertIsNotNone(lookup.id)
        self.assertEqual('666', lookup.id)
        self.assertEqual('key1', lookup.key)
        self.assertEqual('value1', lookup.value)
        self.assertEqual({'_id': '666', 'key': 'key1', 'value': 'value1'}, lookup.to_document())

    def test_from_document(self):
        lookup1 = Lookup.from_document({'key': 'key1', 'value': 'value1'})
        self.assertIsNotNone(lookup1)
        self.assertIsNone(lookup1.id)
        self.assertEqual('key1', lookup1.key)
        self.assertEqual('value1', lookup1.value)

        lookup2 = Lookup.from_document({'_id': '666', 'key': 'key1', 'value': 'value1'})
        self.assertIsNotNone(lookup2)
        self.assertIsNotNone(lookup2.id)
        self.assertEqual('666', lookup2.id)
        self.assertEqual('key1', lookup2.key)
        self.assertEqual('value1', lookup2.value)

import unittest

from programy.storage.stores.nosql.mongo.dao.map import Map


class MapTests(unittest.TestCase):

    def test_init_no_id(self):
        amap = Map(name="TEST", key_values={"key1": "val1", "key2": "val2"})

        self.assertIsNotNone(amap)
        self.assertIsNone(amap.id)
        self.assertEqual("TEST", amap.name)
        self.assertEqual({"key1": "val1", "key2": "val2"}, amap.key_values)
        self.assertEqual({'key_values': {'key1': 'val1', 'key2': 'val2'}, 'name': 'TEST'}, amap.to_document())

    def test_init_with_id(self):
        amap = Map(name="TEST", key_values={"key1": "val1", "key2": "val2"})
        amap.id = '666'

        self.assertIsNotNone(amap)
        self.assertIsNotNone(amap.id)
        self.assertEqual('666', amap.id)
        self.assertEqual("TEST", amap.name)
        self.assertEqual({"key1": "val1", "key2": "val2"}, amap.key_values)
        self.assertEqual({'_id': '666', 'key_values': {'key1': 'val1', 'key2': 'val2'}, 'name': 'TEST'}, amap.to_document())

    def test_from_document_no_id(self):
        amap1 = Map.from_document({'key_values': {'key1': 'val1', 'key2': 'val2'}, 'name': 'TEST'})
        self.assertIsNotNone(amap1)
        self.assertIsNone(amap1.id)
        self.assertEqual("TEST", amap1.name)
        self.assertEqual({"key1": "val1", "key2": "val2"}, amap1.key_values)

    def test_from_document_with_id(self):
        amap2 = Map.from_document({'_id': '666', 'key_values': {'key1': 'val1', 'key2': 'val2'}, 'name': 'TEST'})
        self.assertIsNotNone(amap2)
        self.assertIsNotNone(amap2.id)
        self.assertEqual('666', amap2.id)
        self.assertEqual("TEST", amap2.name)
        self.assertEqual({"key1": "val1", "key2": "val2"}, amap2.key_values)

    def test_repr_no_id(self):
        amap1 = Map.from_document({'key_values': {'key1': 'val1', 'key2': 'val2'}, 'name': 'TEST'})
        self.assertEquals("<Map(id='n/a', name='TEST', values='key1, key2')>", str(amap1))

    def test_repr_with_id(self):
        amap2 = Map.from_document({'_id': '666', 'key_values': {'key1': 'val1', 'key2': 'val2'}, 'name': 'TEST'})
        self.assertEquals("<Map(id='666', name='TEST', values='key1, key2')>", str(amap2))

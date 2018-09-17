import unittest

from programy.storage.stores.nosql.mongo.dao.set import Set


class SetTests(unittest.TestCase):

    def test_init_no_id(self):
        aset = Set(name="TEST", values=["val1", "val2", "val3"])

        self.assertIsNotNone(aset)
        self.assertIsNone(aset.id)
        self.assertEqual("TEST", aset.name)
        self.assertEqual(["val1", "val2", "val3"], aset.values)
        self.assertEqual({'values': ["val1", "val2", "val3"], 'name': 'TEST'}, aset.to_document())

    def test_init_with_id(self):
        aset = Set(name="TEST", values=["val1", "val2", "val3"])
        aset.id = '666'

        self.assertIsNotNone(aset)
        self.assertIsNotNone(aset.id)
        self.assertEqual('666', aset.id)
        self.assertEqual("TEST", aset.name)
        self.assertEqual(["val1", "val2", "val3"], aset.values)
        self.assertEqual({'_id': '666', 'values': ["val1", "val2", "val3"], 'name': 'TEST'}, aset.to_document())

    def test_from_document(self):
        aset1 = Set.from_document({'values': ["val1", "val2", "val3"], 'name': 'TEST'})
        self.assertIsNotNone(aset1)
        self.assertIsNone(aset1.id)
        self.assertEqual("TEST", aset1.name)
        self.assertEqual(["val1", "val2", "val3"], aset1.values)

        aset2 = Set.from_document({'_id': '666', 'values': ["val1", "val2", "val3"], 'name': 'TEST'})
        self.assertIsNotNone(aset2)
        self.assertIsNotNone(aset2.id)
        self.assertEqual('666', aset2.id)
        self.assertEqual("TEST", aset2.name)
        self.assertEqual(["val1", "val2", "val3"], aset2.values)

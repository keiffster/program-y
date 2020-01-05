import os
import os.path
import unittest

from programy.mappings.sets import SetCollection
from programy.storage.entities.store import Store


class MockSetCollection(object):

    def __init__(self):
        self.sets = {}

    def empty(self):
        self.sets.clear()

    def remove(self, name):
        self.sets.pop(name, None)

    def add_set(self, set_name, the_set, store):
        self.sets[set_name] = the_set


class SetStoreAsserts(unittest.TestCase):

    def assert_set_storage(self, store):
        store.empty()

        store.add_to_set("TESTSET1", "Val1")
        store.add_to_set("TESTSET1", "Val2")
        store.add_to_set("TESTSET1", "Val3")
        store.add_to_set("TESTSET2", "Val4")
        store.commit()

        set_collection = MockSetCollection()
        store.load_all(set_collection)
        self.assertEqual(2, len(set_collection.sets.keys()))
        self.assertTrue('TESTSET1' in set_collection.sets)
        self.assertTrue('VAL1' in set_collection.sets['TESTSET1'])
        self.assertTrue('VAL2' in set_collection.sets['TESTSET1'])
        self.assertTrue('VAL3' in set_collection.sets['TESTSET1'])
        self.assertTrue('TESTSET2' in set_collection.sets)
        self.assertTrue('VAL4' in set_collection.sets['TESTSET2'])

        self.assertTrue(store.remove_from_set("TESTSET1", "Val2"))
        self.assertFalse(store.remove_from_set("TESTSET1", "Val5"))
        self.assertTrue(store.remove_from_set("TESTSET2", "Val4"))
        self.assertFalse(store.remove_from_set("TESTSET4", "Val2"))
        store.commit()

        set_collection = MockSetCollection()
        store.load_all(set_collection)
        self.assertEqual(1, len(set_collection.sets.keys()))
        self.assertTrue('TESTSET1' in set_collection.sets)
        self.assertTrue('VAL1' in set_collection.sets['TESTSET1'])
        self.assertTrue('VAL3' in set_collection.sets['TESTSET1'])
        self.assertFalse('TESTSET2' in set_collection.sets)

    def assert_upload_from_text(self, store):
        store.empty ()

        store.upload_from_text('TESTSET', """
        VAL1
        VAL2
        VAL3
        VAL4
        """)

        set_collection = SetCollection()
        self.assertTrue(store.load(set_collection, 'TESTSET'))
        self.assertFalse(store.load(set_collection, 'TESTSET2'))
        self.assertTrue(set_collection.contains('TESTSET'))
        values = set_collection.set('TESTSET')
        self.assertTrue('VAL1' in values)
        self.assertTrue('VAL2' in values)
        self.assertTrue('VAL3' in values)
        self.assertTrue('VAL4' in values)

    def assert_upload_from_text_file(self, store):
        store.empty()

        store.upload_from_file(os.path.dirname(__file__) + os.sep + "data" + os.sep + "sets" + os.sep + "text" + os.sep + "testset.txt")

        set_collection = SetCollection()
        store.load(set_collection, 'TESTSET')
        self.assertTrue(set_collection.contains('TESTSET'))
        values = set_collection.set('TESTSET')
        self.assertTrue('VAL1' in values)
        self.assertTrue('VAL2' in values)
        self.assertTrue('VAL3' in values)
        self.assertTrue('VAL4' in values)

    def assert_upload_text_files_from_directory_no_subdir(self, store):
        store.empty ()

        store.upload_from_directory(os.path.dirname(__file__)+os.sep+"data"+os.sep+"sets"+os.sep+"text", subdir=False)

        set_collection = SetCollection()
        store.load(set_collection, 'TESTSET')
        self.assertTrue(set_collection.contains('TESTSET'))
        values = set_collection.set('TESTSET')
        self.assertTrue('VAL1' in values)
        self.assertTrue('VAL2' in values)
        self.assertTrue('VAL3' in values)
        self.assertTrue('VAL4' in values)

    def assert_upload_text_files_from_directory_with_subdir(self, store):
        store.empty ()

        store.upload_from_directory(os.path.dirname(__file__)+os.sep+"data"+os.sep+"sets"+os.sep+"text", subdir=True)

        set_collection = SetCollection()
        store.load_all(set_collection)

        self.assertTrue(set_collection.contains('TESTSET'))
        values = set_collection.set('TESTSET')
        self.assertTrue('VAL1' in values)
        self.assertTrue('VAL2' in values)
        self.assertTrue('VAL3' in values)
        self.assertTrue('VAL4' in values)

        self.assertTrue(set_collection.contains('TESTSET2'))
        values = set_collection.set('TESTSET2')
        self.assertTrue('VAL5' in values)
        self.assertTrue('VAL6' in values)
        self.assertTrue('VAL7' in values)
        self.assertTrue('VAL8' in values)

    def assert_upload_from_csv_file(self, store):
        store.empty()

        store.upload_from_file(os.path.dirname(__file__) + os.sep + "data" + os.sep + "sets" + os.sep + "csv" + os.sep + "testset.csv", fileformat=Store.CSV_FORMAT)

        set_collection = SetCollection()
        store.load(set_collection, 'TESTSET')
        self.assertTrue(set_collection.contains('TESTSET'))
        values = set_collection.set('TESTSET')
        self.assertTrue('VAL1' in values)
        self.assertTrue('VAL2' in values)
        self.assertTrue('VAL3' in values)
        self.assertTrue('VAL4' in values)

    def assert_upload_csv_files_from_directory_with_subdir(self, store):
        store.empty()

        store.upload_from_directory(os.path.dirname(__file__) + os.sep + "data" + os.sep + "sets" + os.sep + "csv", fileformat=Store.CSV_FORMAT)

        set_collection = SetCollection()
        store.load(set_collection, 'TESTSET')
        self.assertTrue(set_collection.contains('TESTSET'))
        values = set_collection.set('TESTSET')
        self.assertTrue('VAL1' in values)
        self.assertTrue('VAL2' in values)
        self.assertTrue('VAL3' in values)
        self.assertTrue('VAL4' in values)

        set_collection = SetCollection()
        store.load(set_collection, 'TESTSET2')
        self.assertTrue(set_collection.contains('TESTSET2'))
        values = set_collection.set('TESTSET2')
        self.assertEqual(4, len(values))
        self.assertTrue('VAL5' in values)
        self.assertTrue('VAL6' in values)
        self.assertTrue('VAL7' in values)
        self.assertTrue('VAL8' in values)

    def assert_empty_named(self, store):
        store.empty()

        store.add_to_set("TESTSET1", "Val1")
        store.add_to_set("TESTSET1", "Val2")
        store.add_to_set("TESTSET1", "Val3")
        store.add_to_set("TESTSET2", "Val4")
        store.commit()

        set_collection = MockSetCollection()
        store.load_all(set_collection)
        self.assertEqual(2, len(set_collection.sets.keys()))
        self.assertTrue('TESTSET1' in set_collection.sets)
        self.assertTrue('VAL1' in set_collection.sets['TESTSET1'])
        self.assertTrue('VAL2' in set_collection.sets['TESTSET1'])
        self.assertTrue('VAL3' in set_collection.sets['TESTSET1'])
        self.assertTrue('TESTSET2' in set_collection.sets)
        self.assertTrue('VAL4' in set_collection.sets['TESTSET2'])

        store.empty_named("TESTSET1")

        set_collection2 = MockSetCollection()
        store.load_all(set_collection2)
        self.assertEqual(1, len(set_collection2.sets.keys()))
        self.assertFalse('TESTSET1' in set_collection2.sets)
        self.assertTrue('TESTSET2' in set_collection2.sets)
        self.assertTrue('VAL4' in set_collection2.sets['TESTSET2'])

    def assert_add_to_set_duplicates(self, store):
        store.empty()

        store.add_to_set("TESTSET1", "Val1")
        store.add_to_set("TESTSET1", "Val1")
        store.commit()

        set_collection = MockSetCollection()
        store.load_all(set_collection)
        self.assertEqual(1, len(set_collection.sets.keys()))
        self.assertTrue('TESTSET1' in set_collection.sets)
        self.assertEqual(1, len(set_collection.sets['TESTSET1']))
        self.assertTrue('VAL1' in set_collection.sets['TESTSET1'])


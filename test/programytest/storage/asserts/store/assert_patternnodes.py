import os
import os.path
import unittest
from programy.parser.pattern.factory import PatternNodeFactory


class PatternNodesStoreAsserts(unittest.TestCase):

    def assert_load(self, store):
        store.empty()

        store.upload_from_file(os.path.dirname(__file__) + os.sep + "data" + os.sep + "nodes" + os.sep + "pattern_nodes.conf")

        collection = PatternNodeFactory()
        store.load(collection)

        self.assertEqual(12, len(collection.nodes))
        self.assertTrue(collection.exists("zeroormore"))

    def assert_load_exception(self, store):
        store.empty()

        store.upload_from_file(os.path.dirname(__file__) + os.sep + "data" + os.sep + "nodes" + os.sep + "pattern_nodes.conf")

        collection = PatternNodeFactory()
        store.load(collection)

        self.assertEqual(0, len(collection.nodes))
        self.assertFalse(collection.exists("zeroormore"))

    def assert_upload_from_file(self, store, verbose=False):
        store.empty()

        count, success = store.upload_from_file(os.path.dirname(__file__) + os.sep + "data" + os.sep + "nodes" + os.sep + "pattern_nodes.conf", verbose=verbose)
        self.assertEquals(17, count)
        self.assertEquals(12, success)

    def assert_upload_from_file_exception(self, store):
        store.empty()

        count, success = store.upload_from_file(os.path.dirname(__file__) + os.sep + "data" + os.sep + "nodes" + os.sep + "pattern_nodes.conf")
        self.assertEquals(0, count)
        self.assertEquals(0, success)

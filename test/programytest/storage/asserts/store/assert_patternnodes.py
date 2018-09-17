import unittest
import os
import os.path

from programy.parser.pattern.factory import PatternNodeFactory


class PatternNodesStoreAsserts(unittest.TestCase):

    def assert_upload_from_file(self, store):
        store.upload_from_file(os.path.dirname(__file__) + os.sep + "data" + os.sep + "nodes" + os.sep + "pattern_nodes.conf")

        collection = PatternNodeFactory()
        store.load(collection)

        self.assertEqual(12, len(collection.nodes))
        self.assertTrue(collection.exists("zeroormore"))
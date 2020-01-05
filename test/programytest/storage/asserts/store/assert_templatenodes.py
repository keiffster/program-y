import os
import os.path
import unittest

from programy.parser.template.factory import TemplateNodeFactory


class TemplateNodesStoreAsserts(unittest.TestCase):

    def assert_load(self, store):
        store.empty()

        store.upload_from_file(os.path.dirname(__file__) + os.sep + "data" + os.sep + "nodes" + os.sep + "template_nodes.conf")

        collection = TemplateNodeFactory()
        store.load(collection)

        self.assertEqual(64, len(collection.nodes))
        self.assertTrue(collection.exists("lowercase"))

    def assert_load_exception(self, store):
        store.empty()

        store.upload_from_file(os.path.dirname(__file__) + os.sep + "data" + os.sep + "nodes" + os.sep + "template_nodes.conf")

        collection = TemplateNodeFactory()
        store.load(collection)

        self.assertEqual(0, len(collection.nodes))
        self.assertFalse(collection.exists("lowercase"))

    def assert_upload_from_file(self, store, verbose=False):
        store.empty()

        count, success = store.upload_from_file(os.path.dirname(__file__) + os.sep + "data" + os.sep + "nodes" + os.sep + "template_nodes.conf", verbose=verbose)
        self.assertEquals(71, count)
        self.assertEquals(64, success)

    def assert_upload_from_file_exception(self, store):
        store.empty()

        count, success = store.upload_from_file(os.path.dirname(__file__) + os.sep + "data" + os.sep + "nodes" + os.sep + "template_nodes.conf")
        self.assertEquals(0, count)
        self.assertEquals(0, success)

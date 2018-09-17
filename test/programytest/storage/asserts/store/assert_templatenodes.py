import unittest
import os
import os.path

from programy.parser.template.factory import TemplateNodeFactory


class TemplateNodesStoreAsserts(unittest.TestCase):

    def assert_upload_from_file(self, store):
        store.upload_from_file(os.path.dirname(__file__) + os.sep + "data" + os.sep + "nodes" + os.sep + "template_nodes.conf")

        collection = TemplateNodeFactory()
        store.load(collection)

        self.assertEqual(64, len(collection.nodes))
        self.assertTrue(collection.exists("lowercase"))
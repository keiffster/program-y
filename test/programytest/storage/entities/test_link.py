import unittest

from programy.storage.entities.link import LinkStore

class LinkStoreTests(unittest.TestCase):

    def test_create_link(self):
        link_store = LinkStore()
        with self.assertRaises(NotImplementedError):
            link_store.create_link("primary_userid", "generated_key", "provided_key", expires=None)

import unittest
import unittest.mock

from programy.storage.entities.braintree import BraintreeStore


class BraintreeStoreTests(unittest.TestCase):

    def test_save_braintree(self):
        store = BraintreeStore()
        with self.assertRaises(NotImplementedError):
            client_context = unittest.mock.Mock()
            pattern_graph = unittest.mock.Mock()
            store.save_braintree(client_context, pattern_graph)
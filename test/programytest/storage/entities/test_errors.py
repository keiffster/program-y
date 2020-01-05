import unittest
import unittest.mock

from programy.storage.entities.errors import ErrorsStore


class ErrorsStoreTests(unittest.TestCase):

    def test_save_errors(self):
        store = ErrorsStore()
        with self.assertRaises(NotImplementedError):
            errors = unittest.mock.Mock()
            store.save_errors(errors)




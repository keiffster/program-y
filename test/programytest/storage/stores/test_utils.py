import unittest

from programy.storage.stores.utils import DAOUtils


class DAOUtilsTests(unittest.TestCase):

    def test_get_value_from_data(self):
        self.assertIsNone(DAOUtils.get_value_from_data({}, "key1"))
        self.assertIsNone(DAOUtils.get_value_from_data({"key1": "value1"}, "key2"))
        self.assertEqual("value1", DAOUtils.get_value_from_data({"key1": "value1"}, "key1"))

    def test_valid_id(self):
        self.assertEqual(DAOUtils.valid_id(None), DAOUtils.NOT_APPLIC)
        self.assertEqual(DAOUtils.valid_id(3), "3")

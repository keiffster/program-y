import unittest
import os
from programy.mappings.sets import SetCollection, SetLoader


class SetTests(unittest.TestCase):

    def test_loader_from_file(self):
        loader = SetLoader()
        self.assertIsNotNone(loader)

        the_set = loader.load_file_contents(os.path.dirname(__file__)+ "/test_files/sets/test_set.txt")
        self.assertIsNotNone(the_set)
        self.assertEqual(len(the_set), 17)

        self.assertIn("ALABAMA", the_set)
        self.assertEqual("Alabama", the_set['ALABAMA'])
        self.assertIn("ALASKA", the_set)
        self.assertIn("KANSAS", the_set)
        self.assertIn("KENTUCKY", the_set)
        self.assertNotIn("London", the_set)

    def test_loader_from_text(self):
        loader = SetLoader()
        self.assertIsNotNone(loader)

        the_set = loader.load_from_text("""
            Val1
            Val2
            Val3
            Val4
        """)
        self.assertIsNotNone(the_set)
        self.assertEqual(len(the_set), 4)

        self.assertIn("VAL1", the_set)
        self.assertEqual("Val1", the_set['VAL1'])
        self.assertIn("VAL2", the_set)
        self.assertIn("VAL3", the_set)
        self.assertIn("VAL4", the_set)

    def test_collection(self):
        loader = SetLoader()
        self.assertIsNotNone(loader)

        collection = SetCollection()
        self.assertIsNotNone(collection)

        collection._sets = loader.load_from_text("""
            Val1
            Val2
            Val3
            Val4
        """)

        self.assertIsNotNone(collection._sets)
        self.assertEqual(len(collection._sets), 4)

        self.assertTrue(collection.contains('VAL1'))
        self.assertTrue(collection.contains('VAL2'))
        self.assertTrue(collection.contains('VAL3'))
        self.assertTrue(collection.contains('VAL4'))
        self.assertFalse(collection.contains('VAL5'))
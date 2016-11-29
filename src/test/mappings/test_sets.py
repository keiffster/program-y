import unittest

from programy.mappings.sets import SetCollection, SetLoader


class SetTests(unittest.TestCase):

    def test_loader_from_file(self):
        loader = SetLoader()
        self.assertIsNotNone(loader)

        the_set = loader.load_file_contents("/Users/keithsterling/Documents/Development/Python/Projects/AIML/program-y/src/test/mappings/test_files/sets/test_set.txt")
        self.assertIsNotNone(the_set)

        self.assertIn("ALABAMA", the_set)
        self.assertIn("ALASKA", the_set)
        self.assertIn("KANSAS", the_set)
        self.assertIn("KENTUCKY", the_set)
        self.assertNotIn("London", the_set)

    def test_loader_from_text(self):
        loader = SetLoader()
        self.assertIsNotNone(loader)

        the_set = loader.load_from_text("""
            VAL1
            VAL2
            VAL3
            VAL4
        """)
        self.assertIsNotNone(the_set)
        self.assertEqual(len(the_set), 4)
        self.assertIn("VAL1", the_set)
        self.assertIn("VAL2", the_set)
        self.assertIn("VAL3", the_set)
        self.assertIn("VAL4", the_set)

    def test_collection(self):
        loader = SetLoader()
        self.assertIsNotNone(loader)

        collection = SetCollection()
        self.assertIsNotNone(collection)

        collection._sets = loader.load_from_text("""
            VAL1
            VAL2
            VAL3
            VAL4
        """)

        self.assertIsNotNone(collection._sets)
        self.assertEqual(len(collection._sets), 4)

        self.assertTrue(collection.contains('VAL1'))
        self.assertTrue(collection.contains('VAL2'))
        self.assertTrue(collection.contains('VAL3'))
        self.assertTrue(collection.contains('VAL4'))
        self.assertFalse(collection.contains('VAL5'))
import unittest

from programy.mappings.sets import SetCollection, SetLoader


class SetTests(unittest.TestCase):

    def test_loader(self):
        loader = SetLoader(SetCollection())
        self.assertIsNotNone(loader)

        the_set = loader.load_from_text("""
            val1
            val2
            val3
            val4
        """)
        self.assertIsNotNone(the_set)
        self.assertEqual(len(the_set), 4)
        self.assertIn("val1", the_set)
        self.assertIn("val2", the_set)
        self.assertIn("val3", the_set)
        self.assertIn("val4", the_set)

    def test_collection(self):
        loader = SetLoader(SetCollection())
        self.assertIsNotNone(loader)

        collection = SetCollection()
        self.assertIsNotNone(collection)

        collection._sets = loader.load_from_text("""
            val1
            val2
            val3
            val4
        """)

        self.assertTrue(collection.contains('val1'))
        self.assertTrue(collection.contains('val2'))
        self.assertTrue(collection.contains('val3'))
        self.assertTrue(collection.contains('val4'))
        self.assertFalse(collection.contains('val15'))
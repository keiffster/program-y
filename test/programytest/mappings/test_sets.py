import unittest
import os
from programy.mappings.sets import SetCollection, SetLoader

class SetTests(unittest.TestCase):

    def test_loader_from_file(self):
        loader = SetLoader()
        self.assertIsNotNone(loader)

        the_set = loader.load_file_contents("testid", os.path.dirname(__file__)+  os.sep + "test_files" + os.sep + "sets" + os.sep + "test_set.txt")
        self.assertIsNotNone(the_set)
        self.assertEqual(len(the_set), 451)

        self.assertIn("AMBER", the_set)
        self.assertEqual([["Amber"]], the_set['AMBER'])

        self.assertIn("RED", the_set)
        self.assertEqual([['Red', 'brown'], ['Red', 'Orange'], ['Red', 'violet'], ['Red']], the_set["RED"])

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
        self.assertEqual([["Val1"]], the_set['VAL1'])
        self.assertIn("VAL2", the_set)
        self.assertIn("VAL3", the_set)
        self.assertIn("VAL4", the_set)

    def test_loader_from_text_multi_word(self):
        loader = SetLoader()
        self.assertIsNotNone(loader)

        the_set = loader.load_from_text("""
            Val11 Val12
            Val2
            Val31 Val32
            Val4
        """)
        self.assertIsNotNone(the_set)
        self.assertEqual(len(the_set), 4)

        self.assertIn("VAL11", the_set)
        self.assertEqual([["Val11", "Val12"]], the_set['VAL11'])
        self.assertIn("VAL2", the_set)
        self.assertIn("VAL31", the_set)
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
import unittest
import os
from programy.mappings.maps import MapCollection, MapLoader


class MapTests(unittest.TestCase):

    def test_loader_from_file(self):
        loader = MapLoader()
        self.assertIsNotNone(loader)

        map = loader.load_file_contents(os.path.dirname(__file__)+ "/test_files/maps/test_map.txt")

        self.assertIsNotNone(map)
        self.assertEqual(len(map.keys()), 12)
        self.assertEqual(map['ALABAMA'], 'Montgomery')
        self.assertEqual(map['COLORADO'], 'Denver')
        self.assertEqual(map['HAWAII'], 'Honolulu')

    def test_loader_from_text(self):
        loader = MapLoader()
        self.assertIsNotNone(loader)

        map = loader.load_from_text("""
        KEY1:VAL1
        KEY2:VAL2
        KEY3:VAL3
        KEY4:VAL4
        """)
        self.assertIsNotNone(map)
        self.assertEqual(len(map.keys()), 4)
        self.assertEqual(map['KEY1'], 'VAL1')
        self.assertEqual(map['KEY2'], 'VAL2')
        self.assertEqual(map['KEY3'], 'VAL3')
        self.assertEqual(map['KEY4'], 'VAL4')

    def test_collection(self):
        collection = MapCollection()
        self.assertIsNotNone(collection)

        loader = MapLoader()
        self.assertIsNotNone(loader)

        collection._maps = loader.load_from_text("""
            KEY1:VAL1
            KEY2:VAL2
            KEY3:VAL3
            KEY4:VAL4
        """)
        self.assertIsNotNone(collection._maps)
        self.assertTrue(collection.contains('KEY1'))
        self.assertEqual(collection.map('KEY1'), 'VAL1')
        self.assertTrue(collection.contains('KEY2'))
        self.assertEqual(collection.map('KEY2'), 'VAL2')
        self.assertTrue(collection.contains('KEY3'))
        self.assertEqual(collection.map('KEY3'), 'VAL3')
        self.assertTrue(collection.contains('KEY4'))
        self.assertEqual(collection.map('KEY4'), 'VAL4')
        self.assertFalse(collection.contains('KEY5'))

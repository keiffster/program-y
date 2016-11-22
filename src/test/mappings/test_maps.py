import unittest

from programy.mappings.maps import MapCollection, MapLoader


class MapTests(unittest.TestCase):

    def test_loader(self):
        loader = MapLoader()
        self.assertIsNotNone(loader)

        map = loader.load_from_text("""
        key1:val1
        key2:val2
        key3:val3
        key4:val4
        """)
        self.assertIsNotNone(map)
        self.assertEqual(len(map.keys()), 4)
        self.assertEqual(map['key1'], 'val1')
        self.assertEqual(map['key2'], 'val2')
        self.assertEqual(map['key3'], 'val3')
        self.assertEqual(map['key4'], 'val4')

    def test_collection(self):
        collection = MapCollection()
        self.assertIsNotNone(collection)

        loader = MapLoader()
        self.assertIsNotNone(loader)

        collection._maps = loader.load_from_text("""
            key1:val1
            key2:val2
            key3:val3
            key4:val4
        """)
        self.assertIsNotNone(collection._maps)
        self.assertTrue(collection.contains('key1'))
        self.assertEqual(collection.map('key1'), 'val1')
        self.assertTrue(collection.contains('key2'))
        self.assertEqual(collection.map('key2'), 'val2')
        self.assertTrue(collection.contains('key3'))
        self.assertEqual(collection.map('key3'), 'val3')
        self.assertTrue(collection.contains('key4'))
        self.assertEqual(collection.map('key4'), 'val4')
        self.assertFalse(collection.contains('key5'))

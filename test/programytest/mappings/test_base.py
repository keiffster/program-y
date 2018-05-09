import unittest
import os

from programy.mappings.base import SingleStringCollection
from programy.mappings.base import DoubleStringCharSplitCollection
from programy.mappings.base import DoubleStringPatternSplitCollection
from programy.mappings.base import TripleStringCollection

class MockSingleStringCollection(SingleStringCollection):

    def __init__(self, process_splits_success=False):
        SingleStringCollection.__init__(self)
        self._process_splits_success = process_splits_success

    def process_splits(self, splits, id=None):
        if self._process_splits_success is True:
            return super(TestSingleStringCollection, self).process_splits(splits, id)
        else:
            return False


class MockDoubleStringCharSplitCollection(DoubleStringCharSplitCollection):

    def __init__(self, process_splits_success=True):
        DoubleStringCharSplitCollection.__init__(self)
        self._process_splits_success = process_splits_success

    def process_splits(self, splits, id=None):
        if self._process_splits_success is True:
            return super(MockDoubleStringCharSplitCollection, self).process_splits(splits, id)
        else:
            return False


class MockDoubleStringPatternSplitCollection(DoubleStringPatternSplitCollection):

    def __init__(self, process_splits_success=True):
        DoubleStringPatternSplitCollection.__init__(self)
        self._process_splits_success = process_splits_success

    def process_splits(self, splits, id=None):
        if self._process_splits_success is True:
            return super(MockDoubleStringPatternSplitCollection, self).process_splits(splits, id)
        else:
            return False


class MockTripleStringCollection(TripleStringCollection):

    def __init__(self, process_splits_success=True):
        TripleStringCollection.__init__(self)
        self._process_splits_success = process_splits_success

    def process_splits(self, splits, id=None):
        if self._process_splits_success is True:
            return super(MockTripleStringCollection, self).process_splits(splits, id)
        else:
            return False


class TestSingleStringCollection(unittest.TestCase):

    def test_single_strings_from_text(self):
        singles = SingleStringCollection ()
        self.assertIsNotNone(singles)

        count = singles.load_from_text("""
        val1
        val2
        val3
        """)
        self.assertEqual(count, 3)
        self.assertIsNotNone(singles.strings)
        self.assertEqual(3, len(singles.strings))
        self.assertIn("val1", singles.strings)
        self.assertIn("val2", singles.strings)
        self.assertIn("val3", singles.strings)

    def test_single_strings_from_file(self):
        singles = SingleStringCollection ()
        self.assertIsNotNone(singles)

        count = singles.load_from_filename(os.path.dirname(__file__) +  os.sep + "test_files/singles.txt")
        self.assertEqual(count, 3)
        self.assertIn("val1", singles.strings)
        self.assertIn("val2", singles.strings)
        self.assertIn("val3", singles.strings)

    def test_single_strings_fail(self):
        singles = MockSingleStringCollection (process_splits_success=False)
        self.assertIsNotNone(singles)

        count = singles.load_from_text("""
        val1
        val2
        val3
        """)
        self.assertEqual(count, 0)


class TestDoubleStringCharSplitCollection(unittest.TestCase):

    def test_double_strings_from_text(self):
        doubles = DoubleStringCharSplitCollection ()
        self.assertIsNotNone(doubles)

        count = doubles.load_from_text("""
        key1,val1
        key2,val2
        key3,val3,val4
        """)
        self.assertEqual(count, 3)

        self.assertTrue(doubles.has_key("key1"))
        self.assertEqual(doubles.value("key1"), "val1")

        self.assertTrue(doubles.has_key("key2"))
        self.assertEqual(doubles.value("key2"), "val2")

        self.assertTrue(doubles.has_key("key3"))
        self.assertEqual(doubles.value("key3"), "val3,val4")

        self.assertFalse(doubles.has_key("key4"))
        doubles.add_value("key4", "val5")
        self.assertTrue(doubles.has_key("key4"))
        self.assertEqual(doubles.value("key4"), "val5")
        doubles.set_value("key4", "val6")
        self.assertEqual(doubles.value("key4"), "val6")

    def test_double_strings_from_file(self):
        doubles = DoubleStringCharSplitCollection ()
        self.assertIsNotNone(doubles)

        count = doubles.load_from_filename(os.path.dirname(__file__) + os.sep + "test_files/doubles.txt")
        self.assertEqual(count, 3)

        self.assertTrue(doubles.has_key("key1"))
        self.assertEqual(doubles.value("key1"), "val1")

        self.assertTrue(doubles.has_key("key2"))
        self.assertEqual(doubles.value("key2"), "val2")

        self.assertTrue(doubles.has_key("key3"))
        self.assertEqual(doubles.value("key3"), "val3,val4")


    def test_double_strings_fail(self):
        doubles = MockDoubleStringCharSplitCollection (process_splits_success=False)
        self.assertIsNotNone(doubles)

        count = doubles.load_from_text("""
        key1,val1
        key2,val2
        key3,val3
        """)
        self.assertEqual(count, 0)

class TestDoubleStringPatternSplitCollection(unittest.TestCase):

    def test_double_strings_line_split(self):
        doubles = DoubleStringPatternSplitCollection ()

        splits = doubles.split_line('"Key1","Val1"')
        self.assertIsNotNone(splits)
        self.assertEqual(2, len(splits))
        self.assertEqual("Key1", splits[0])
        self.assertEqual("Val1", splits[1])

        splits = doubles.split_line('')
        self.assertIsNone(splits)

    def test_double_strings_from_text(self):
        doubles = DoubleStringPatternSplitCollection ()
        self.assertIsNotNone(doubles)

        count = doubles.load_from_text("""
        "key1","val1"
        "key2","val2"
        "key3","val3,val4"
        """)
        self.assertEqual(count, 3)

        self.assertTrue(doubles.has_key("key1"))
        #self.assertEqual(doubles.value("key1"), "(^key1|key1|key1$)")

        self.assertTrue(doubles.has_key("key2"))
        #self.assertEqual(doubles.value("key2"), "(^key2|key2|key2$)")

        self.assertTrue(doubles.has_key("key3"))
        #self.assertEqual(doubles.value("key3"), "(^key3|key3|key3$)")

        self.assertFalse(doubles.has_key("key4"))
        self.assertIsNone(doubles.value("keyX"))


    def test_double_strings_from_file(self):
        doubles = DoubleStringPatternSplitCollection ()
        self.assertIsNotNone(doubles)

        count = doubles.load_from_filename(os.path.dirname(__file__) +  os.sep + "test_files" + os.sep + "doubles_pattern.txt")
        self.assertEqual(count, 3)

        self.assertTrue(doubles.has_key("key1"))
        #self.assertEqual(doubles.value("key1"), "(^key1|key1|key1$)")

        self.assertTrue(doubles.has_key("key2"))
        #self.assertEqual(doubles.value("key2"), "(^key2|key2|key2$)")

        self.assertTrue(doubles.has_key("key3"))
        #self.assertEqual(doubles.value("key3"), "(^key3|key3|key3$)")

    def test_double_strings_fail(self):
        doubles = MockDoubleStringPatternSplitCollection (process_splits_success=False)
        self.assertIsNotNone(doubles)

        count = doubles.load_from_text("""
        "key1","val1"
        "key2","val2"
        "key3","val3,val4"
        """)
        self.assertEqual(count, 0)


class TestTripleStringCollection(unittest.TestCase):

    def test_triple_strings_from_text(self):
        triples = TripleStringCollection ()
        self.assertIsNotNone(triples)
        self.assertEqual(".*", triples.get_split_pattern())

        count = triples.load_from_text("""
        key1:val11:val12
        key2:val21:val22
        key3:val31:val32:val33
        """)
        self.assertEqual(count, 3)

        self.assertTrue(triples.has_primary("key1"))
        self.assertTrue(triples.has_primary("key2"))
        self.assertTrue(triples.has_primary("key3"))

        self.assertTrue(triples.has_secondary("key1", "val11"))
        self.assertTrue(triples.has_secondary("key2", "val21"))
        self.assertTrue(triples.has_secondary("key3", "val31"))

        self.assertEqual(triples.value("key1", "val11"), "val12")
        self.assertEqual(triples.value("key2", "val21"), "val22")
        self.assertEqual(triples.value("key3", "val31"), "val32:val33")

        self.assertIsNone(triples.value("keyX", "val31X"))
        self.assertIsNone(triples.value("key3", "val31X"))

        self.assertTrue(triples.has_primary("key1"))
        self.assertFalse(triples.has_primary("keyX"))
        self.assertTrue(triples.has_secondary("key1", "val11"))
        self.assertFalse(triples.has_secondary("key1", "val1X"))
        self.assertFalse(triples.has_secondary("keyX", "val1X"))


    def test_triple_strings_from_file(self):
        triples = TripleStringCollection ()
        self.assertIsNotNone(triples)

        count = triples.load_from_filename(os.path.dirname(__file__) +  os.sep + "test_files" + os.sep + "triples.txt")
        self.assertEqual(count, 3)

        self.assertTrue(triples.has_primary("key1"))
        self.assertTrue(triples.has_primary("key2"))
        self.assertTrue(triples.has_primary("key3"))

        self.assertTrue(triples.has_secondary("key1", "val11"))
        self.assertTrue(triples.has_secondary("key2", "val21"))
        self.assertTrue(triples.has_secondary("key3", "val31"))

        self.assertEqual(triples.value("key1", "val11"), "val12")
        self.assertEqual(triples.value("key2", "val21"), "val22")
        self.assertEqual(triples.value("key3", "val31"), "val32:val33")

    def test_triple_strings_fail(self):
        triples = MockTripleStringCollection (process_splits_success=False)
        self.assertIsNotNone(triples)

        count = triples.load_from_text("""
        key1:val11:val12
        key2:val21:val22
        key3:val31:val32
        """)
        self.assertEqual(count, 0)

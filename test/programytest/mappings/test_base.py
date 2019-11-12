import unittest
import re
from programy.mappings.base import DoubleStringCharSplitCollection
from programy.mappings.base import DoubleStringPatternSplitCollection
from programy.mappings.base import SingleStringCollection


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

        singles.empty()
        self.assertEqual(0, len(singles.strings))


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

        doubles.empty()
        self.assertEqual(0, len(doubles.pairs))


class TestDoubleStringPatternSplitCollection(unittest.TestCase):

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
        self.assertEqual([re.compile('(^key1|key1|key1$)', re.IGNORECASE), 'VAL1'], doubles.value("key1"))

        self.assertTrue(doubles.has_key("key2"))
        self.assertEqual([re.compile('(^key2|key2|key2$)', re.IGNORECASE), 'VAL2'], doubles.value("key2"))

        self.assertTrue(doubles.has_key("key3"))
        self.assertEqual([re.compile('(^key3|key3|key3$)', re.IGNORECASE), 'VAL3,VAL4'], doubles.value("key3"))

        self.assertFalse(doubles.has_key("key4"))
        self.assertEqual(None, doubles.value("key4"))

        doubles.empty()
        self.assertEqual(0, len(doubles.pairs))

    def test_replace_by_pattern(self):
        doubles = DoubleStringPatternSplitCollection()
        self.assertIsNotNone(doubles)

        count = doubles.load_from_text("""
        "key1","val1"
        "key2","val2"
        "key3","val3,val4"
        "key5","val5"
        "key6","val6."
        """)

        self.assertEquals("HELLO. VAL5", doubles.replace_by_pattern("HELLO. KEY5"))
        self.assertEquals("HELLO VAL1", doubles.replace_by_pattern("HELLO KEY1"))
        self.assertEquals("VAL2 HELLO VAL2", doubles.replace_by_pattern("KEY2 HELLO KEY2"))
        self.assertEquals("HELLO VAL3,VAL4", doubles.replace_by_pattern("HELLO KEY3"))
        self.assertEquals("HELLO VAL6. HI", doubles.replace_by_pattern("HELLO KEY6 HI"))

    def test_replace_bad_regex(self):
        doubles = DoubleStringPatternSplitCollection()
        self.assertIsNotNone(doubles)

        count = doubles.load_from_text("""
        "key1","val1"
        """)

        doubles._pairs["KEY2"] = "{)("
        self.assertEquals("HELLO KEY2", doubles.replace_by_pattern("HELLO KEY2"))

    def test_match_case(self):
        doubles = DoubleStringPatternSplitCollection()

        self.assertEquals("equal", doubles.match_case("Equal", "EQUAL"))
        self.assertEquals("EQUAL", doubles.match_case("EQUAL", "equal"))
        self.assertEquals("equals", doubles.match_case("Equal", "Equals"))
        self.assertEquals("EQUALS", doubles.match_case("EQUal", "Equals"))

    def test_split_line_by_pattern(self):
        doubles = DoubleStringPatternSplitCollection()

        self.assertEquals(["KEY1", "VAL1"], doubles.split_line_by_pattern('"KEY1","VAL1"', DoubleStringPatternSplitCollection.RE_OF_SPLIT_PATTERN))

    def test_split_line_by_bad_pattern(self):
        doubles = DoubleStringPatternSplitCollection()

        self.assertEquals(None, doubles.split_line_by_pattern('"KEY1", "VAL1"',
                                                                          re.compile('\"(.*?)\",\"(.*?)\"')))
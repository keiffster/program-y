import unittest

from programy.mappings.base import SingleStringCollection, DoubleStringCharSplitCollection, TripleStringCollection

class TestDoubleStringCollection(DoubleStringCharSplitCollection):
    def __init__(self):
        DoubleStringCharSplitCollection.__init__(self)

    def split_line(self, line):
        return self.split_line_by_char(line)


class TestTripleStringCollection(TripleStringCollection):
    def __init__(self):
        TripleStringCollection.__init__(self)

    def split_line(self, line):
        return self.split_line_by_char(line)


class BaseTests(unittest.TestCase):

    def test_single_strings(self):
        singles = SingleStringCollection ()
        self.assertIsNotNone(singles)

        count = singles.load_from_text("""
        val1
        val2
        val3
        """)
        self.assertEqual(count, 3)
        self.assertIn("val1", singles.strings)
        self.assertIn("val2", singles.strings)
        self.assertIn("val3", singles.strings)

    def test_double_strings(self):
        doubles = TestDoubleStringCollection ()
        self.assertIsNotNone(doubles)

        count = doubles.load_from_text("""
        key1,val1
        key2,val2
        key3,val3
        """)
        self.assertEqual(count, 3)

        self.assertTrue(doubles.has_key("key1"))
        self.assertEqual(doubles.value("key1"), "val1")

        self.assertTrue(doubles.has_key("key2"))
        self.assertEqual(doubles.value("key2"), "val2")

        self.assertTrue(doubles.has_key("key3"))
        self.assertEqual(doubles.value("key3"), "val3")

    def test_triple_strings(self):
        triples = TestTripleStringCollection ()
        self.assertIsNotNone(triples)

        count = triples.load_from_text("""
        key1:val11:val12
        key2:val21:val22
        key3:val31:val32
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
        self.assertEqual(triples.value("key3", "val31"), "val32")

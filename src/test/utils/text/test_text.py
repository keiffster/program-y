import unittest
from programy.utils.text.text import TextUtils

#############################################################################
#

class TextUtilsTests(unittest.TestCase):

    def test_get_tabs(self):
        tabs = TextUtils.get_tabs(0)
        self.assertEqual(tabs, "")

        tabs = TextUtils.get_tabs(1, tabs="\t")
        self.assertEqual(tabs, "\t")

        tabs = TextUtils.get_tabs(5, tabs="\t")
        self.assertEqual(tabs, "\t\t\t\t\t")

    def test_strip_whitespace(self):
        self.assertEquals("", TextUtils.strip_whitespace(""))
        self.assertEquals("", TextUtils.strip_whitespace(" "))
        self.assertEquals("", TextUtils.strip_whitespace("\t"))
        self.assertEquals("", TextUtils.strip_whitespace("\n"))
        self.assertEquals("", TextUtils.strip_whitespace("\r"))
        self.assertEquals("", TextUtils.strip_whitespace("\r\t\n"))
        self.assertEquals("test", TextUtils.strip_whitespace("\r\t\ntest\r\t\n"))
        self.assertEquals("test test", TextUtils.strip_whitespace("\r\t\ntest test\r\t\n"))
        self.assertEquals("test test", TextUtils.strip_whitespace("\r\t\ntest\n\r\ttest\r\t\n"))

    def test_strip_all_whitespace(self):
        self.assertEquals("", TextUtils.strip_all_whitespace(""))
        self.assertEquals("", TextUtils.strip_all_whitespace(" "))
        self.assertEquals("", TextUtils.strip_all_whitespace("\t"))
        self.assertEquals("", TextUtils.strip_all_whitespace("\n"))
        self.assertEquals("", TextUtils.strip_all_whitespace("\r"))
        self.assertEquals("", TextUtils.strip_all_whitespace("\r\t\n"))
        self.assertEquals("test", TextUtils.strip_all_whitespace("\r\t\ntest\r\t\n"))
        self.assertEquals("testtest", TextUtils.strip_all_whitespace("\r\t\ntest test\r\t\n"))
        self.assertEquals("testtest", TextUtils.strip_all_whitespace("\r\t\ntest\n\r\ttest\r\t\n"))



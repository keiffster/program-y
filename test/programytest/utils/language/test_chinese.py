import unittest

from programy.utils.language.chinese import ChineseLanguage

#############################################################################
#

class ChineseTests(unittest.TestCase):

    def test_is_language(self):
        self.assertFalse(ChineseLanguage.is_language(""))
        self.assertFalse(ChineseLanguage.is_language("H"))
        self.assertTrue(ChineseLanguage.is_language("你"))

    def test_split_langauge(self):
        self.assertEqual([], ChineseLanguage.split_language(""))
        self.assertEqual(['X'], ChineseLanguage.split_language("X"))
        self.assertEqual(['你'], ChineseLanguage.split_language("你"))
        self.assertEqual(['你', '好'], ChineseLanguage.split_language("你好"))
        self.assertEqual(['X', '你', '好'], ChineseLanguage.split_language("X你好"))
        self.assertEqual(['X', '你', '好', 'Y'], ChineseLanguage.split_language("X你好Y"))

    def test_split_unicode(self):
        self.assertEqual([], ChineseLanguage.split_unicode(""))
        self.assertEqual(['X'], ChineseLanguage.split_unicode("X"))
        self.assertEqual(['你'], ChineseLanguage.split_unicode("你"))
        self.assertEqual(['你', '好'], ChineseLanguage.split_unicode("你好"))
        self.assertEqual(['X', '你', '好'], ChineseLanguage.split_unicode("X你好"))
        self.assertEqual(['X', '你', '好', 'Y'], ChineseLanguage.split_unicode("X你好Y"))

    def test_split_with_spaces(self):
        self.assertEqual('', ChineseLanguage.split_with_spaces([]))
        self.assertEqual('X', ChineseLanguage.split_with_spaces(['X']))
        self.assertEqual('你', ChineseLanguage.split_with_spaces(['你']))
        self.assertEqual('你  好', ChineseLanguage.split_with_spaces(['你', '好']))
        self.assertEqual('X  你  好', ChineseLanguage.split_with_spaces(['X', '你', '好']))
        self.assertEqual('X  你  好  Y', ChineseLanguage.split_with_spaces(['X', '你', '好', 'Y']))

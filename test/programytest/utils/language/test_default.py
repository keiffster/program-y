import unittest

from programy.utils.language.default import DefaultLangauge


#############################################################################
#

class DefaultTests(unittest.TestCase):

    def test_split_into_sentences(self):
        sentences = DefaultLangauge.split_into_sentences("")
        self.assertEqual([], sentences)

        sentences = DefaultLangauge.split_into_sentences("Hello")
        self.assertEqual(["Hello"], sentences)

        sentences = DefaultLangauge.split_into_sentences("Hello World")
        self.assertEqual(["Hello World"], sentences)

        sentences = DefaultLangauge.split_into_sentences("Hello, World")
        self.assertEqual(["Hello, World"], sentences)

        sentences = DefaultLangauge.split_into_sentences("Hello, World!")
        self.assertEqual(["Hello, World"], sentences)

        sentences = DefaultLangauge.split_into_sentences("Hello. World")
        self.assertEqual(["Hello", "World"], sentences)

        sentences = DefaultLangauge.split_into_sentences("Hello? World")
        self.assertEqual(["Hello", "World"], sentences)

        sentences = DefaultLangauge.split_into_sentences("Hello. World.?!")
        self.assertEqual(["Hello", "World"], sentences)

        sentences = DefaultLangauge.split_into_sentences("!Hello. World")
        self.assertEqual(["Hello", "World"], sentences)

        sentences = DefaultLangauge.split_into_sentences("半宽韩文字母")
        self.assertEqual(["半宽韩文字母"], sentences)

        sentences = DefaultLangauge.split_into_sentences("半宽韩文字母. 半宽平假名")
        self.assertEqual(["半宽韩文字母", "半宽平假名"], sentences)

    def test_split_into_words(self):
        words = DefaultLangauge.split_into_words("")
        self.assertEqual([], words)

        words = DefaultLangauge.split_into_words("Hello")
        self.assertEqual(["Hello"], words)

        words = DefaultLangauge.split_into_words("Hello World")
        self.assertEqual(["Hello", "World"], words)

        words = DefaultLangauge.split_into_words("  Hello    World   ")
        self.assertEqual(["Hello", "World"], words)
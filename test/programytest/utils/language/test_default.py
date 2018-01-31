import unittest

from programy.utils.language.default import DefaultLangauge


#############################################################################
#

class DefaultTests(unittest.TestCase):

    def test_split_into_sentences(self):
        sentences = DefaultLangauge.split_into_sentences("")
        self.assertEquals([], sentences)

        sentences = DefaultLangauge.split_into_sentences("Hello")
        self.assertEquals(["Hello"], sentences)

        sentences = DefaultLangauge.split_into_sentences("Hello World")
        self.assertEquals(["Hello World"], sentences)

        sentences = DefaultLangauge.split_into_sentences("Hello, World")
        self.assertEquals(["Hello, World"], sentences)

        sentences = DefaultLangauge.split_into_sentences("Hello, World!")
        self.assertEquals(["Hello, World"], sentences)

        sentences = DefaultLangauge.split_into_sentences("Hello. World")
        self.assertEquals(["Hello", "World"], sentences)

        sentences = DefaultLangauge.split_into_sentences("Hello? World")
        self.assertEquals(["Hello", "World"], sentences)

        sentences = DefaultLangauge.split_into_sentences("Hello. World.?!")
        self.assertEquals(["Hello", "World"], sentences)

        sentences = DefaultLangauge.split_into_sentences("!Hello. World")
        self.assertEquals(["Hello", "World"], sentences)

        sentences = DefaultLangauge.split_into_sentences("半宽韩文字母")
        self.assertEquals(["半宽韩文字母"], sentences)

        sentences = DefaultLangauge.split_into_sentences("半宽韩文字母. 半宽平假名")
        self.assertEquals(["半宽韩文字母", "半宽平假名"], sentences)

    def test_split_into_words(self):
        words = DefaultLangauge.split_into_words("")
        self.assertEquals([], words)

        words = DefaultLangauge.split_into_words("Hello")
        self.assertEquals(["Hello"], words)

        words = DefaultLangauge.split_into_words("Hello World")
        self.assertEquals(["Hello", "World"], words)

        words = DefaultLangauge.split_into_words("  Hello    World   ")
        self.assertEquals(["Hello", "World"], words)
import unittest

from programy.nlp.stemming import Stemmer

import programytest.externals as Externals


class StemmerTests(unittest.TestCase):

    def test_stem_default(self):

        self.assertEquals("troubl", Stemmer.stem("trouble"))
        self.assertEquals("troubl", Stemmer.stem("troubled"))
        self.assertEquals("troubl", Stemmer.stem("troubles"))
        self.assertEquals("troubl", Stemmer.stem("troubling"))
        self.assertEquals("", Stemmer.stem(""))

    def test_stem_porter(self):

        self.assertEquals("troubl", Stemmer.stem("trouble", stemmer="porter"))
        self.assertEquals("troubl", Stemmer.stem("troubled", stemmer="porter"))
        self.assertEquals("troubl", Stemmer.stem("troubles", stemmer="porter"))
        self.assertEquals("troubl", Stemmer.stem("troubling", stemmer="porter"))

    def test_stem_lancaster(self):

        self.assertEquals("troubl", Stemmer.stem("trouble", stemmer="lancaster"))
        self.assertEquals("troubl", Stemmer.stem("troubled", stemmer="lancaster"))
        self.assertEquals("troubl", Stemmer.stem("troubles", stemmer="lancaster"))
        self.assertEquals("troubl", Stemmer.stem("troubling", stemmer="lancaster"))

    def test_stem_regex(self):

        self.assertEquals("troubl", Stemmer.stem("trouble", stemmer="regex", regexp="ing$|s$|e$|able$|ed$|es$", min=0))
        self.assertEquals("troubl", Stemmer.stem("troubled", stemmer="regex", regexp="ing$|s$|e$|able$|ed$|es$", min=0))
        self.assertEquals("troubl", Stemmer.stem("troubles", stemmer="regex", regexp="ing$|s$|e$|able$|ed$|es$", min=0))
        self.assertEquals("troubl", Stemmer.stem("troubling", stemmer="regex", regexp="ing$|s$|e$|able$|ed$|es$", min=0))

    def test_stem_isri(self):

        self.assertEquals("trouble", Stemmer.stem("trouble", stemmer="isri"))
        self.assertEquals("troubled", Stemmer.stem("troubled", stemmer="isri"))
        self.assertEquals("troubles", Stemmer.stem("troubles", stemmer="isri"))
        self.assertEquals("troubling", Stemmer.stem("troubling", stemmer="isri"))

    def test_stem_snowball(self):

        self.assertEquals("troubl", Stemmer.stem("trouble", stemmer="snowball", language="english"))
        self.assertEquals("troubl", Stemmer.stem("troubled", stemmer="snowball", language="english"))
        self.assertEquals("troubl", Stemmer.stem("troubles", stemmer="snowball", language="english"))
        self.assertEquals("troubl", Stemmer.stem("troubling", stemmer="snowball", language="english"))

    @unittest.skipIf(Externals.rslp_stemming is False, Externals.rslp_stemming_disabled)
    def test_stem_rslp(self):

        self.assertEquals("troubl", Stemmer.stem("trouble", stemmer="rslp"))
        self.assertEquals("troubl", Stemmer.stem("troubled", stemmer="rslp"))
        self.assertEquals("troubl", Stemmer.stem("troubles", stemmer="rslp"))
        self.assertEquals("troubl", Stemmer.stem("troubling", stemmer="rslp"))

    def test_stem_cistem(self):

        self.assertEquals("speicherbehalt", Stemmer.stem("Speicherbehältern", stemmer="cistem", case_insensitive=False))

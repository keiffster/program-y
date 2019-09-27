import unittest

from programy.nlp.stemming import Stemmer

import programytest.externals as Externals


class StemmerTests(unittest.TestCase):

    def test_stem_default(self):

        self.assertEqual("troubl", Stemmer.stem("trouble"))
        self.assertEqual("troubl", Stemmer.stem("troubled"))
        self.assertEqual("troubl", Stemmer.stem("troubles"))
        self.assertEqual("troubl", Stemmer.stem("troubling"))
        self.assertEqual("", Stemmer.stem(""))

    def test_stem_porter(self):

        self.assertEqual("troubl", Stemmer.stem("trouble", stemmer="porter"))
        self.assertEqual("troubl", Stemmer.stem("troubled", stemmer="porter"))
        self.assertEqual("troubl", Stemmer.stem("troubles", stemmer="porter"))
        self.assertEqual("troubl", Stemmer.stem("troubling", stemmer="porter"))

    def test_stem_lancaster(self):

        self.assertEqual("troubl", Stemmer.stem("trouble", stemmer="lancaster"))
        self.assertEqual("troubl", Stemmer.stem("troubled", stemmer="lancaster"))
        self.assertEqual("troubl", Stemmer.stem("troubles", stemmer="lancaster"))
        self.assertEqual("troubl", Stemmer.stem("troubling", stemmer="lancaster"))

    def test_stem_regex(self):

        self.assertEqual("troubl", Stemmer.stem("trouble", stemmer="regex", regexp="ing$|s$|e$|able$|ed$|es$", min=0))
        self.assertEqual("troubl", Stemmer.stem("troubled", stemmer="regex", regexp="ing$|s$|e$|able$|ed$|es$", min=0))
        self.assertEqual("troubl", Stemmer.stem("troubles", stemmer="regex", regexp="ing$|s$|e$|able$|ed$|es$", min=0))
        self.assertEqual("troubl", Stemmer.stem("troubling", stemmer="regex", regexp="ing$|s$|e$|able$|ed$|es$", min=0))

    def test_stem_isri(self):

        self.assertEqual("trouble", Stemmer.stem("trouble", stemmer="isri"))
        self.assertEqual("troubled", Stemmer.stem("troubled", stemmer="isri"))
        self.assertEqual("troubles", Stemmer.stem("troubles", stemmer="isri"))
        self.assertEqual("troubling", Stemmer.stem("troubling", stemmer="isri"))

    def test_stem_snowball(self):

        self.assertEqual("troubl", Stemmer.stem("trouble", stemmer="snowball", language="english"))
        self.assertEqual("troubl", Stemmer.stem("troubled", stemmer="snowball", language="english"))
        self.assertEqual("troubl", Stemmer.stem("troubles", stemmer="snowball", language="english"))
        self.assertEqual("troubl", Stemmer.stem("troubling", stemmer="snowball", language="english"))

    @unittest.skipIf(Externals.rslp_stemming is False, Externals.rslp_stemming_disabled)
    def test_stem_rslp(self):

        self.assertEqual("troubl", Stemmer.stem("trouble", stemmer="rslp"))
        self.assertEqual("troubl", Stemmer.stem("troubled", stemmer="rslp"))
        self.assertEqual("troubl", Stemmer.stem("troubles", stemmer="rslp"))
        self.assertEqual("troubl", Stemmer.stem("troubling", stemmer="rslp"))

    def test_stem_cistem(self):

        self.assertEqual("speicherbehalt", Stemmer.stem("Speicherbehältern", stemmer="cistem", case_insensitive=False))

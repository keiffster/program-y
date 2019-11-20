import unittest
import programytest.externals as Externals
from programy.nlp.stemming import Stemmer


class StemmerTests(unittest.TestCase):

    def test_stem_default(self):
        stemmer = Stemmer()
        self.assertIsNotNone(stemmer)
        self.assertIsNotNone(stemmer._impl)

        self.assertEqual("troubl", stemmer.stem("trouble"))
        self.assertEqual("troubl", stemmer.stem("troubled"))
        self.assertEqual("troubl", stemmer.stem("troubles"))
        self.assertEqual("troubl", stemmer.stem("troubling"))
        self.assertEqual("", stemmer.stem(""))

    def test_stem_unknonw(self):
        with self.assertRaises(ValueError):
            _ = Stemmer(stemmer="unknown")

    def test_stem_porter(self):
        stemmer = Stemmer(stemmer="porter")
        self.assertIsNotNone(stemmer)
        self.assertIsNotNone(stemmer._impl)

        self.assertEqual("troubl", stemmer.stem("trouble"))
        self.assertEqual("troubl", stemmer.stem("troubled"))
        self.assertEqual("troubl", stemmer.stem("troubles"))
        self.assertEqual("troubl", stemmer.stem("troubling"))

    def test_stem_lancaster(self):
        stemmer = Stemmer(stemmer="lancaster")
        self.assertIsNotNone(stemmer)
        self.assertIsNotNone(stemmer._impl)

        self.assertEqual("troubl", stemmer.stem("trouble"))
        self.assertEqual("troubl", stemmer.stem("troubled"))
        self.assertEqual("troubl", stemmer.stem("troubles"))
        self.assertEqual("troubl", stemmer.stem("troubling"))

    def test_stem_regex(self):
        stemmer = Stemmer( stemmer="regex", regexp="ing$|s$|e$|able$|ed$|es$", min=0)
        self.assertIsNotNone(stemmer)
        self.assertIsNotNone(stemmer._impl)

        self.assertEqual("troubl", stemmer.stem("trouble"))
        self.assertEqual("troubl", stemmer.stem("troubled"))
        self.assertEqual("troubl", stemmer.stem("troubles"))
        self.assertEqual("troubl", stemmer.stem("troubling"))

    def test_stem_regex_no_min(self):
        stemmer = Stemmer( stemmer="regex", regexp="ing$|s$|e$|able$|ed$|es$")
        self.assertIsNotNone(stemmer)
        self.assertIsNotNone(stemmer._impl)

        self.assertEqual("troubl", stemmer.stem("trouble"))
        self.assertEqual("troubl", stemmer.stem("troubled"))
        self.assertEqual("troubl", stemmer.stem("troubles"))
        self.assertEqual("troubl", stemmer.stem("troubling"))

    def test_stem_isri(self):
        stemmer = Stemmer(stemmer="isri")
        self.assertIsNotNone(stemmer)
        self.assertIsNotNone(stemmer._impl)

        self.assertEqual("trouble", stemmer.stem("trouble"))
        self.assertEqual("troubled", stemmer.stem("troubled"))
        self.assertEqual("troubles", stemmer.stem("troubles"))
        self.assertEqual("troubling", stemmer.stem("troubling"))

    def test_stem_snowball(self):
        stemmer = Stemmer(stemmer="snowball", language="english")
        self.assertIsNotNone(stemmer)
        self.assertIsNotNone(stemmer._impl)

        self.assertEqual("troubl", stemmer.stem("trouble"))
        self.assertEqual("troubl", stemmer.stem("troubled"))
        self.assertEqual("troubl", stemmer.stem("troubles"))
        self.assertEqual("troubl", stemmer.stem("troubling"))

    def test_stem_snowball_no_language(self):
        stemmer = Stemmer(stemmer="snowball")
        self.assertIsNotNone(stemmer)
        self.assertIsNotNone(stemmer._impl)

        self.assertEqual("troubl", stemmer.stem("trouble"))
        self.assertEqual("troubl", stemmer.stem("troubled"))
        self.assertEqual("troubl", stemmer.stem("troubles"))
        self.assertEqual("troubl", stemmer.stem("troubling"))

    @unittest.skipIf(Externals.rslp_stemming is False or Externals.all_externals is False, Externals.rslp_stemming_disabled)
    def test_stem_rslp(self):
        stemmer = Stemmer(stemmer="rslp")
        self.assertIsNotNone(stemmer)
        self.assertIsNotNone(stemmer._impl)

        self.assertEqual("avi", stemmer.stem("avião"))
        self.assertEqual("avi", stemmer.stem("aviões"))
        self.assertEqual("avi", stemmer.stem("aviação"))

    def test_stem_cistem(self):
        stemmer = Stemmer(stemmer="cistem", case_insensitive=False)
        self.assertIsNotNone(stemmer)
        self.assertIsNotNone(stemmer._impl)

        self.assertEqual("speicherbehalt", stemmer.stem("Speicherbehältern"))

    def test_stem_cistem_case_sensetive(self):
        stemmer = Stemmer(stemmer="cistem", case_insensitive=True)
        self.assertIsNotNone(stemmer)
        self.assertIsNotNone(stemmer._impl)

        self.assertEqual("speicherbehal", stemmer.stem("Speicherbehältern"))

    def test_stem_cistem_no_case_sensetive(self):
        stemmer = Stemmer(stemmer="cistem")
        self.assertIsNotNone(stemmer)
        self.assertIsNotNone(stemmer._impl)

        self.assertEqual("speicherbehalt", stemmer.stem("Speicherbehältern"))

    def test_no_stemmer_loaded(self):
        stemmer = Stemmer(stemmer="cistem")
        stemmer._impl = None

        self.assertEquals("Hallo", stemmer.stem("Hallo"))
import unittest

from programy.nlp.translate.textblob_translator import TextBlobTranslator

import programytest.externals as Externals


class TestTextBlobTranslator(unittest.TestCase):

    def test_languages(self):
        translator = TextBlobTranslator()
        languages = translator.languages()
        self.assertTrue(languages.startswith("AFRIKAANS, ALBANIAN, "))

        self.assertTrue(translator.supports_language('ENGLISH'))
        self.assertFalse(translator.supports_language('KLINGON'))

    def test_language_codes(self):
        translator = TextBlobTranslator()
        self.assertEqual("EN", translator.language_code("ENGLISH"))
        self.assertEqual("UNKNOWN", translator.language_code("KLINGON"))

    @unittest.skipIf(Externals.google_translate is False, Externals.google_translate_disabled)
    def test_detect_language(self):
        translator = TextBlobTranslator()
        self.assertEqual("EN", translator.detect("Hello"))
        self.assertEqual("FR", translator.detect("Bonjour"))
        # Cantonese, currently not supported by Google Translate
        self.assertEqual("UNKNOWN", translator.detect("粵語", "UNKNOWN"))

    def test_translate(self):
        translator = TextBlobTranslator()
        translated = translator.translate("Hello", from_lang='EN', to_lang='FR')
        self.assertTrue("Bonjour", translated)
import unittest
from textblob.exceptions import NotTranslated
from textblob import TextBlob
from urllib.error import URLError
import programytest.externals as Externals
from programy.nlp.translate.textblob_translator import TextBlobTranslator


class MockTextBlobTranslator(TextBlobTranslator):

    def __init__(self, not_translated=False, url_error=False, translated=None):
        TextBlobTranslator.__init__(self)
        self.not_translated = not_translated
        self.url_error = url_error
        self.translated = translated

    def _do_translate(self, text, from_lang, to_lang):
        if self.not_translated is True:
            raise NotTranslated("Mock error")

        if self.url_error is True:
            raise URLError("Mock error")

        if self.translated is not None:
            return self.translated

        return text


class TestTextBlobTranslator(unittest.TestCase):

    def test_get_textblob(self):
        translator = TextBlobTranslator()
        tb = translator._get_textblob("string")
        self.assertIsNotNone(tb)
        self.assertIsInstance(tb, TextBlob)

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

    @unittest.skipIf(Externals.google_translate is False or Externals.all_externals is False, Externals.google_translate_disabled)
    def test_detect_language(self):
        translator = TextBlobTranslator()
        self.assertEqual("EN", translator.detect("Hello"))
        self.assertEqual("FR", translator.detect("Bonjour"))
        # Cantonese, currently not supported by Google Translate
        self.assertEqual("UNKNOWN", translator.detect("粵語", "UNKNOWN"))

    def test_translate_to_from(self):
        translator = TextBlobTranslator()
        translated = translator.translate("Hello", from_lang='EN', to_lang='FR')
        self.assertTrue("Bonjour", translated)

    def test_translate_to_only(self):
        translator = TextBlobTranslator()
        translated = translator.translate("Hello", to_lang='FR')
        self.assertTrue("Bonjour", translated)

    def test_translate_translate_error(self):
        translator = MockTextBlobTranslator(not_translated=True)
        self.assertEquals("Hello", translator.translate("Hello", from_lang='EN', to_lang='FR'))

    def test_translate_url_error(self):
        translator = MockTextBlobTranslator(url_error=True)
        self.assertEquals("Hello", translator.translate("Hello", from_lang='EN', to_lang='FR'))
"""
Copyright (c) 2016-2019 Keith Sterling http://www.keithsterling.com

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated
documentation files (the "Software"), to deal in the Software without restriction, including without limitation
the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software,
and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the
Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO
THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT,
TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
"""
from programy.utils.logging.ylogger import YLogger

from urllib.error import URLError

from textblob import TextBlob
from textblob.exceptions import NotTranslated
from textblob.exceptions import TranslatorError
from programy.translate.base import BaseTranslator

languages = {
            "AFRIKAANS": "AF",
            "ALBANIAN": "SQ",
            "AMHARIC": "AM",
            "ARABIC": "AR",
            "ARMENIAN": "HY",
            "AZEERBAIJANI": "AZ",
            "BASQUE": "EU",
            "BELARUSIAN": "BE",
            "BENGALI": "BN",
            "BOSNIAN": "BS",
            "BULGARIAN": "BG",
            "CATALAN": "CA",
            "CEBUANO": "CEB",
            "SIMPLIFIED CHINESE": "ZH-CN",
            "CHINESE": "ZH-TW",
            "TRADITIONAL CHINESE": "ZH-TW",
            "CORSICAN": "CO",
            "CROATIAN": "HR",
            "CZECH": "CS",
            "DANISH": "DA",
            "DUTCH": "NL",
            "ENGLISH": "EN",
            "ESPERANTO": "EO",
            "ESTONIAN": "ET",
            "FINNISH": "FI",
            "FRENCH": "FR",
            "FRISIAN": "FY",
            "GALICIAN": "GL",
            "GEORGIAN": "KA",
            "GERMAN": "DE",
            "GREEK": "EL",
            "GUJARATI": "GU",
            "HAITIAN": "HT",
            "CREOLE": "HT",
            "HAUSA": "HA",
            "HAWAIIAN": "HAW",
            "HEBREW": "HE**",
            "HINDI": "HI",
            "HMONG": "HMN",
            "HUNGARIAN": "HU",
            "ICELANDIC": "IS",
            "IGBO": "IG",
            "INDONESIAN": "ID",
            "IRISH": "GA",
            "ITALIAN": "IT",
            "JAPANESE": "JA",
            "JAVANESE": "JW",
            "KANNADA": "KN",
            "KAZAKH": "KK",
            "KHMER": "KM",
            "KOREAN": "KO",
            "KURDISH": "KU",
            "KYRGYZ": "KY",
            "LAO": "LO",
            "LATIN": "LA",
            "LATVIAN": "LV",
            "LITHUANIAN": "LT",
            "LUXEMBOURGISH": "LB",
            "MACEDONIAN": "MK",
            "MALAGASY": "MG",
            "MALAY": "MS",
            "MALAYALAM": "ML",
            "MALTESE": "MT",
            "MAORI": "MI",
            "MARATHI": "MR",
            "MONGOLIAN": "MN",
            "MYANMAR": "MY",
            "BURMESE": "MY",
            "NEPALI": "NE",
            "NORWEGIAN": "NO",
            "NYANJA": "NY",
            "CHICHEWA": "NY",
            "PASHTO": "PS",
            "PERSIAN": "FA",
            "POLISH": "PL",
            "PORTUGUESE": "PT",
            "BRAZILIAN": "PT",
            "PUNJABI": "PA",
            "ROMANIAN": "RO",
            "RUSSIAN": "RU",
            "SAMOAN": "SM",
            "SCOTTISH": "GD",
            "SCOTS GAELIC": "GD",
            "SERBIAN": "SR",
            "SESOTHO": "ST",
            "SHONA": "SN",
            "SINDHI": "SD",
            "SINHALA": "SI",
            "SINHALESE": "SI",
            "SLOVAK": "SK",
            "SLOVENIAN": "SL",
            "SOMALI": "SO",
            "SPANISH": "ES",
            "SUNDANESE": "SU",
            "SWAHILI": "SW",
            "SWEDISH": "SV",
            "TAGALOG": "TL",
            "FILIPINO": "TL",
            "TAJIK": "TG",
            "TAMIL": "TA",
            "TELUGU": "TE",
            "THAI": "TH",
            "TURKISH": "TR",
            "UKRAINIAN": "UK",
            "URDU": "UR",
            "UZBEK": "UZ",
            "VIETNAMESE": "VI",
            "WELSH": "CY",
            "XHOSA": "XH",
            "YIDDISH": "YI",
            "YORUBA": "YO",
            "ZULU": "ZU"
        }


class TextBlobTranslator(BaseTranslator):

    def languages(self):
        return ", ".join(languages.keys())

    def supports_language(self, language):
        return bool(language in languages)

    def language_code(self, code):
        if code in languages:
            return languages[code]
        return "UNKNOWN"

    def detect(self, text, default='EN'):
        blob = TextBlob(text)
        try:
            return blob.detect_language().upper()

        except TranslatorError as te:
            YLogger.exception(None, "Unable to determine langauge for [%s]", te, text)

        return default

    def translate(self, text, from_lang, to_lang="EN"):

        YLogger.debug(None, "Translating [%s] from [%s] to [%s], are they the same?", text, from_lang, to_lang)

        blob = TextBlob(text)
        try:
            if from_lang is not None:
                translated = str(blob.translate(from_lang=from_lang, to=to_lang))
            else:
                translated = str(blob.translate(to=to_lang))
            YLogger.debug(None, "Translated [%s] to [%s]", text, translated)
            return translated

        except NotTranslated as nte:
            YLogger.exception(None, "Unable to translate text from [%s] to [%s], are they the same?", nte, from_lang, to_lang)

        except URLError as urle:
            YLogger.exception(None, "No connection to Google Translate", urle)

        return text


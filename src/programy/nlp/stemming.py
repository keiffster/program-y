"""
Copyright (c) 2016-2020 Keith Sterling http://www.keithsterling.com

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
import nltk
from nltk.stem.regexp import RegexpStemmer
from nltk.stem.lancaster import LancasterStemmer
from nltk.stem.isri import ISRIStemmer
from nltk.stem.porter import PorterStemmer
from nltk.stem.snowball import SnowballStemmer
from nltk.stem.rslp import RSLPStemmer
from nltk.stem.cistem import Cistem


class Stemmer:

    @staticmethod
    def download_additional():
        nltk.download('rslp')   # pragma: no cover

    def __init__(self, stemmer="porter", **kwargs):
        self._impl = self._get_stemmer(stemmer, **kwargs)

    def stem(self, string):
        if self._impl is not None:
            return self._impl.stem(string)

        return string

    def _get_porter_stemmer(self):
        return PorterStemmer()

    def _get_lancaster_stemmer(self):
        return LancasterStemmer()

    def _get_regex_stemmer(self, regexp, minimum):
        return RegexpStemmer(regexp=regexp, min=minimum)

    def _get_iris_stemmer(self):
        return ISRIStemmer()

    def _get_snowball_stemmer(self, language):
        return SnowballStemmer(language=language)

    def _get_rslp_stemmer(self):
        return RSLPStemmer()

    def _get_cis_stemmer(self, case_insensitive):
        return Cistem(case_insensitive=case_insensitive)

    def _get_stemmer(self, stemmer="porter", **kwargs):

        if stemmer == "porter":
            return self._get_porter_stemmer()

        elif stemmer == "lancaster":
            return self._get_lancaster_stemmer()

        elif stemmer == "regex":
            regexp = kwargs['regexp']
            if 'min' in kwargs:
                minimum = kwargs['min']

            else:
                minimum = 0

            return self._get_regex_stemmer(regexp=regexp, minimum=minimum)

        elif stemmer == "isri":
            return self._get_iris_stemmer()

        elif stemmer == "snowball":
            if 'language' in kwargs:
                language = kwargs['language']

            else:
                language = 'english'

            return self._get_snowball_stemmer(language=language)

        elif stemmer == "rslp":
            return self._get_rslp_stemmer()

        elif stemmer == "cistem":
            if 'case_insensitive' in kwargs:
                case_insensitive = kwargs['case_insensitive']

            else:
                case_insensitive = False

            return self._get_cis_stemmer(case_insensitive=case_insensitive)

        else:
            raise ValueError("Unknown stemmer [%s]"%stemmer)

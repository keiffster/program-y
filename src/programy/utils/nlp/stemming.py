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
import nltk
from nltk.stem.regexp import RegexpStemmer
from nltk.stem.lancaster import LancasterStemmer
from nltk.stem.isri import ISRIStemmer
from nltk.stem.porter import PorterStemmer
from nltk.stem.snowball import SnowballStemmer
from nltk.stem.rslp import RSLPStemmer
from nltk.stem.cistem import Cistem


class Stemmer(object):

    @staticmethod
    def download_additional():
        nltk.download('rslp')

    @staticmethod
    def stem(string, stemmer="porter", **kwargs):

        if stemmer == "porter":
            impl = PorterStemmer()
        elif stemmer == "lancaster":
            impl = LancasterStemmer()
        elif stemmer == "regex":
            regexp = kwargs['regexp']
            if 'min' in kwargs:
                min = kwargs['min']
            else:
                mins = 0
            impl = RegexpStemmer(regexp=regexp, min=min)
        elif stemmer == "isri":
            impl = ISRIStemmer()
        elif stemmer == "snowball":
            if 'language' in kwargs:
                language=kwargs['language']
            else:
                language='english'
            impl = SnowballStemmer(language=language)
        elif stemmer == "rslp":
            impl = RSLPStemmer()
        elif stemmer == "cistem":
            if 'case_insensitive' in kwargs:
                case_insensitive = kwargs['case_insensitive']
            else:
                case_insensitive = False
            impl = Cistem(case_insensitive=case_insensitive)
        else:
            return string

        return impl.stem(string)

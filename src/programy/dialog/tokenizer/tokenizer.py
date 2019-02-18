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
import re
from programy.utils.logging.ylogger import YLogger
from programy.utils.classes.loader import ClassLoader


class Tokenizer(object):

    def __init__(self, split_chars=' '):
        self.split_chars = split_chars

    def texts_to_words(self, texts):
        if not texts:
            return []
        return [word.strip() for word in texts.split(self.split_chars) if word]

    def words_to_texts(self, words):
        if not words:
            return ''
        to_join = [word.strip() for word in words if word]
        return self.split_chars.join(to_join)

    def words_from_current_pos(self, words, current_pos):
        if not words:
            return ''
        return self.split_chars.join(words[current_pos:])

    def compare(self, value1, value2):
        return value1 == value2

    @staticmethod
    def load_tokenizer(configuration):
        if configuration is not None and configuration.tokenizer.classname is not None:
            YLogger.info(None, "Loading tokenizer from class [%s]", configuration.tokenizer.classname)
            tokenizer_class = ClassLoader.instantiate_class(configuration.tokenizer.classname)
            return tokenizer_class(configuration.tokenizer.split_chars)
        else:
            return Tokenizer(configuration.tokenizer.split_chars)


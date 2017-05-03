"""
Copyright (c) 2016 Keith Sterling

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated
documentation files (the "Software"), to deal in the Software without restriction, including without limitation
the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software,
and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO
THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT,
TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
"""


import logging
import re

from programy.processors.processing import PostProcessor

class FormatPunctuationProcessor(PostProcessor):
    def __init__(self):
        PostProcessor.__init__(self)

    def spaceSplit(self, string):
        last = 0
        splits = []
        inQuote = None
        for i, letter in enumerate(string):
            if inQuote:
                if (letter == inQuote):
                    inQuote = None
            else:
                if (letter == '"' or letter == "'"):
                    inQuote = letter

            if not inQuote and letter == ' ':
                splits.append(string[last:i])
                last = i + 1

        if last < len(string):
            splits.append(string[last:])

        return splits

    def process(self, bot, clientid, word_str):
        logging.debug("Formatting punctuation...")

        word_list = self.spaceSplit(word_str)
        new_word_list = []
        for word in word_list:
            word = re.sub(r'(["|\'])\s+', r'\1', word)
            word = re.sub(r'\s+(["|\'])', r'\1', word)
            new_word_list.append(word)
        word_str = " ".join(new_word_list)
        word_str = re.sub(r'\s+([.,:;!?])', r'\1', word_str)
        word_str = re.sub(r'([@])\s+', r'\1', word_str)

        return word_str
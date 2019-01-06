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
import re

from programy.processors.processing import PostProcessor

class FormatPunctuationProcessor(PostProcessor):
    def __init__(self):
        PostProcessor.__init__(self)

    def space_split(self, string):
        last = 0
        splits = []
        in_quote = None
        for i, letter in enumerate(string):
            if in_quote:
                if letter == in_quote:
                    in_quote = None
            else:
                if letter == '"' or letter == "'":
                    in_quote = letter

            if not in_quote and letter == ' ':
                splits.append(string[last:i])
                last = i + 1

        if last < len(string):
            splits.append(string[last:])

        return splits

    def process(self, context, word_string):
        YLogger.debug(context, "Formatting punctuation...")

        word_list = self.space_split(word_string)
        new_word_list = []
        for word in word_list:
            word = re.sub(r'(["|\'])\s+', r'\1', word)
            word = re.sub(r'\s+(["|\'])', r'\1', word)
            new_word_list.append(word)
        word_string = " ".join(new_word_list)
        word_string = re.sub(r'\s+([.,:;!?])', r'\1', word_string)
        word_string = re.sub(r'([@])\s+', r'\1', word_string)

        return word_string

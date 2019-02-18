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


class Sentence(object):

    def __init__(self, tokenizer, text: str = None ):
        self._tokenizer = tokenizer
        self._words = self._tokenizer.texts_to_words(text)
        self._response = None
        self._matched_context = None
        self._positivity = 0.00
        self._subjectivity = 0.5

    @property
    def words(self):
        return self._words

    @property
    def positivity(self):
        return self._positivity

    @positivity.setter
    def positivity(self, value):
        self._positivity = value

    @property
    def subjectivity(self):
        return self._subjectivity

    @subjectivity.setter
    def subjectivity(self, value):
        self._subjectivity = value

    def append_word(self, word):
        self._words.append(word)

    def append_sentence(self, sentence):
        for word in sentence.words:
            self._words.append(word)

    def replace_words(self, text):
        self._words = self._split_into_words(text)

    @property
    def response(self):
        return self._response

    @response.setter
    def response(self, text: str):
        self._response = text

    @property
    def matched_context(self):
        return self._matched_context

    @matched_context.setter
    def matched_context(self, context):
        self._matched_context = context

    def num_words(self):
        return len(self.words)

    def word(self, num: int):
        if num < self.num_words():
            return self.words[num]
        return None

    def words_from_current_pos(self, current_pos: int):
        return self._tokenizer.words_from_current_pos(self._words, current_pos)

    def text(self):
        return self._tokenizer.words_to_texts(self._words)

    def _split_into_words(self, text):
        if text is None:
            return []
        return self._tokenizer.texts_to_words(text)

    def calculate_sentinment_score(self, client_context):

        assert (client_context is not None)

        if client_context.bot.sentiment_analyser is not None:
            positivity, subjectivity = client_context.bot.sentiment_analyser.analyse_all(self.text())
            YLogger.debug(client_context, "Sentiment: positivity[%f], subjectivity [%f]", positivity, subjectivity)
            self._positivity = positivity
            self._subjectivity = subjectivity




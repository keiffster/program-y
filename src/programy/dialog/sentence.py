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
from programy.utils.logging.ylogger import YLogger
from programy.parser.pattern.matchcontext import MatchContext


class Sentence:

    def __init__(self, client_context=None, text: str = None,
                 response: str = None,
                 matched_context: MatchContext = None,
                 positivity=0.0, subjectivity=0.5):
        if text is not None:
            self._words = client_context.brain.tokenizer.texts_to_words(text)
        else:
            self._words = []
        self._response = response
        self._matched_context = matched_context
        self._positivity = positivity
        self._subjectivity = subjectivity

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

    @property
    def words(self):
        return self._words

    @words.setter
    def words(self, words):
        self._words = words[:]

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

    def replace_words(self, client_context, text):
        self._words = Sentence._split_into_words(client_context.brain.tokenizer, text)

    def num_words(self):
        return len(self.words)

    def word(self, num: int):
        if num < self.num_words():
            return self.words[num]
        return None

    def words_from_current_pos(self, client_context, current_pos: int):
        return client_context.brain.tokenizer.words_from_current_pos(self._words, current_pos)

    def text(self, client_context):
        return client_context.brain.tokenizer.words_to_texts(self._words)

    @staticmethod
    def _split_into_words(tokenizer, text):
        if text is None or tokenizer is None:
            return []
        return tokenizer.texts_to_words(text)

    def calculate_sentinment_score(self, client_context):

        assert client_context is not None

        if client_context.bot.sentiment_analyser is not None:
            positivity, subjectivity = client_context.bot.sentiment_analyser.analyse_all(self.text(client_context))
            YLogger.debug(client_context, "Sentiment: positivity[%f], subjectivity [%f]", positivity, subjectivity)
            self._positivity = positivity
            self._subjectivity = subjectivity

    def to_json(self):
        json_data = {
            "words": self._words,
            "response": self._response,
            "positivity": self._positivity,
            "subjectivity": self._subjectivity
        }

        if self._matched_context is not None:
            json_data["matched_context"] = self._matched_context.to_json()

        return json_data

    @staticmethod
    def from_json(client_context, json_data):

        sentence = Sentence(client_context)

        sentence.words = json_data['words']
        sentence.response = json_data['response']
        sentence.positivity = json_data['positivity']
        sentence.subjectivity = json_data['subjectivity']

        if 'matched_context' in json_data:
            sentence.matched_context = MatchContext.from_json(json_data["matched_context"])

        return sentence

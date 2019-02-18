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
from programy.dialog.sentence import Sentence


class Question(object):

    @staticmethod
    def create_from_text(client_context, text, split=True, srai=False):
        question = Question(srai)
        if split is True:
            question.split_into_sentences(client_context, text)
        else:
            question.sentences.append(Sentence(client_context.brain.tokenizer, text))
        question.recalculate_sentinment_score(client_context)
        return question

    @staticmethod
    def create_from_sentence(sentence: Sentence, srai=False):
        question = Question(srai)
        question.sentences.append(sentence)
        return question

    @staticmethod
    def create_from_question(question, srai=False):
        new_question = Question(srai)
        for each_sentence in question.sentences:
            new_question.sentences.append(each_sentence)
        return new_question

    def __init__(self, srai=False):
        self._srai = srai
        self._sentences = []
        self._properties = {}
        self._current_sentence_no = -1

    def debug_info(self):
        text = ""
        for sentence in self._sentences:
            text += sentence.text()
            text += " = "
            if sentence.response is not None:
                text += sentence.response
            else:
                text += "N/A"
            text += ", "
        return text

    @property
    def sentences(self):
        return self._sentences

    def has_response(self):
        for sentence in self._sentences:
            if sentence.response is not None:
                return True
        return False

    def set_current_sentence_no(self, sentence_no):
        self._current_sentence_no = sentence_no

    def set_property(self, name: str, value: str):
        self._properties[name] = value

    def property(self, name: str):
        if name in self._properties:
            return self._properties[name]
        return None

    def sentence(self, num: int):
        if num < len(self._sentences):
            return self._sentences[num]
        raise Exception("Num sentence array violation !")

    def current_sentence(self):
        if not self._sentences:
            raise Exception("Num sentence array violation !")
        return self._sentences[self._current_sentence_no]

    def previous_nth_sentence(self, num):
        if len(self._sentences) < num:
            raise Exception("Num sentence array violation !")
        previous = -1 - num
        return self._sentences[previous]

    def combine_sentences(self):
        return ". ".join([sentence.text() for sentence in self._sentences])

    def combine_answers(self):
        return ". ".join([sentence.response for sentence in self.sentences if sentence.response is not None])

    def split_into_sentences(self, client_context, text):
        if client_context.bot.sentence_splitter.is_active():
            if text is not None and text.strip():
                all_sentences = client_context.bot.sentence_splitter.split(text)
                for each_sentence in all_sentences:
                    self._sentences.append(Sentence(client_context.brain.tokenizer, each_sentence))
        else:
            self._sentences.append(Sentence(client_context.brain.tokenizer, text))

    def recalculate_sentinment_score(self, client_context):
        for sentence in self._sentences:
            sentence.calculate_sentinment_score(client_context)

    def calculate_sentinment_score(self):

        positivity = 0.00
        subjectivity = 0.00

        count = 0
        for sentence in self._sentences:
            positivity += sentence.positivity
            subjectivity += sentence.subjectivity
            count += 1

        if count > 0:
            positivity /= count
            subjectivity /= count
        else:
            subjectivity = 0.5

        return positivity, subjectivity

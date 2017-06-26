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

class Sentence(object):

    def __init__(self, text: str=None, split_chars: str=" "):
        self._words = self._split_into_words(text, split_chars)
        self._response = None
        self._matched_context = None

    @property
    def words(self):
        return self._words

    def append_word(self, word):
        self._words.append(word)

    def append_sentence(self, sentence):
        for word in sentence._words:
            self._words.append(word)

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
        else:
            return None

    def words_from_current_pos(self, current_pos: int):
        if len(self._words) > 0:
            return " ".join(self._words[current_pos:])
        else:
            # return ""
            raise Exception("Num word array violation !")

    def text(self):
        return " ".join(self._words)

    def _split_into_words(self, sentence, split_chars: str):
        if sentence is None:
            return []
        else:
            sentence = sentence.strip()
            if len(sentence) == 0:
                return []
            else:
                return sentence.split(split_chars)


class Question(object):

    @staticmethod
    def create_from_text(text: str, sentence_split_chars: str=".", word_split_chars: str=" ", split=True):
        question = Question()
        if split is True:
            question._split_into_sentences(text, sentence_split_chars, word_split_chars)
        else:
            question._sentences = []
            question._sentences.append(Sentence(text))
        return question

    @staticmethod
    def create_from_sentence(sentence: Sentence):
        question = Question()
        question.sentences.append(sentence)
        return question

    @staticmethod
    def create_from_question(question):
        new_question = Question()
        for each_sentence in question.sentences:
            new_question.sentences.append(each_sentence)
        return new_question

    def __init__(self):
        self._sentences = []
        self._predicates = {}

    @property
    def sentences(self):
        return self._sentences

    def set_predicate(self, name: str, value: str):
        self._predicates[name] = value

    def predicate(self, name: str):
        if name in self._predicates:
            return self._predicates[name]
        else:
            return None

    def sentence(self, num: int):
        if num < len(self._sentences):
            return self._sentences[num]
        else:
            raise Exception("Num sentence array violation !")

    def current_sentence(self):
        if len(self._sentences) == 0:
            raise Exception("Num sentence array violation !")
        else:
            return self._sentences[-1]

    def previous_sentence(self, num):
        if len(self._sentences) < num:
            raise Exception("Num sentence array violation !")
        else:
            return self._sentences[len(self._sentences)-num]

    def combine_sentences(self):
        return ". ".join([sentence.text() for sentence in self._sentences])

    def combine_answers(self):
        return ". ".join([sentence.response for sentence in self.sentences if sentence.response is not None])

    def _split_into_sentences(self, text: str, sentence_split_chars: str, word_split_chars: str):
        if text is not None and len(text.strip()) > 0:
            self._sentences = []
            all_sentences = text.split(sentence_split_chars)
            for each_sentence in all_sentences:
                self._sentences.append(Sentence(each_sentence, word_split_chars))
#
# A Conversation is made up of questions, each question is made up of sentences
#
class Conversation(object):

    def __init__(self, clientid: str, bot: object, max_histories=100):
        self._bot = bot
        self._clientid = clientid
        self._questions = []
        self._max_histories = max_histories
        self._predicates = {}
        self._predicates['topic'] = '*'

    @property
    def bot(self):
        return self._bot

    @property
    def clientid(self):
        return self._clientid

    @property
    def questions(self):
        return self._questions

    # 1 indexed, not 0 indexed, 1st question is nth_question(1)
    def nth_question(self, num: int):
        if num <= len(self._questions):
            question_num = len(self._questions)-num
            return self._questions[question_num]
        else:
            raise Exception("Invalid question index")

    def current_question(self):
        if len(self._questions) > 0:
            return self._questions[-1]
        else:
            raise Exception("Invalid question index")

    def all_sentences(self):
        sentences = []
        for question in self._questions:
            for sentence in question.sentences:
                sentences.append(sentence.text())
        return sentences

    def nth_sentence(self, num: int):
        sentences = self.all_sentences()
        if num <= len(sentences):
            return sentences[len(sentences)-num]
        else:
            raise Exception("Invalid sentence index")

    def set_predicate(self, name: str, value: str):
        if name == 'topic':
            if value == "":
                value = '*'

        self._predicates[name] = value

    def predicate(self, name: str):
        if self._predicates is not None:
            if name in self._predicates:
                return self._predicates[name]

        return None

    def record_dialog(self, question: Question):
        if len(self._questions) == self._max_histories:
            logging.info("Conversation history at max [%d], removing oldest", self._max_histories)
            self._questions.remove(self._questions[0])
        self._questions.append(question)

    def pop_dialog(self):
        if len(self._questions) > 0:
            self._questions.pop()

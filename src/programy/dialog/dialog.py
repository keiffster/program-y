"""
Copyright (c) 2016-2018 Keith Sterling http://www.keithsterling.com

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

from programy.dialog.tokenizer.tokenizer import Tokenizer
from programy.utils.text.text import TextUtils

class Sentence(object):

    def __init__(self, tokenizer, text: str = None ):
        self._tokenizer = tokenizer
        self._words = self._tokenizer.texts_to_words(text)
        self._response = None
        self._matched_context = None

    @property
    def words(self):
        return self._words

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


class Question(object):

    @staticmethod
    def create_from_text(client_context, text, split=True, srai=False):
        question = Question(srai)
        if split is True:
            question.split_into_sentences(client_context, text)
        else:
            question.sentences.append(Sentence(client_context.brain.tokenizer, text))
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
        str = ""
        for sentence in self._sentences:
            str += sentence.text()
            str += " = "
            if sentence.response is not None:
                str += sentence.response
            else:
                str += "N/A"
            str += ", "
        return str

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
        if text is not None and text.strip():
            all_sentences = client_context.bot.sentence_splitter.split(text)
            for each_sentence in all_sentences:
                self._sentences.append(Sentence(client_context.brain.tokenizer, each_sentence))


#
# A Conversation is made up of questions, each question is made up of sentences
#
class Conversation(object):

    def __init__(self, client_context):
        self._client_context = client_context
        self._questions = []
        self._max_histories = client_context.bot.configuration.conversations.max_histories
        self._properties = {'topic': client_context.bot.configuration.conversations.initial_topic}

    @property
    def questions(self):
        return self._questions

    @property
    def max_histories(self):
        return self._max_histories

    @property
    def properties(self):
        return self._properties

    def has_current_question(self):
        return bool(self._questions)

    def current_question(self):
        if self._questions:
            return self._questions[-1]
        raise Exception("Invalid question index")

    def previous_nth_question(self, num: int):
        if len(self._questions) < num:
            raise Exception("Num question array violation !")
        previous = -1 - num
        return self._questions[previous]

    def set_property(self, name: str, value: str):
        if name == 'topic':
            if value == "":
                value = '*'
        self._properties[name] = value

    def property(self, name: str):
        if self._properties is not None:
            if name in self._properties:
                return self._properties[name]
        return None

    def record_dialog(self, question: Question):
        if len(self._questions) == self._max_histories:
            YLogger.info(self, "Conversation history at max [%d], removing oldest", self._max_histories)
            self._questions.remove(self._questions[0])
        self._questions.append(question)

    def pop_dialog(self):
        if self._questions:
            self._questions.pop()

    def load_initial_variables(self, variables_collection):
        for pair in variables_collection.pairs:
            YLogger.debug(self, "Setting variable [%s] = [%s]", pair[0], pair[1])
            self._properties[pair[0]] = pair[1]

    def get_topic_pattern(self, client_context):
        topic_pattern = self.property("topic")

        if topic_pattern is None:
            YLogger.info(client_context, "No Topic pattern default to [*]")
            topic_pattern = "*"
        else:
            YLogger.info(client_context, "Topic pattern = [%s]", topic_pattern)

        return topic_pattern

    def parse_last_sentences_from_response(self, response):

        # If the response contains punctuation such as "Hello. There" then THAT is none
        response = re.sub(r'<\s*br\s*/>\s*', ".", response)
        response = re.sub(r'<br></br>*', ".", response)
        sentences = response.split(".")
        sentences = [x for x in sentences if x]
        last_sentence = sentences[-1]
        that_pattern = TextUtils.strip_all_punctuation(last_sentence)
        that_pattern = that_pattern.strip()

        if that_pattern == "":
            that_pattern = '*'

        return that_pattern

    def get_that_pattern(self, client_context, srai=False):
        try:
            that_question = None
            if srai is False:
                that_question = self.previous_nth_question(1)
            else:
                if len(self._questions) > 2:
                    for question in reversed(self._questions[:-2]):
                        if question._srai is False and question.has_response():
                            that_question = question
                            break

            if that_question is not None:
                that_sentence = that_question.current_sentence()
            else:
                that_sentence = None

            # If the last response was valid, i.e not none and not empty string, then use
            # that as the that_pattern, otherwise we default to '*' as pattern
            if that_sentence.response is not None and that_sentence.response != '':
                that_pattern = self.parse_last_sentences_from_response(that_sentence.response)
                YLogger.info(client_context, "That pattern = [%s]", that_pattern)
            else:
                YLogger.info(client_context, "That pattern, no response, default to [*]")
                that_pattern = "*"

        except Exception as e:
            YLogger.info(client_context, "No That pattern default to [*]")
            that_pattern = "*"

        return that_pattern

    def to_json(self):
        json_data = {
            'client_context': self._client_context.to_json(),
            'questions': [],
            'max_histories': self._max_histories,
            'properties': self._properties
        }

        for question in self.questions:
            json_question = {'sentences': [],
                             'srai': question._srai,
                             'properties': question._properties,
                             'current_sentence_no': question._current_sentence_no
            }
            json_data['questions'].append(json_question)

            for sentence in question.sentences:
                json_sentence = {"question": sentence.text(),
                                 "response": sentence.response
                                 }
                json_question['sentences'].append(json_sentence)

        return json_data

    def from_json(self, json_data):
        if json_data is not None:
            json_questions = json_data['questions']
            for json_question in json_questions:
                json_sentences = json_question['sentences']
                for json_sentence in json_sentences:
                    question = Question.create_from_text(self._client_context, json_sentence['question'])
                    question.sentence(0).response = json_sentence['response']
                    self._questions.append(question)
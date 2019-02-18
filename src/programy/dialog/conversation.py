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

from programy.utils.text.text import TextUtils
from programy.dialog.question import Question

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
                                 "response": sentence.response,
                                 "positivity": sentence.positivity,
                                 "subjectivity": sentence.subjectivity
                                 }
                json_question['sentences'].append(json_sentence)

        return json_data

    def from_json(self, client_context, json_data):
        if json_data is not None:
            json_questions = json_data['questions']
            for json_question in json_questions:
                json_sentences = json_question['sentences']
                for json_sentence in json_sentences:
                    question = Question.create_from_text(self._client_context, json_sentence['question'])
                    question.sentence(0).response = json_sentence['response']
                    self._questions.append(question)
            self.recalculate_sentiment_score(client_context)

    def recalculate_sentiment_score(self, client_context):
        for question in self._questions:
            question.recalculate_sentinment_score(client_context)

    def calculate_sentiment_score(self):

        positivity = 0.00
        subjectivity = 0.00

        count = 0
        for question in self._questions:
            q_positivity, q_subjectivity = question.calculate_sentinment_score()

            positivity += q_positivity
            subjectivity += q_subjectivity

            count += 1

        if count > 0:
            positivity /= count
            subjectivity /= count
        else:
            subjectivity = 0.5

        return positivity, subjectivity

    def save_sentiment(self):
        positivity, subjectivity = self.calculate_sentiment_score()
        self._properties['positivity'] = str(positivity)
        self._properties['subjectivity'] = str(subjectivity)


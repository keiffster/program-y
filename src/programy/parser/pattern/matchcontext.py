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

import datetime

from programy.parser.pattern.match import Match


class MatchContext(object):

    def __init__(self,
                 max_search_depth,
                 max_search_timeout,
                 matched_nodes=None,
                 template_node=None,
                 sentence=None,
                 response=None):
        self._max_search_depth = max_search_depth
        self._max_search_timeout = max_search_timeout
        self._total_search_start = datetime.datetime.now()
        self._matched_nodes = []
        if matched_nodes is not None:
            self._matched_nodes = matched_nodes.copy()
        self._template_node = template_node
        self._sentence = sentence
        self._response = response

    @property
    def matched_nodes(self):
        return self._matched_nodes

    @property
    def template_node(self):
        return self._template_node

    @template_node.setter
    def template_node(self, template_node):
        self._template_node = template_node

    @property
    def response(self):
        return self._response

    @response.setter
    def response(self, response):
        self._response = response

    @property
    def sentence(self):
        return self._sentence

    @sentence.setter
    def sentence(self, sentence):
        self._sentence = sentence

    @property
    def max_search_depth(self):
        return self._max_search_depth

    @property
    def total_search_start(self):
        return self._total_search_start

    @property
    def max_search_timeout(self):
        return self._max_search_timeout

    def search_depth_exceeded(self, depth):
        if self._max_search_depth == -1:
            return False
        return bool(depth > self._max_search_depth)

    def total_search_time(self):
        delta = datetime.datetime.now() - self._total_search_start
        return abs(delta.total_seconds())

    def search_time_exceeded(self):
        if self._max_search_timeout == -1:
            return False
        return bool(self.total_search_time() >= self._max_search_timeout)

    def add_match(self, match):
        self._matched_nodes.append(match)

    def pop_match(self):
        if self._matched_nodes:
            self._matched_nodes.pop()

    def pop_matches(self, matches_add):
        for match in range(0, matches_add):
            self.pop_match()

    @property
    def matched_nodes(self):
        return self._matched_nodes

    def matched(self):
        return bool(self._template_node is not None or self._response is not None)

    def _get_indexed_match_by_type(self, client_context, index, match_type):
        count = 1
        for matched_node in self._matched_nodes:
            if matched_node.matched_node_type == match_type and matched_node.matched_node_multi_word is True:
                if count == index:
                    return matched_node.joined_words(client_context)
                count += 1
        return None

    def star(self, client_context, index):
        return self._get_indexed_match_by_type(client_context, index, Match.WORD)

    def topicstar(self, client_context, index):
        return self._get_indexed_match_by_type(client_context, index, Match.TOPIC)

    def thatstar(self, client_context, index):
        return self._get_indexed_match_by_type(client_context, index, Match.THAT)

    def list_matches(self, client_context, output_func=YLogger.debug, tabs="\t", include_template=True):
        output_func(client_context, "%sMatches..."%tabs)
        count = 1
        if self._sentence is not None:
            output_func(client_context, "%sAsked:"%(tabs, self._sentence))
        for match in self._matched_nodes:
            output_func(client_context, "%s\t%d: %s"%(tabs, count, match.to_string(client_context)))
            count += 1
        output_func(client_context, "%sMatch score %.2f"%(tabs, self.calculate_match_score()))
        if include_template is True:
            if self.matched() is True:
                if self._response is not None:
                    output_func(client_context, "%s\tResponse: %s"%(tabs, self._response))
            else:
                output_func(client_context, "%s\tResponse: None"%tabs)

    def calculate_match_score(self):
        wildcards = 0
        words = 0
        for match in self._matched_nodes:
            if match.matched_node_type == Match.WORD:
                if match.matched_node_wildcard:
                    wildcards += 1
                else:
                    words += 1
        total = wildcards+words
        if total > 0:
            return (words/(wildcards+words))*100.00
        return 0.00

    def to_json(self):
        context={ "max_search_depth":self._max_search_depth,
                  "max_search_timeout": self._max_search_timeout,
                  "total_search_start": self._total_search_start.strftime("%d/%m/%Y, %H:%M:%S"),
                  "sentence": self._sentence,
                  "response": self._response,
                  "matched_nodes": []
                }

        for match in self._matched_nodes:
            context["matched_nodes"].append(match.to_json())

        return context

    @staticmethod
    def from_json(json_data):
        match_context = MatchContext(0, 0)

        match_context._max_search_depth = json_data["max_search_depth"]
        match_context._max_search_timeout = json_data["max_search_timeout"]
        match_context._total_search_start = datetime.strptime(json_data["total_search_start"], "%d/%m/%Y, %H:%M:%S")
        match_context._sentence = json_data["sentence"]
        match_context._response = json_data["response"]

        for match_data in json_data["matched_nodes"]:
            match_context._matched_nodes.append(Match.from_json(match_data))

        return match_context

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


class Match:
    WORD = 0
    TOPIC = 2
    THAT = 3

    def __init__(self, match_type, node, word):
        self._matched_node_type = match_type

        if node is not None:
            self._matched_node_str = node.to_string(verbose=False)

        self._matched_node_words = []

        if node is not None and \
                (node.is_wildcard() or \
                 node.is_set() or \
                 node.is_iset() or \
                 node.is_bot() or \
                 node.is_regex()):
            self._matched_node_multi_word = True
        else:
            self._matched_node_multi_word = False

        if node is not None:
            self._matched_node_wildcard = node.is_wildcard()
        else:
            self._matched_node_wildcard = False

        if word is not None:
            self.add_word(word)

    def add_word(self, word):
        self._matched_node_words.append(word)

    @property
    def matched_node_type(self):
        return self._matched_node_type

    @matched_node_type.setter
    def matched_node_type(self, node_type):
        self._matched_node_type = node_type

    @property
    def matched_node_str(self):
        return self._matched_node_str

    @matched_node_str.setter
    def matched_node_str(self, node_str):
        self._matched_node_str = node_str

    @property
    def matched_node_multi_word(self):
        return self._matched_node_multi_word

    @matched_node_multi_word.setter
    def matched_node_multi_word(self, multi_word):
        self._matched_node_multi_word = multi_word

    @property
    def matched_node_wildcard(self):
        return self._matched_node_wildcard

    @matched_node_wildcard.setter
    def matched_node_wildcard(self, wildcard):
        self._matched_node_wildcard = wildcard

    @property
    def matched_node_words(self):
        return self._matched_node_words

    @matched_node_words.setter
    def matched_node_words(self, words):
        self._matched_node_words = words[:]

    def joined_words(self, client_context):
        return client_context.brain.tokenizer.words_to_texts(self._matched_node_words)

    @staticmethod
    def type_to_string(match_type):
        if match_type == Match.WORD:
            return "Word"
        elif match_type == Match.TOPIC:
            return "Topic"
        elif match_type == Match.THAT:
            return "That"
        return "Unknown"

    @staticmethod
    def string_to_type(match_type):
        if match_type == 'Word':
            return Match.WORD
        elif match_type == 'Topic':
            return Match.TOPIC
        elif match_type == 'That':
            return Match.THAT
        return -1

    def to_string(self, client_context):
        return "Match=(%s) Node=(%s) Matched=(%s)" % (Match.type_to_string(self.matched_node_type),
                                                      self.matched_node_str,
                                                      self.joined_words(client_context))

    def to_json(self):
        return {"type": Match.type_to_string(self.matched_node_type),
                "node": self.matched_node_str,
                "words": self.matched_node_words,
                "multi_word": self.matched_node_multi_word,
                "wild_card": self.matched_node_wildcard}

    @staticmethod
    def from_json(json_data):
        match = Match(0, None, None)

        match.matched_node_type = Match.string_to_type(json_data["type"])
        match.matched_node_str = json_data["node"]
        match.matched_node_words = json_data["words"]
        match.matched_node_multi_word = json_data["multi_word"]
        match.matched_node_wildcard = json_data["wild_card"]

        return match

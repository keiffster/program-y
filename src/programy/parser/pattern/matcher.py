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
from programy.parser.pattern.nodes import PatternNode
from programy.dialog import Sentence
from programy.bot import Bot

class MatchContext(object):
    def __init__(self):
        self.bot = None
        self.clientid = None
        self.pattern_sentence = None
        self.pattern_stars = []
        self.topic_sentence = None
        self.topic_stars = []
        self.that_sentence = None
        self.that_stars = []


class PatternMatcher(object):

    def __init__(self, graph, max_match_depth=1000):
        self._graph = graph
        self._max_match_depth = max_match_depth

    @property
    def graph(self):
        return self._graph

    def matches_to_stars(self, matches, stars):
        stars.clear()
        for match in matches:
            if len(match) > 0:
                matched = " ".join(match)
                if matched != "*":
                    stars.append(matched)

    def match(self,
              bot: Bot,
              clientid: str,
              pattern_sentence: Sentence,
              pattern_stars: list,
              topic_sentence: Sentence,
              topic_stars: list,
              that_sentence: Sentence,
              that_stars: list):
        logging.debug("Pattern matching sentence [%s],  topic[%s], that[%s]",
                      pattern_sentence.words_from_current_pos(0),
                      topic_sentence.words_from_current_pos(0),
                      that_sentence.words_from_current_pos(0))

        match_context = MatchContext()
        match_context.bot = bot
        match_context.clientid = clientid
        match_context.pattern_sentence = pattern_sentence
        match_context.topic_sentence = topic_sentence
        match_context.that_sentence = that_sentence

        matched_path = []
        matched_stars = []
        if self.match_children(match_context, self.graph.root, pattern_sentence, 0, matched_path, matched_stars,
                               0) is True:
            
            for match in match_context.pattern_stars:
                pattern_stars.append(match)

            for match in match_context.topic_stars:
                topic_stars.append(match)

            for match in match_context.that_stars:
                that_stars.append(match)

            return matched_path[0]

        return None

    def _get_tabs(self, depth: int):
        string = ""
        for i in range(depth):
            string += "\t"
        return string

    def end_of_sentence(self, match_context, root, sentence, num_word, matched_path, matched_stars, depth):

        tabs_str = self._get_tabs(depth)

        if root.has_zero_or_more():
            logging.debug("%sRoot has zero or more", tabs_str)
            if root.arrow is not None:
                if self.match_children(match_context, root.arrow, sentence, num_word + 1, matched_path,
                                       matched_stars, depth + 1) is True:
                    return True
            else:
                if self.match_children(match_context, root.hash, sentence, num_word + 1, matched_path,
                                       matched_stars, depth + 1) is True:
                    return True

        if root.has_topic():
            self.matches_to_stars(matched_stars, match_context.pattern_stars)
            matched_stars = []
            if self.match_children(match_context, root.topic, match_context.topic_sentence, 0, matched_path,
                                   matched_stars, 0) is True:
                return True

        elif root.has_that():
            self.matches_to_stars(matched_stars, match_context.topic_stars)
            matched_stars = []
            if self.match_children(match_context, root.that, match_context.that_sentence, 0, matched_path,
                                   matched_stars, 0) is True:
                return True

        elif root.has_template():
            logging.debug("%sRoot has template...[%s]", tabs_str, root.template.to_string())
            self.matches_to_stars(matched_stars, match_context.that_stars)
            matched_path.append(root.template)
            return True

        else:
            logging.debug("%sRoot has no topic, that or template, exiting...", tabs_str)
            return False

    def is_zero_or_more(self, match_context, root, sentence, num_word, matched_path, matched_stars, depth):

        tabs_str = self._get_tabs(depth)

        word = sentence.word(num_word)

        # added = False
        logging.debug("%sRoot is 0 or more", tabs_str)
        if root.has_wildcard():
            logging.debug("%sRoot next is wildcard", tabs_str)

            logging.debug("%s0ORM HAS. Adding (%s) to star match (%d)", tabs_str, word, len(matched_stars))
            # added = True
            matched_stars[len(matched_stars) - 1].append(word)
            matched_stars.append([])

            if root.hash is not None:
                if self.match_children(match_context, root.hash, sentence, num_word + 1, matched_path,
                                       matched_stars, depth + 1) is True:
                    return True
            elif root.arrow is not None:
                if self.match_children(match_context, root.arrow, sentence, num_word + 1, matched_path,
                                       matched_stars, depth + 1) is True:
                    return True
            else:
                raise Exception("Unknown zero or ore wild card")

                # if len(matched_stars) > 0:
                #    matched_stars.pop()

        else:
            for child in root.children:
                if child.matches(match_context.bot, match_context.clientid, word):

                    if child.is_set() or child.is_bot():
                        matched_stars.append([])
                        logging.debug("%sAdding new star match", tabs_str)
                        matched_stars[len(matched_stars) - 1].append(word)

                    logging.debug("%s0 or more matched child [%s] -> word [%s]", tabs_str, child.to_string(), word)
                    if self.match_children(match_context, child, sentence, num_word + 1, matched_path,
                                           matched_stars, depth + 1) is True:
                        return True

        logging.debug("%s0ORM. Adding (%s) to star match (%d)", tabs_str, word, len(matched_stars))
        # if added is False:
        # matched_stars.append([])
        logging.debug("%sAdding new star match", tabs_str)
        matched_stars[len(matched_stars) - 1].append(word)

        if self.match_children(match_context, root, sentence, num_word + 1, matched_path, matched_stars,
                               depth + 1) is True:
            return True

        if len(matched_stars) > 0:
            matched_stars.pop()

        return False

    def is_one_or_more(self, match_context, root, sentence, num_word, matched_path, matched_stars, depth):

        tabs_str = self._get_tabs(depth)

        word = sentence.word(num_word)

        logging.debug("%sRoot is one or more", tabs_str)
        if root.has_wildcard():
            logging.debug("%sRoot next is wildcard", tabs_str)

            logging.debug("%s1ORM HAS. Adding (%s) to star match (%d)", tabs_str, word, len(matched_stars))
            matched_stars.append([])
            matched_stars[len(matched_stars) - 1].append(word)

            if root.underline is not None:
                if self.match_children(match_context, root.underline, sentence, num_word + 1, matched_path,
                                       matched_stars, depth + 1) is True:
                    return True
            if root.star is not None:
                if self.match_children(match_context, root.star, sentence, num_word + 1, matched_path,
                                       matched_stars, depth + 1) is True:
                    return True
            else:
                raise Exception("Unknown one or ore wild card")

            if len(matched_stars) > 0:
                matched_stars.pop()

        else:
            for child in root.children:
                if child.matches(match_context.bot, match_context.clientid, word):

                    if child.is_set() or child.is_bot():
                        matched_stars.append([])
                        logging.debug("%sAdding new star match", tabs_str)
                        matched_stars[len(matched_stars) - 1].append(word)

                    logging.debug("%s1 or more matched child [%s] -> word [%s]", tabs_str, child.to_string(), word)
                    if self.match_children(match_context, child, sentence, num_word + 1, matched_path, matched_stars,
                                           depth + 1) is True:
                        return True

            logging.debug("%s1ORM Adding (%s) to star match (%d)", tabs_str, word, len(matched_stars))
            matched_stars[len(matched_stars) - 1].append(word)

            if self.match_children(match_context, root, sentence, num_word + 1, matched_path, matched_stars,
                                   depth + 1) is True:
                return True

            if len(matched_stars) > 0:
                matched_stars.pop()

        return False

    def match_children(self, match_context: MatchContext, root: PatternNode, sentence: Sentence, num_word: int,
                       matched_path: list, matched_stars: list, depth: int):

        tabs_str = self._get_tabs(depth)

        if depth > self._max_match_depth:
            logging.debug("%sMax recursive depth reached [%d]", tabs_str, self._max_match_depth)
            return False

        if num_word >= sentence.num_words():
            return self.end_of_sentence(match_context, root, sentence, num_word, matched_path, matched_stars, depth)

        if root.is_zero_or_more():
            result = self.is_zero_or_more(match_context, root, sentence, num_word, matched_path, matched_stars, depth)
            if result is True:
                return True

        if root.is_one_or_more():
            result = self.is_one_or_more(match_context, root, sentence, num_word, matched_path, matched_stars, depth)
            if result is True:
                return True

        #########################################################################################################
        # Order = $  # _ word ^ *

        word = sentence.word(num_word)

        if root.has_priority_words():
            logging.debug("%sRoot has priority", tabs_str)
            for child in root.priority_words:
                if child.matches(match_context.bot, match_context.clientid, word):

                    if child.is_set() or child.is_bot():
                        matched_stars.append([])
                        logging.debug("%sAdding new star match", tabs_str)
                        matched_stars[len(matched_stars) - 1].append(word)

                    logging.debug("%sPriority matched child [%s] -> word [%s]", tabs_str, child.to_string(), word)
                    if self.match_children(match_context, child, sentence, num_word+1, matched_path, matched_stars,
                                           depth+1) is True:
                        return True

        if root.has_zero_or_more():
            if num_word <= sentence.num_words():

                if root.hash is not None:
                    logging.debug("%sRoot is 0 or more", tabs_str)
                    matched_stars.append([])

                    logging.debug("%sMatching child [#] -> word [%s]", tabs_str, word)
                    if self.match_children(match_context, root.hash, sentence, num_word, matched_path, matched_stars,
                                           depth+1) is True:
                        return True

                    if len(matched_stars) > 0:
                        matched_stars.pop()

        if root.has_one_or_more():
            if num_word < sentence.num_words():
                if root.underline is not None:
                    logging.debug("%sRoot has 1 or more", tabs_str)

                    logging.debug("%sHAS 1ORM Adding (%s) to star match (%d)", tabs_str, word, len(matched_stars))
                    matched_stars.append([])
                    matched_stars[len(matched_stars) - 1].append(word)

                    logging.debug("%sMatching child [_] -> word [%s]", tabs_str, word)
                    if self.match_children(match_context, root.underline, sentence, num_word+1, matched_path,
                                           matched_stars, depth+1) is True:
                        return True

                    if len(matched_stars) > 0:
                        matched_stars.pop()

        if root.has_children():
            logging.debug("%sRoot has children (%d)", tabs_str, depth)
            for child in root.children:
                if child.matches(match_context.bot, match_context.clientid, word):

                    if child.is_set() or child.is_bot():
                        matched_stars.append([])
                        logging.debug("%sAdding new star match", tabs_str)
                        matched_stars[len(matched_stars) - 1].append(word)

                    logging.debug("%sMatched child [%s] -> word [%s]", tabs_str, child.to_string(), word)
                    if self.match_children(match_context, child, sentence, num_word+1, matched_path, matched_stars,
                                           depth+1) is True:
                        return True

        if root.has_zero_or_more():
            if num_word <= sentence.num_words():
                if root.arrow is not None:
                    logging.debug("%sRoot is 0 or more", tabs_str)
                    matched_stars.append([])

                    logging.debug("%sMatching child [^] -> word [%s]", word, tabs_str)
                    if self.match_children(match_context, root.arrow, sentence, num_word, matched_path, matched_stars,
                                           depth+1) is True:
                        return True

                    if len(matched_stars) > 0:
                        matched_stars.pop()

        if root.has_one_or_more():
            if num_word < sentence.num_words():
                if root.star is not None:
                    logging.debug("%sRoot has 1 or more", tabs_str)
                    logging.debug("%sHAS 1ORM Adding (%s) to star match (%d)", tabs_str, word, len(matched_stars))
                    matched_stars.append([])
                    matched_stars[len(matched_stars) - 1].append(word)

                    logging.debug("%sMatching child [*] -> word [%s]", tabs_str, word)
                    if self.match_children(match_context, root.star, sentence, num_word+1, matched_path,
                                           matched_stars, depth+1) is True:
                        return True

                    if len(matched_stars) > 0:
                        matched_stars.pop()

        logging.debug("%sNo match", tabs_str)
        matched_stars.clear()
        matched_stars.append([])
        return False

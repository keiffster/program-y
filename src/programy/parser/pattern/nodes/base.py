"""
Copyright (c) 2016-17 Keith Sterling http://www.keithsterling.com

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

from programy.utils.text.text import TextUtils
from programy.parser.pattern.matcher import Match, EqualsMatch
import datetime

#######################################################################################################################
#
class PatternNode(object):

    THAT = "__THAT__"
    TOPIC = "__TOPIC__"

    def __init__(self):

        # Child Nodes
        self._priority_words = []
        self._0ormore_hash = None
        self._1ormore_underline = None
        self._children = []
        self._children_words = {}
        self._iset_names = {}
        self._set_names = {}
        self._bot_properties = {}
        self._0ormore_arrow = None
        self._1ormore_star = None

        # Topic, That and Template Nodes
        self._topic = None
        self._that = None
        self._template = None

    ########################################################################
    #
    def is_root(self):
        return False

    ########################################################################
    #
    @property
    def priority_words(self):
        return self._priority_words

    def has_priority_words(self):
        return True if len(self._priority_words) > 0 else False

    def is_priority(self):
        return False

    ########################################################################
    #
    @property
    def arrow(self):
        return self._0ormore_arrow

    @property
    def hash(self):
        return self._0ormore_hash

    @property
    def underline(self):
        return self._1ormore_underline

    @property
    def star(self):
        return self._1ormore_star

    def has_wildcard(self):
        if self.has_zero_or_more() is True or self.has_one_or_more():
            return True
        return False

    def has_zero_or_more(self):
        if self._0ormore_arrow is not None or self._0ormore_hash is not None:
            return True
        else:
            return False

    def has_0ormore_arrow(self):
        return bool(self._0ormore_arrow is not None)

    def has_0ormore_hash(self):
        return bool(self._0ormore_hash is not None)

    def has_one_or_more(self):
        if self._1ormore_star is not None or self._1ormore_underline is not None:
            return True
        else:
            return False

    def has_1ormore_star(self):
        return bool(self._1ormore_star is not None)

    def has_1ormore_underline(self):
        return bool(self._1ormore_underline is not None)

    def is_wildcard(self):
        return False

    def is_zero_or_more(self):
        return False

    def is_one_or_more(self):
        return False

    def is_word(self):
        return False

    ########################################################################
    #
    @property
    def children(self):
        return self._children

    def child(self, num):
        return self._children[num]

    def has_children(self):
        if len(self._children) > 0:
            return True

        return False

    def has_nodes(self):
        if len(self._children) > 0:
            return True

        if self.has_priority_words():
            return True

        if self.has_wildcard():
            return True

        return False

    ########################################################################
    #
    @property
    def topic(self):
        return self._topic

    def is_topic(self):
        return False

    def has_topic(self):
        return bool(self.topic is not None)

    def add_topic(self, topic):
        if self.has_topic() is False:
            self._topic = topic
        return self._topic

    ########################################################################
    #
    @property
    def that(self):
        return self._that

    def add_that(self, that):
        if self.has_that() is False:
            self._that = that
        return self._that

    def is_that(self):
        return False

    def has_that(self):
        return bool(self.that is not None)

    ########################################################################
    #
    @property
    def template(self):
        return self._template

    def is_template(self):
        return False

    def has_template(self):
        return bool(self.template is not None)

    def add_template(self, template):
        if self.has_template() is False:
            self._template = template
        return self._template

    ########################################################################
    #
    def is_set(self):
        return False

    def is_iset(self):
        return False

    ########################################################################
    #
    def is_bot(self):
        return False

    ########################################################################
    #
    def equivalent(self, other):
        return False

    def equals(self, bot, clientid, words, word_no):
        return EqualsMatch(False, word_no)

    def equals_ignore_case(self, bot, client, word1, word2):
        if word1 is not None and word2 is not None:
            return bool(word1.upper() == word2.upper())
        return False

    ########################################################################
    #
    def can_add(self, new_node):
        pass

    def _node_exists(self, new_node):

        for priority in self._priority_words:
            if priority.equivalent(new_node):
                # Equivalent node already exists, use this one instead
                return priority

        if new_node.is_zero_or_more() is True:
            if self._0ormore_arrow is not None:
                if self._0ormore_arrow.equivalent(new_node):
                    return self._0ormore_arrow
            if self._0ormore_hash is not None:
                if self._0ormore_hash.equivalent(new_node):
                    return self._0ormore_hash

        if new_node.is_one_or_more() is True:
            if self._1ormore_underline is not None:
                if self._1ormore_underline.equivalent(new_node):
                    return self._1ormore_underline
            if self._1ormore_star is not None:
                if self._1ormore_star.equivalent(new_node):
                    return self._1ormore_star

        if new_node.is_topic() is True:
            if self._topic is not None:
                if self._topic.equivalent(new_node):
                    return self._topic

        if new_node.is_that():
            if self._that is not None:
                if self._that.equivalent(new_node):
                    return self._that

        if new_node.is_iset() is True:
            return None

        if new_node.is_set() is True:
            if new_node.set_name in self._set_names:
                existing_node = self._set_names[new_node.set_name]
                if existing_node.is_word:
                    if existing_node.equivalent(new_node):
                        # Equivalent node already exists, use this one instead
                        return existing_node

        if new_node.is_bot() is True:
            if new_node.property in self._bot_properties:
                existing_node = self._bot_properties[new_node.property]
                if existing_node.is_word:
                    if existing_node.equivalent(new_node):
                        # Equivalent node already exists, use this one instead
                        return existing_node

        if new_node.is_word():
            if new_node.word in self._children_words:
                existing_node = self._children_words[new_node.word]
                if existing_node.is_word:
                    if existing_node.equivalent(new_node):
                        # Equivalent node already exists, use this one instead
                        return existing_node

        return None

    def _add_node(self, new_node):
        # Otherwise use the new node, and return that to maintain consistence
        # And allow child node to be chained, but supports duplicates
        if new_node.is_priority():
            self._priority_words.append(new_node)
        elif new_node.is_zero_or_more():
            if new_node.wildcard == '^':
                self._0ormore_arrow = new_node
            elif new_node.wildcard == '#':
                self._0ormore_hash = new_node
        elif new_node.is_one_or_more():
            if new_node.wildcard == '_':
                self._1ormore_underline = new_node
            elif new_node.wildcard == '*':
                self._1ormore_star = new_node
        elif new_node.is_template():
            self._template = new_node
        else:
            # Append sets and bots to the end of the array as they take a slightly
            # lower priority to actual words.
            # This allows the following to work
            #  my favorite color is green
            #  my favorite color is <set>color</set>
            # In the above, if the set color contains green then
            # it still gets picked up in the first grammar and not he second
            if new_node.is_set():
                self.children.append(new_node)
                self._set_names[new_node.set_name] = new_node
            elif new_node.is_iset():
                self.children.append(new_node)
                self._iset_names[new_node.iset_name] = new_node
            elif new_node.is_bot():
               self.children.append(new_node)
               self._bot_properties[new_node.property] = new_node
            else:
                self.children.insert(0, new_node)
                if new_node.is_word():
                    self._children_words[new_node.word] = new_node

        return new_node

    def add_child(self, new_node):

        # Check the rules allow this now to be a child of the current node
        self.can_add(new_node)

        # Next check for duplicates, returning original if one exists
        exists = self._node_exists(new_node)
        if exists is not None:
            return exists

        # Otherwise add the new node to the appropriate container
        result = self._add_node(new_node)
        return result

    def _child_count(self, verbose=True):
        if verbose is True:
            return "P(%d)^(%d)#(%d)C(%d)_(%d)*(%d)To(%d)Th(%d)Te(%d)" % (
                len(self._priority_words),
                1 if self._0ormore_arrow is not None else 0,
                1 if self._0ormore_hash is not None else 0,
                len(self.children),
                1 if self._1ormore_underline is not None else 0,
                1 if self._1ormore_star is not None else 0,
                1 if self._topic is not None else 0,
                1 if self._that is not None else 0,
                1 if self._template is not None else 0
            )
        else:
            return ""

    def to_string(self, verbose=True):
        if verbose is True:
            return "NODE [%s]" % self._child_count(verbose)
        else:
            return "NODE"

    def dump(self, tabs, output_func=logging.debug, eol="", verbose=True):

        output_func("%s%s%s" % (tabs, self.to_string(verbose), eol))

        for priority in self._priority_words:
            priority.dump(tabs+"\t", output_func, eol, verbose)

        if self._0ormore_arrow is not None:
            self._0ormore_arrow.dump(tabs+"\t", output_func, eol, verbose)
        if self._0ormore_hash is not None:
            self._0ormore_hash.dump(tabs+"\t", output_func, eol, verbose)
        if self._1ormore_underline is not None:
            self._1ormore_underline.dump(tabs+"\t", output_func, eol, verbose)
        if self._1ormore_star is not None:
            self._1ormore_star.dump(tabs+"\t", output_func, eol, verbose)
        if self._topic is not None:
            self._topic.dump(tabs+"\t", output_func, eol, verbose)
        if self._that is not None:
            self._that.dump(tabs+"\t", output_func, eol, verbose)
        if self._template is not None:
            self._template.dump(tabs+"\t", output_func, eol, verbose)

        for child in self.children:
            child.dump(tabs+"\t", output_func, eol, verbose)

    def match_children(self, bot, clientid, children, child_type, words, word_no, context, type, depth):

        tabs = TextUtils.get_tabs(depth)

        for child in children:

            result = child.equals(bot, clientid, words, word_no)
            if result.matched is True:
                word_no = result.word_no
                logging.debug("%s%s matched %s" % (tabs, child_type, result.matched_phrase))

                match_node = Match(type, child, result.matched_phrase)

                context.add_match(match_node)

                match = child.consume(bot, clientid, context, words, word_no + 1, type, depth+1)
                if match is not None:
                    logging.debug("%sMatched %s child, success!" % (tabs, child_type))
                    return match, word_no
                else:
                    context.pop_match ()

        return None, word_no

    def consume(self, bot, clientid, context, words, word_no, type, depth):

        tabs = TextUtils.get_tabs(depth)

        if context.search_time_exceeded() is True:
            logging.error("%sMax search time [%d]secs exceeded" % (tabs, context.max_search_time))
            return None

        if context.search_depth_exceeded(depth) is True:
            logging.error("%sMax search depth [%d] exceeded" % (tabs, context.max_search_depth))
            return None

        if word_no >= words.num_words():
            if self._template is not None:
                logging.debug("%sFound a template, success!" % (tabs))
                return self._template
            else:
                logging.debug("%sNo more words and no template, no match found!" % (tabs))
                #context.pop_match()
                return None

        if self._topic is not None:
            match = self._topic.consume(bot, clientid, context, words, word_no, Match.TOPIC, depth+1)
            if match is not None:
                logging.debug("%sMatched topic, success!" % (tabs))
                return match
            if words.word(word_no) == PatternNode.TOPIC:
                logging.debug("%s Looking for a %s, none give, no match found!" % (tabs, PatternNode.TOPIC))
                return None

        if self._that is not None:
            match = self._that.consume(bot, clientid, context, words, word_no, Match.THAT, depth+1)
            if match is not None:
                logging.debug("%sMatched that, success!" % (tabs))
                return match
            if words.word(word_no) == PatternNode.THAT:
                logging.debug("%s Looking for a %s, none give, no match found!" % (tabs, PatternNode.THAT))
                return None

        match, word_no = self.match_children(bot, clientid, self._priority_words, "Priority", words, word_no, context, type, depth)
        if match is not None:
            return match

        if self._0ormore_hash is not None:
            match = self._0ormore_hash.consume(bot, clientid, context, words, word_no, type, depth+1)
            if match is not None:
                logging.debug("%sMatched 0 or more hash, success!" % (tabs))
                return match

        if self._1ormore_underline is not None:
            match = self._1ormore_underline.consume(bot, clientid, context, words, word_no, type, depth+1)
            if match is not None:
                logging.debug("%sMatched 1 or more underline, success!" % (tabs))
                return match

        match, word_no = self.match_children(bot, clientid, self._children, "Word", words, word_no, context, type, depth)
        if match is not None:
            return match

        if self._0ormore_arrow is not None:
            match = self._0ormore_arrow.consume(bot, clientid, context, words, word_no, type, depth+1)
            if match is not None:
                logging.debug("%sMatched 0 or more arrow, success!" % (tabs))
                return match

        if self._1ormore_star is not None:
            match = self._1ormore_star.consume(bot, clientid, context, words, word_no, type, depth+1)
            if match is not None:
                logging.debug("%sMatched 1 or more star, success!" % (tabs))
                return match

        logging.debug("%sNo match for %s, trying another path" % (tabs, words.word(word_no)))
        return None


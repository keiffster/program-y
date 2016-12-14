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
from programy.parser.exceptions import ParserException


#######################################################################################################################
#
class PatternNode(object):

    def __init__(self):
        self._priority_words = []
        self._0ormore_arrow = None
        self._0ormore_hash = None
        self._children = []
        self._1ormore_underline = None
        self._1ormore_star = None
        self._topic = None
        self._that = None
        self._template = None

    @property
    def priority_words(self):
        return self._priority_words

    @property
    def arrow(self):
        return self._0ormore_arrow

    @property
    def hash(self):
        return self._0ormore_hash

    @property
    def children(self):
        return self._children

    def child(self, num):
        return self._children[num]

    @property
    def underline(self):
        return self._1ormore_underline

    @property
    def star(self):
        return self._1ormore_star

    @property
    def topic(self):
        return self._topic

    @property
    def template(self):
        return self._template

    @property
    def that(self):
        return self._that

    def is_root(self):
        return False

    def is_priority(self):
        return False

    def is_wildcard(self):
        return False

    def is_zero_or_more(self):
        return False

    def is_one_or_more(self):
        return False

    def is_set(self):
        return False

    def is_bot(self):
        return False

    def is_template(self):
        return False

    def has_priority_words(self):
        return True if len(self._priority_words) > 0 else False

    def has_wildcard(self):
        if self.has_zero_or_more() is True or self.has_one_or_more():
            return True
        return False

    def has_zero_or_more(self):
        if self._0ormore_arrow is not None or self._0ormore_hash is not None:
            return True

    def has_one_or_more(self):
        if self._1ormore_star is not None or self._1ormore_underline is not None:
            return True

    def has_topic(self):
        return bool(self.topic is not None)

    def add_topic(self, topic):
        if self.has_topic() is False:
            self._topic = topic
        return self._topic

    def add_that(self, that):
        if self.has_that() is False:
            self._that = that
        return self._that

    def has_that(self):
        return bool(self.that is not None)

    def has_template(self):
        return bool(self.template is not None)

    def add_template(self, template):
        if self.has_template() is False:
            self._template = template
        return self._template

    def has_children(self):
        if len(self._children) > 0:
            return True

        if self.has_priority_words():
            return True

        if self.has_wildcard():
            return True

        return False

    def equivalent(self, other):
        return False

    def equals(self, bot, clientid, word):
        return False

    def matches(self, bot, clientid, word):
        return False

    def can_add(self, new_node):
        pass

    def _node_exists(self, new_node):

        for priority in self._priority_words:
            if priority.equivalent(new_node):
                # Equivalent node already exists, use this one insead
                return priority

        if self._0ormore_arrow is not None:
            if self._0ormore_arrow.equivalent(new_node):
                return self._0ormore_arrow
        if self._0ormore_hash is not None:
            if self._0ormore_hash.equivalent(new_node):
                return self._0ormore_hash

        if self._1ormore_underline is not None:
            if self._1ormore_underline.equivalent(new_node):
                return self._1ormore_underline
        if self._1ormore_star is not None:
            if self._1ormore_star.equivalent(new_node):
                return self._1ormore_star

        if self._topic is not None:
            if self._topic.equivalent(new_node):
                return self._topic

        if self._that is not None:
            if self._that.equivalent(new_node):
                return self._that

        for child in self.children:
            if child.equivalent(new_node):
                return child

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
            self.children.append(new_node)
        return new_node

    def add_child(self, new_node):

        # Check the rules allow this now to be a child of the current node
        self.can_add(new_node)

        # Next check for duplicates, returning original if one exists
        exists = self._node_exists(new_node)
        if exists is not None:
            return exists

        # Otherwise add the new node to the appropriate container
        return self._add_node(new_node)

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
        return "NODE [%s]" % self._child_count(verbose)

    def dump(self, tabs, output_func=logging.debug, verbose=True):

        output_func("%s%s" % (tabs, self.to_string(verbose)))

        for priority in self._priority_words:
            priority.dump(tabs+"\t", output_func, verbose)
        if self._0ormore_arrow is not None:
            self._0ormore_arrow.dump(tabs+"\t", output_func, verbose)
        if self._0ormore_hash is not None:
            self._0ormore_hash.dump(tabs+"\t", output_func, verbose)
        if self._1ormore_underline is not None:
            self._1ormore_underline.dump(tabs+"\t", output_func, verbose)
        if self._1ormore_star is not None:
            self._1ormore_star.dump(tabs+"\t", output_func, verbose)
        if self._topic is not None:
            self._topic.dump(tabs+"\t", output_func, verbose)
        if self._that is not None:
            self._that.dump(tabs+"\t", output_func, verbose)
        if self._template is not None:
            self._template.dump(tabs+"\t", output_func, verbose)
        for child in self.children:
            child.dump(tabs+"\t", output_func, verbose)


#######################################################################################################################
#
class PatternRootNode(PatternNode):

    def __init__(self):
        PatternNode.__init__(self)

    def is_root(self):
        return True

    def can_add(self, new_node: PatternNode):
        if isinstance(new_node, PatternRootNode):
            raise ParserException("Cannot add root node to existing root node")
        if isinstance(new_node, PatternTopicNode):
            raise ParserException("Cannot add topic node to root node")
        if isinstance(new_node, PatternThatNode):
            raise ParserException("Cannot add that node to root node")
        if isinstance(new_node, PatternTemplateNode):
            raise ParserException("Cannot add template node to root node")

    def equivalent(self, other: PatternNode)->bool:
        if isinstance(other, PatternRootNode):
            return True
        return False

    def to_string(self, verbose: bool=True)->str:
        return "ROOT [%s]" % self._child_count(verbose)


#######################################################################################################################
#
class PatternTopicNode(PatternNode):

    def __init__(self):
        PatternNode.__init__(self)

    def can_add(self, new_node):
        if isinstance(new_node, PatternRootNode):
            raise ParserException("Cannot add root node to topic node")
        if isinstance(new_node, PatternTopicNode):
            raise ParserException("Cannot add topic node to topic node")
        if isinstance(new_node, PatternThatNode):
            raise ParserException("Cannot add that node to topic node")

    def equivalent(self, other):
        if isinstance(other, PatternTopicNode):
            return True
        return False

    def to_string(self, verbose=True):
        return "TOPIC [%s]" % self._child_count(verbose)


#######################################################################################################################
#
class PatternThatNode(PatternNode):

    def __init__(self):
        PatternNode.__init__(self)

    def can_add(self, new_node):
        if isinstance(new_node, PatternRootNode):
            raise ParserException("Cannot add root node to that node")
        if isinstance(new_node, PatternTopicNode):
            raise ParserException("Cannot add topic node to that node")
        if isinstance(new_node, PatternThatNode):
            raise ParserException("Cannot add that node to that node")

    def equivalent(self, other):
        if isinstance(other, PatternThatNode):
            return True
        return False

    def to_string(self, verbose=True):
        return "THAT [%s]" % self._child_count(verbose)


#######################################################################################################################
#
class PatternTemplateNode(PatternNode):

    def __init__(self, template):
        PatternNode.__init__(self)
        self._template = template

    @property
    def template(self):
        return self._template

    def is_template(self):
        return True

    def can_add(self, new_node):
        if isinstance(new_node, PatternRootNode):
            raise ParserException("Cannot add root node to template node")
        if isinstance(new_node, PatternTopicNode):
            raise ParserException("Cannot add topic node to template node")
        if isinstance(new_node, PatternThatNode):
            raise ParserException("Cannot add that node to template node")
        if isinstance(new_node, PatternTemplateNode):
            raise ParserException("Cannot add template node to template node")

    def equivalent(self, other):
        if isinstance(other, PatternTemplateNode):
            return True
        return False

    def to_string(self, verbose=True):
        return "PTEMPLATE [%s] " % (self._child_count(verbose))


#######################################################################################################################
#
class PatternWordNode(PatternNode):

    def __init__(self, word):
        PatternNode.__init__(self)
        self._word = word

    @property
    def word(self):
        return self._word

    def can_add(self, new_node):
        if isinstance(new_node, PatternRootNode):
            raise ParserException("Cannot add root node to child node")

    def matches(self, bot, clientid, word):
        if self._word == word:
            return True
        return False

    def equivalent(self, other):
        if isinstance(other, PatternWordNode):
            if self._word == other.word:
                return True
        return False

    def equals(self, bot, clientid, word):
        if self.word == word:
            return True
        return False

    def to_string(self, verbose=True):
        return "WORD [%s] word=[%s]" % (self._child_count(verbose), self.word)


#######################################################################################################################
#
class PatternPriorityWordNode(PatternWordNode):

    def __init__(self, word):
        PatternWordNode.__init__(self, word)

    def is_priority(self):
        return True

    def equivalent(self, other):
        if isinstance(other, PatternPriorityWordNode):
            if self.word == other.word:
                return True
        return False

    def equals(self, bot, clientid, word):
        if self._word == word:
            return True
        return False

    def matches(self, bot, clientid, word):
        if self._word == word:
            return True
        return False

    def to_string(self, verbose=True):
        return "PWORD [%s] word=[%s]" % (self._child_count(verbose), self.word)


#######################################################################################################################
#
class PatternSetNode(PatternWordNode):

    def __init__(self, word):
        PatternWordNode.__init__(self, word.upper())

    @property
    def set_name(self):
        return self.word

    def is_set(self):
        return True

    def equivalent(self, other):
        if isinstance(other, PatternSetNode):
            if self._word == other.word:
                return True
        return False

    def equals(self, bot, client, word):
        if bot.brain.sets.contains(self.set_name):
            logging.debug("Looking for [%s] in set [%s]", word, self.set_name)
            set_words = bot.brain.sets.set(self.set_name)
            if word in set_words:
                logging.debug("Found a word [%s] in set [%s]", word, self.set_name)
                return True
        return False

    def matches(self, bot, clientid, word):
        return self.equals(bot, clientid, word)

    def to_string(self, verbose=True):
        return "SET [%s] name=[%s]" % (self._child_count(verbose), self.word)


#######################################################################################################################
#
class PatternBotNode(PatternWordNode):

    def __init__(self, word):
        PatternWordNode.__init__(self, word)

    def is_bot(self):
        return True

    def equivalent(self, other):
        if isinstance(other, PatternBotNode):
            if self._word == other.word:
                return True
        return False

    def equals(self, bot, clientid, word):
        if bot.brain.properties.has_property(self.word):
            if word == bot.brain.properties.property(self.word):
                return True
        return False

    def matches(self, bot, clientid, word):
        return self.equals(bot, clientid, word)

    def to_string(self, verbose=True):
        return "BOT [%s] property=[%s]" % (self._child_count(verbose), self.word)


#######################################################################################################################
#
class PatternWildCardNode(PatternNode):

    def __init__(self, wildcard):
        PatternNode.__init__(self)
        if wildcard not in self.matching_wildcards():
            raise ParserException("%s not in valid wildcards %s" % (wildcard, ", ".join(self.matching_wildcards())))
        self._wildcard = wildcard

    def is_wildcard(self):
        return True

    def can_add(self, new_node):
        if isinstance(new_node, PatternRootNode):
            raise ParserException("Cannot add root node to child node")

    def has_child_match(self, bot, clientid, next_word):

        for priority in self._priority_words:
            if priority.equals(bot, clientid, next_word):
                return priority

        if self._0ormore_arrow is not None:
            return self._0ormore_arrow

        if self._0ormore_hash is not None:
            return self._0ormore_hash

        for child in self.children:
            if child.equals(bot, clientid, next_word):
                return child

        if self._1ormore_underline is not None:
            return self._1ormore_underline

        if self._1ormore_star is not None:
            return self._1ormore_star

        return None

    @property
    def wildcard(self):
        return self._wildcard

    def matching_wildcards(self):
        return []


#######################################################################################################################
#
class PatternZeroOrMoreWildCardNode(PatternWildCardNode):

    MATCH_CHARS = ['^', '#']

    def __init__(self, wildcard):
        PatternWildCardNode.__init__(self, wildcard)

    def is_zero_or_more(self):
        return True

    def matching_wildcards(self):
        return PatternZeroOrMoreWildCardNode.MATCH_CHARS

    @staticmethod
    def is_wild_card(text):
        return bool(text in PatternZeroOrMoreWildCardNode.MATCH_CHARS)

    def equivalent(self, other):
        if isinstance(other, PatternZeroOrMoreWildCardNode):
            if self._wildcard == other.wildcard:
                return True
        return False

    def to_string(self, verbose=True):
        return "ZEROORMORE [%s] wildcard=[%s]" % (self._child_count(verbose), self.wildcard)


#######################################################################################################################
#
class PatternOneOrMoreWildCardNode(PatternWildCardNode):

    MATCH_CHARS = ['_', '*']

    def __init__(self, wildcard):
        PatternWildCardNode.__init__(self, wildcard)

    def is_one_or_more(self):
        return True

    def matching_wildcards(self):
        return PatternOneOrMoreWildCardNode.MATCH_CHARS

    @staticmethod
    def is_wild_card(text):
        return bool(text in PatternOneOrMoreWildCardNode.MATCH_CHARS)

    def equivalent(self, other):
        if isinstance(other, PatternOneOrMoreWildCardNode):
            if self._wildcard == other.wildcard:
                return True
        return False

    def to_string(self, verbose=True):
        return "ONEORMORE [%s] wildcard=[%s]" % (self._child_count(verbose), self.wildcard)

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
from programy.utils.text.text import TextUtils
from programy.parser.pattern.matcher import Match

#######################################################################################################################
#
class PatternNode(object):

    def __init__(self):

        # Child Nodes
        self._priority_words = []
        self._0ormore_hash = None
        self._1ormore_underline = None
        self._children = []
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

    ########################################################################
    #
    def is_bot(self):
        return False

    ########################################################################
    #
    def equivalent(self, other):
        return False

    def equals(self, bot, clientid, word):
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
        if verbose is True:
            return "NODE [%s]" % self._child_count(verbose)
        else:
            return "NODE"

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

    def consume(self, bot, clientid, context, words, word_no, type, depth):

        tabs = TextUtils.get_tabs(word_no)

        if depth > context.max_search_depth:
            logging.error("%sMax search depth [%d]exceeded" % (tabs, context.max_search_depth))
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
                return match
            if words.word(word_no) == PatternTopicNode.TOPIC:
                logging.debug("%sLooking for a %s, none give, no match found!" % (PatternTopicNode.TOPIC, tabs))
                #context.pop_match()
                return None

        if self._that is not None:
            match = self._that.consume(bot, clientid, context, words, word_no, Match.THAT, depth+1)
            if match is not None:
                return match
            if words.word(word_no) == PatternThatNode.THAT:
                logging.debug("%sLooking for a %s, none give, no match found!" % (PatternThatNode.THAT, tabs))
                #context.pop_match()
                return None

        for child in self._priority_words:
            if child.equals(bot, clientid, words.word(word_no)):
                logging.debug("%sPriority %s matched %s" % (tabs, child._word, words.word(word_no)))

                logging.debug("%sMATCH -> %s" % (tabs, words.word(word_no)))
                match_node = Match(type, child, words.word(word_no))
                context.add_match(match_node)

                match = child.consume(bot, clientid, context, words, word_no + 1, type, depth+1)
                if match is not None:
                    return match
                else:
                    context.pop_match ()

        if self._0ormore_hash is not None:
            match = self._0ormore_hash.consume(bot, clientid, context, words, word_no, type, depth+1)
            if match is not None:
                return match
            #else:
            #    context.pop_match ()

        if self._1ormore_underline is not None:
            match = self._1ormore_underline.consume(bot, clientid, context, words, word_no, type, depth+1)
            if match is not None:
                return match
            #else:
            #    context.pop_match ()

        for child in self._children:
            if child.equals(bot, clientid, words.word(word_no)):
                logging.debug("%sChild %s matched %s" % (tabs, child._word, words.word(word_no)))

                logging.debug("%sMATCH -> %s" % (tabs, words.word(word_no)))
                match_node = Match(type, child, words.word(word_no))
                context.add_match(match_node)

                match = child.consume(bot, clientid, context, words, word_no + 1, type, depth+1)
                if match is not None:
                    return match
                else:
                    context.pop_match ()

        if self._0ormore_arrow is not None:
            match = self._0ormore_arrow.consume(bot, clientid, context, words, word_no, type, depth+1)
            if match is not None:
                return match
            #else:
            #    context.pop_match ()

        if self._1ormore_star is not None:
            match = self._1ormore_star.consume(bot, clientid, context, words, word_no, type, depth+1)
            if match is not None:
                return match
            #else:
            #    context.pop_match ()

        logging.debug("%sNo match for %s, trying another path" % (tabs, words.word(word_no)))
        return None


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
        if verbose is True:
            return "ROOT [%s]" % self._child_count(verbose)
        else:
            return "ROOT "

    def match(self, bot, clientid, context, words):
        return self.consume(bot, clientid, context, words, 0, Match.WORD, 0)

#######################################################################################################################
#
class PatternTopicNode(PatternNode):

    TOPIC = "__TOPIC__"

    def __init__(self):
        PatternNode.__init__(self)

    def can_add(self, new_node):
        if isinstance(new_node, PatternRootNode):
            raise ParserException("Cannot add root node to topic node")
        if isinstance(new_node, PatternTopicNode):
            raise ParserException("Cannot add topic node to topic node")
        if isinstance(new_node, PatternThatNode):
            raise ParserException("Cannot add that node to topic node")

    def is_topic(self):
        return True

    def equivalent(self, other):
        if isinstance(other, PatternTopicNode):
            return True
        return False

    def to_string(self, verbose=True):
        if verbose is True:
            return "TOPIC [%s]" % self._child_count(verbose)
        else:
            return "TOPIC"

    def consume(self, bot, clientid, context, words, word_no, type, depth):

        tabs = TextUtils.get_tabs(word_no)

        if depth > context.max_search_depth:
            logging.error("%sMax search depth [%d]exceeded" % (tabs, context.max_search_depth))
            return None

        if words.word(word_no) == PatternTopicNode.TOPIC:
            logging.debug("%sTopic matched %s" % (tabs, words.word(word_no)))
            return super(PatternTopicNode, self).consume(bot, clientid, context, words, word_no+1, type, depth+1)

        logging.debug("%sTopic NOT matched %s" % (tabs, words.word(word_no)))
        return None

#######################################################################################################################
#
class PatternThatNode(PatternNode):

    THAT = "__THAT__"

    def __init__(self):
        PatternNode.__init__(self)

    def can_add(self, new_node):
        if isinstance(new_node, PatternRootNode):
            raise ParserException("Cannot add root node to that node")
        if isinstance(new_node, PatternTopicNode):
            raise ParserException("Cannot add topic node to that node")
        if isinstance(new_node, PatternThatNode):
            raise ParserException("Cannot add that node to that node")

    def is_that(self):
        return True

    def equivalent(self, other):
        if isinstance(other, PatternThatNode):
            return True
        return False

    def to_string(self, verbose=True):
        if verbose is True:
            return "THAT [%s]" % self._child_count(verbose)
        else:
            return "THAT"

    def consume(self, bot, clientid, context, words, word_no, type, depth):

        tabs = TextUtils.get_tabs(word_no)

        if depth > context.max_search_depth:
            logging.error("%sMax search depth [%d]exceeded" % (tabs, context.max_search_depth))
            return None

        if words.word(word_no) == PatternThatNode.THAT:
            logging.debug("%sThat matched %s" % (tabs, words.word(word_no)))
            return super(PatternThatNode, self).consume(bot, clientid, context, words, word_no + 1, type, depth+1)

        logging.debug("%sTHAT NOT matched %s" % (tabs, words.word(word_no)))
        return None

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
        if verbose is True:
            return "PTEMPLATE [%s] " % (self._child_count(verbose))
        else:
            return "PTEMPLATE"

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
        if verbose is True:
            return "WORD [%s] word=[%s]" % (self._child_count(verbose), self.word)
        else:
            return "WORD [%s]" % (self.word)

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

    def to_string(self, verbose=True):
        if verbose is True:
            return "PWORD [%s] word=[%s]" % (self._child_count(verbose), self.word)
        else:
            return "PWORD [%s]" % (self.word)


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
        if self.set_name.upper() == 'NUMBER':
            return word.isnumeric()
        elif bot.brain.sets.contains(self.set_name):
            logging.debug("Looking for [%s] in set [%s]", word, self.set_name)
            set_words = bot.brain.sets.set(self.set_name)
            if word in set_words:
                logging.debug("Found word [%s] in set [%s]"%(word, self.set_name))
                return True
        return False

    def to_string(self, verbose=True):
        if verbose is True:
            return "SET [%s] name=[%s]" % (self._child_count(verbose), self.word)
        else:
            return "SET name=[%s]" % (self.word)


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
                logging.debug("Found word [%s] as bot property"%(word))
                return True
        return False

    def to_string(self, verbose=True):
        if verbose is True:
            return "BOT [%s] property=[%s]" % (self._child_count(verbose), self.word)
        else:
            return "BOT property=[%s]" % (self.word)


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
        if verbose is True:
            return "ZEROORMORE [%s] wildcard=[%s]" % (self._child_count(verbose), self.wildcard)
        else:
            return "ZEROORMORE [%s]" % (self.wildcard)

    def consume(self, bot, clientid, context, words, word_no, type, depth):

        tabs = TextUtils.get_tabs(word_no)

        if depth > context.max_search_depth:
            logging.error("%sMax search depth [%d]exceeded" % (tabs, context.max_search_depth))
            return None

        context_match = Match(type, self, None)
        context.add_match(context_match)
        matches_added = 1

        if self._0ormore_hash is not None:
            logging.debug("%sWildcard is next node, moving on!"%(tabs))
            match = self._0ormore_hash.consume(bot, clientid, context, words, word_no+1, type, depth+1)
            if match is not None:
                return match

        if self._1ormore_underline is not None:
            logging.debug("%sWildcard is next node, moving on!"%(tabs))
            match = self._1ormore_underline.consume(bot, clientid, context, words, word_no+1, type, depth+1)
            if match is not None:
                return match

        if self._0ormore_arrow is not None:
            logging.debug("%sWildcard is next node, moving on!"%(tabs))
            match = self._0ormore_arrow.consume(bot, clientid, context, words, word_no+1, type, depth+1)
            if match is not None:
                return match

        if self._1ormore_star is not None:
            logging.debug("%sWildcard is next node, moving on!"%(tabs))
            match = self._1ormore_star.consume(bot, clientid, context, words, word_no+1, type, depth+1)
            if match is not None:
                return match

        # TODO Add priority words first

        word = words.word(word_no)

        if len(self._children) > 0:
            for child in self._children:
                if child.equals(bot, clientid, word):
                    logging.debug ("%sWildcard child %s matched %s"%(tabs, child._word, word))

                    logging.debug("%s*MATCH -> %s" % (tabs, word))
                    context_match2 = Match(Match.WORD, child, word)
                    context.add_match(context_match2)
                    matches_added += 1

                    match = child.consume(bot, clientid, context, words, word_no+1, type, depth+1)
                    if match is not None:
                        return match

                    if word == PatternTopicNode.TOPIC or word == PatternThatNode.THAT:
                        logging.debug ("Found a topic or that ar the wrong place....")
                        context.pop_matches(matches_added)
                        return None

            logging.debug("%sWildcard %s consumed %s" % (tabs, self._wildcard, word))

            logging.debug("%s*MATCH -> %s" % (tabs, word))
            context_match.add_word(word)

            match = super(PatternZeroOrMoreWildCardNode, self).consume(bot, clientid, context, words, word_no + 1, type, depth+1)
            if match is not None:
                return match

            word_no += 1
            word = words.word(word_no)

            if word == PatternTopicNode.TOPIC or word == PatternThatNode.THAT:
                logging.debug("Found a topic or that ar the wrong place....")
                context.pop_matches(matches_added)
                return None

            logging.debug("%sWildcard %s consumed %s" % (tabs, self._wildcard, word))
            logging.debug("%s*MATCH -> %s" % (tabs, word))
            context_match.add_word(word)

            match = super(PatternZeroOrMoreWildCardNode, self).consume(bot, clientid, context, words, word_no + 1, type, depth+1)
            if match is not None:
                return match

            word_no += 1
            if word_no >= words.num_words():
                context.pop_matches(matches_added)
                return None
            word = words.word(word_no)

        logging.debug("%sNo children, consume words until next break point" % (tabs))
        while word_no < words.num_words() - 1:
            match = super(PatternZeroOrMoreWildCardNode, self).consume(bot, clientid, context, words, word_no, type, depth+1)
            if match is not None:
                return match

            if word == PatternTopicNode.TOPIC or word == PatternThatNode.THAT:
                logging.debug("Found a topic or that ar the wrong place....")
                context.pop_matches(matches_added)
                return None

            logging.debug("%s*MATCH -> %s" % (tabs, word))
            context_match.add_word(word)

            word_no += 1
            word = words.word(word_no)
            logging.debug("%sWildcard %s consumed %s" % (tabs, self._wildcard, word))

        logging.debug("%sWildcard %s consumed %s" % (tabs, self._wildcard, word))

        match = super(PatternZeroOrMoreWildCardNode, self).consume(bot, clientid, context, words, word_no, type, depth+1)

        if match is not None:
            return match
        else:
            context.pop_matches(matches_added)
            return None

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
        if verbose is True:
            return "ONEORMORE [%s] wildcard=[%s]" % (self._child_count(verbose), self.wildcard)
        else:
            return "ONEORMORE [%s]" % (self.wildcard)

    def consume(self, bot, clientid, context, words, word_no, type, depth):

        tabs = TextUtils.get_tabs(word_no)

        if depth > context.max_search_depth:
            logging.error("%sMax search depth [%d]exceeded" % (tabs, context.max_search_depth))
            return None

        if word_no >= words.num_words():
            return None

        word = words.word(word_no)
        logging.debug("%sWildcard %s consumed %s" % (tabs, self._wildcard, word))

        logging.debug("%s*MATCH -> %s" % (tabs, word))
        context_match = Match(type, self, word)
        context.add_match(context_match)
        matches_add = 1

        if self._0ormore_hash is not None:
            logging.debug("%sWildcard is next node, moving on!"%(tabs))
            match = self._0ormore_hash.consume(bot, clientid, context, words, word_no+1, type, depth+1)
            if match is not None:
                return match

        if self._1ormore_underline is not None:
            logging.debug("%sWildcard is next node, moving on!"%(tabs))
            match = self._1ormore_underline.consume(bot, clientid, context, words, word_no+1, type, depth+1)
            if match is not None:
                return match

        if self._0ormore_arrow is not None:
            logging.debug("%sWildcard is next node, moving on!"%(tabs))
            match = self._0ormore_arrow.consume(bot, clientid, context, words, word_no+1, type, depth+1)
            if match is not None:
                return match

        if self._1ormore_star is not None:
            logging.debug("%sWildcard is next node, moving on!"%(tabs))
            match = self._1ormore_star.consume(bot, clientid, context, words, word_no+1, type, depth+1)
            if match is not None:
                return match

        # TODO Add priority words first

        word_no += 1
        if word_no >= words.num_words():
            logging.debug("%sNo more words" % (tabs))
            return super(PatternOneOrMoreWildCardNode, self).consume(bot, clientid, context, words, word_no, type, depth+1)
        word = words.word(word_no)

        if len(self._children) > 0:
            for child in self._children:
                if child.equals(bot, clientid, word):
                    logging.debug ("%sWildcard child %s matched %s"%(tabs, child._word, word))

                    logging.debug("%sMATCH -> %s" % (tabs, word))
                    context_match2 = Match(Match.WORD, child, word)
                    context.add_match(context_match2)
                    matches_add += 1
                    match = child.consume(bot, clientid, context, words, word_no+1, type, depth+1)
                    if match is not None:
                        return match

            if word == PatternTopicNode.TOPIC or word == PatternThatNode.THAT:
                logging.debug ("Found a topic or that ar the wrong place....")
                context.pop_matches(matches_add)
                return None

            logging.debug ("%sWildcard %s consumed %s"%(tabs, self._wildcard, word))

            logging.debug("%s*MATCH -> %s" % (tabs, word))
            context_match.add_word(word)

            word_no += 1
            if word_no >= words.num_words():
                context.pop_matches(matches_add)
                return None
            word = words.word(word_no)

        logging.debug("%sNo children, consume words until next break point"%(tabs))
        while word_no < words.num_words()-1:
            match = super(PatternOneOrMoreWildCardNode, self).consume(bot, clientid, context, words, word_no, type, depth+1)
            if match is not None:
                return match

            if word == PatternTopicNode.TOPIC or word == PatternThatNode.THAT:
                logging.debug ("Found a topic or that ar the wrong place....")
                context.pop_matches(matches_add)
                return None

            logging.debug("%sWildcard %s consumed %s" % (tabs, self._wildcard, word))

            logging.debug("%s*MATCH -> %s" % (tabs, word))
            context_match.add_word(word)

            word_no += 1
            word = words.word(word_no)

        logging.debug("%sWildcard %s consumed %s" % (tabs, self._wildcard, word))
        logging.debug("%s*MATCH -> %s" % (tabs, word))
        context_match.add_word(word)

        if word_no == words.num_words()-1:
            match = super(PatternOneOrMoreWildCardNode, self).consume(bot, clientid, context, words, word_no+1, type, depth+1)
        else:
            match = super(PatternOneOrMoreWildCardNode, self).consume(bot, clientid, context, words, word_no, type, depth+1)

        if match is not None:
            return match
        else:
            context.pop_matches(matches_add)
            return None


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

from programy.utils.text.text import TextUtils
from programy.parser.pattern.matcher import Match, EqualsMatch

#######################################################################################################################
#

class MultiValueDict(dict):

    def __setitem__(self, key, value):
        """add the given value to the list of values for this key"""
        self.setdefault(key, []).append(value)

    def remove(self, key, value):
        if key in self:
            for v in self[key]:
                if v == value:
                    self[key].remove(value)
            if len(self[key]) == 0:
                del self[key]


class PatternNode(object):

    THAT = "__THAT__"
    TOPIC = "__TOPIC__"

    def __init__(self, userid='*'):

        self._userid = userid

        # Child Nodes
        self._priority_words = []
        self._0ormore_hash = None
        self._1ormore_underline = None
        self._children = []
        self._children_words = MultiValueDict()
        self._iset_names = MultiValueDict()
        self._set_names = MultiValueDict()
        self._bot_properties = MultiValueDict()
        self._0ormore_arrow = None
        self._1ormore_star = None

        # Topic, That and Template Nodes
        self._topic = None
        self._that = None
        self._template = None

    @property
    def userid(self):
        return self._userid

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
        return True if self._priority_words else False

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
        return bool(self._0ormore_arrow is not None or self._0ormore_hash is not None)

    def has_0ormore_arrow(self):
        return bool(self._0ormore_arrow is not None)

    def has_0ormore_hash(self):
        return bool(self._0ormore_hash is not None)

    def has_one_or_more(self):
        return bool(self._1ormore_star is not None or self._1ormore_underline is not None)

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
        if self._children:
            return True
        return False

    def has_nodes(self):
        if self._children:
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
    def is_regex(self):
        return False

    ########################################################################
    #
    def equivalent(self, other):
        return False

    def equals(self, client_context, words, word_no):
        return EqualsMatch(False, word_no)

    def equals_ignore_case(self, word1, word2):
        if word1 is not None and word2 is not None:
            return bool(word1.upper() == word2.upper())
        return False

    ########################################################################
    #
    def can_add(self, new_node):
        pass

    def _priority_node_exist(self, new_node):
        for priority in self._priority_words:
            if priority.equivalent(new_node) is True:
                # Equivalent node already exists, use this one instead
                return priority
        return None

    def _zero_or_more_node_exist(self, new_node):
        if self._0ormore_arrow is not None:
            if self._0ormore_arrow.equivalent(new_node) is True:
                return self._0ormore_arrow
        if self._0ormore_hash is not None:
            if self._0ormore_hash.equivalent(new_node) is True:
                return self._0ormore_hash
        return None

    def _one_or_more_node_exist(self, new_node):
        if self._1ormore_underline is not None:
            if self._1ormore_underline.equivalent(new_node) is True:
                return self._1ormore_underline
        if self._1ormore_star is not None:
            if self._1ormore_star.equivalent(new_node) is True:
                return self._1ormore_star
        return None

    def _topic_node_exist(self, new_node):
        if self._topic is not None:
            return self._topic
        return None

    def _that_node_exist(self, new_node):
        if self._that is not None:
            return self._that
        return None

    def _template_node_exist(self, new_node):
        if self._template is not None:
            return self._template
        return None

    def _iset_node_exist(self, new_node):
        for existing_node in self.children:
            if existing_node.is_iset():
                if existing_node.equivalent(new_node):
                    return existing_node
        return None

    def _set_node_exist(self, new_node):
        if new_node.set_name in self._set_names:
            existing_nodes = self._set_names[new_node.set_name]
            for existing_node in existing_nodes:
                if existing_node.equivalent(new_node):
                    # Equivalent node already exists, use this one instead
                    return existing_node
        return None

    def _bot_node_exist(self, new_node):
        if new_node.property in self._bot_properties:
            existing_nodes = self._bot_properties[new_node.property]
            for existing_node in existing_nodes:
                if existing_node.equivalent(new_node):
                    # Equivalent node already exists, use this one instead
                    return existing_node
        return None

    def _regex_node_exist(self, new_node):
        for existing_node in self.children:
            if existing_node.is_regex():
                if existing_node.equivalent(new_node):
                    return existing_node
        return None

    def _word_node_exist(self, new_node):
        if new_node.word in self._children_words:
            existing_nodes = self._children_words[new_node.word]
            for existing_node in existing_nodes:
                if existing_node.equivalent(new_node):
                    # Equivalent node already exists, use this one instead
                    return existing_node
        return None

    def _node_exists(self, new_node):

        if new_node.is_priority() is True:
            return self._priority_node_exist(new_node)

        if new_node.is_zero_or_more() is True:
            return self._zero_or_more_node_exist(new_node)

        if new_node.is_one_or_more() is True:
            return self._one_or_more_node_exist(new_node)

        if new_node.is_topic() is True:
            return self._topic_node_exist(new_node)

        if new_node.is_that():
            return self._that_node_exist(new_node)

        if new_node.is_template() is True:
            return self._template_node_exist(new_node)

        if new_node.is_iset() is True:
            return self._iset_node_exist(new_node)

        if new_node.is_set() is True:
            return self._set_node_exist(new_node)

        if new_node.is_bot() is True:
            return self._bot_node_exist(new_node)

        if new_node.is_regex() is True:
            return self._regex_node_exist(new_node)

        if new_node.is_word():
            return self._word_node_exist(new_node)

        return None

    def _add_node(self, new_node):

        # Otherwise use the new node, and return that to maintain consistence
        # And allow child node to be chained, but supports duplicates
        if new_node.is_priority()  is True:
            self._priority_words.append(new_node)

        elif new_node.is_zero_or_more() is True:
            if new_node.wildcard == '^':
                self._0ormore_arrow = new_node
            elif new_node.wildcard == '#':
                self._0ormore_hash = new_node

        elif new_node.is_one_or_more() is True:
            if new_node.wildcard == '_':
                self._1ormore_underline = new_node
            elif new_node.wildcard == '*':
                self._1ormore_star = new_node

        elif new_node.is_template() is True:
            self._template = new_node

        else:
            # Append sets and bots to the end of the array as they take a slightly
            # lower priority to actual words.
            # This allows the following to work
            #  my favorite color is green
            #  my favorite color is <set>color</set>
            # In the above, if the set color contains green then
            # it still gets picked up in the first grammar and not he second
            if new_node.is_set() is True:
                self.children.append(new_node)
                self._set_names[new_node.set_name] = new_node

            elif new_node.is_iset() is True:
                self.children.append(new_node)
                self._iset_names[new_node.iset_name] = new_node

            elif new_node.is_bot() is True:
                self.children.append(new_node)
                self._bot_properties[new_node.property] = new_node

            elif new_node.is_regex() is True:
                self.children.append(new_node)

            else:
                self.children.insert(0, new_node)
                if new_node.is_word() is True:
                    self._children_words[new_node.word] = new_node

        return new_node

    def _remove_node(self, current_node):
        YLogger.debug(None, "Removing %s" % current_node.to_string())

        if current_node.is_priority()  is True:
            self._priority_words.remove(current_node)

        elif current_node.is_zero_or_more() is True:
            if current_node.wildcard == '^':
                self._0ormore_arrow = None
            elif current_node.wildcard == '#':
                self._0ormore_hash = None

        elif current_node.is_one_or_more() is True:
            if current_node.wildcard == '_':
                self._1ormore_underline = None
            elif current_node.wildcard == '*':
                self._1ormore_star = None

        elif current_node.is_template() is True:
            self._template = None

        else:
            # Append sets and bots to the end of the array as they take a slightly
            # lower priority to actual words.
            # This allows the following to work
            #  my favorite color is green
            #  my favorite color is <set>color</set>
            # In the above, if the set color contains green then
            # it still gets picked up in the first grammar and not he second
            if current_node.is_set() is True:
                self.children.remove(current_node)
                self._set_names.remove(current_node.set_name, current_node)

            elif current_node.is_iset() is True:
                self.children.remove(current_node)
                self._iset_names.remove(current_node.iset_name, current_node)

            elif current_node.is_bot() is True:
                self.children.remove(current_node)
                self._bot_properties.remove(current_node.property, current_node)

            elif current_node.is_regex() is True:
                self.children.remove(current_node)

            else:
                self.children.remove(current_node)
                if current_node.is_word() is True:
                    self._children_words.remove(current_node.word, current_node)

    def add_child(self, new_node, replace_existing=False):

        # Check the rules allow this now to be a child of the current node
        self.can_add(new_node)

        # Next check for duplicates, returning original if one exists
        exists = self._node_exists(new_node)
        if exists is not None and replace_existing is False:
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
        return ""

    def to_string(self, verbose=True):
        if verbose is True:
            return "NODE [%s] [%s]"%(self.userid, self._child_count(verbose))
        return "NODE"

    def get_tabs(self, client_context, depth):
        if client_context.bot.configuration.tab_parse_output is True:
            return TextUtils.get_tabs(depth)
        return ""

    def dump(self, tabs, output_func=YLogger.debug, eol="", verbose=True):

        string = "{0}{1}{2}".format(tabs, self.to_string(verbose), eol)
        if output_func == print:
            output_func(string)
        else:
            output_func(self, string)

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

    def to_xml(self, client_context, include_user=False):
        string = ""

        for priority in self._priority_words:
            string += priority.to_xml(client_context, include_user)

        if self._0ormore_arrow is not None:
            string += self._0ormore_arrow.to_xml(client_context, include_user)

        if self._0ormore_hash is not None:
            string += self._0ormore_hash.to_xml(client_context, include_user)

        if self._1ormore_underline is not None:
            string += self._1ormore_underline.to_xml(client_context, include_user)

        if self._1ormore_star is not None:
            string += self._1ormore_star.to_xml(client_context, include_user)

        if self._topic is not None:
            string += self._topic.to_xml(client_context, include_user)

        if self._that is not None:
            string += self._that.to_xml(client_context, include_user)

        if self._template is not None:
            string += self._template.to_xml(client_context)

        for child in self.children:
            string += child.to_xml(client_context, include_user)

        return string

    def match_children(self, client_context, children, child_type, words, word_no, context, match_type, depth):

        tabs = self.get_tabs(client_context, depth)

        for child in children:

            result = child.equals(client_context, words, word_no)
            if result.matched is True:
                word_no = result.word_no
                YLogger.debug(client_context, "%s%s matched %s", tabs, child_type, result.matched_phrase)

                match_node = Match(match_type, child, result.matched_phrase)

                context.add_match(match_node)

                match = child.consume(client_context, context, words, word_no + 1, match_type, depth+1)
                if match is not None:
                    YLogger.debug(client_context, "%sMatched %s child, success!", tabs, child_type)
                    return match, word_no
                else:
                    context.pop_match()

        return None, word_no

    def consume(self, client_context, context, words, word_no, match_type, depth):

        tabs = self.get_tabs(client_context, depth)

        if context.search_time_exceeded() is True:
            YLogger.error(client_context, "%sMax search time [%d]secs exceeded", tabs, context.max_search_timeout)
            return None

        if context.search_depth_exceeded(depth) is True:
            YLogger.error(client_context, "%sMax search depth [%d] exceeded", tabs, context.max_search_depth)
            return None

        if word_no >= words.num_words():
            if self._template is not None:
                YLogger.debug(client_context, "%sFound a template, success!", tabs)
                return self._template
            else:
                YLogger.debug(client_context, "%sNo more words and no template, no match found!", tabs)
                return None

        if self._topic is not None:
            match = self._topic.consume(client_context, context, words, word_no, Match.TOPIC, depth+1)
            if match is not None:
                YLogger.debug(client_context, "%sMatched topic, success!", tabs)
                return match
            if words.word(word_no) == PatternNode.TOPIC:
                YLogger.debug(client_context, "%s Looking for a %s, none give, no match found!", tabs, PatternNode.TOPIC)
                return None

        if self._that is not None:
            match = self._that.consume(client_context, context, words, word_no, Match.THAT, depth+1)
            if match is not None:
                YLogger.debug(client_context, "%sMatched that, success!", tabs)
                return match
            if words.word(word_no) == PatternNode.THAT:
                YLogger.debug(client_context, "%s Looking for a %s, none give, no match found!", tabs, PatternNode.THAT)
                return None

        match, word_no = self.match_children(client_context, self._priority_words, "Priority", words, word_no, context, match_type, depth)
        if match is not None:
            return match

        if self._0ormore_hash is not None:
            match = self._0ormore_hash.consume(client_context, context, words, word_no, match_type, depth+1)
            if match is not None:
                YLogger.debug(client_context, "%sMatched 0 or more hash, success!", tabs)
                return match

        if self._1ormore_underline is not None:
            match = self._1ormore_underline.consume(client_context, context, words, word_no, match_type, depth+1)
            if match is not None:
                YLogger.debug(client_context, "%sMatched 1 or more underline, success!", tabs)
                return match

        match, word_no = self.match_children(client_context, self._children, "Word", words, word_no, context, match_type, depth)
        if match is not None:
            return match

        if self._0ormore_arrow is not None:
            match = self._0ormore_arrow.consume(client_context, context, words, word_no, match_type, depth+1)
            if match is not None:
                YLogger.debug(client_context, "%sMatched 0 or more arrow, success!", tabs)
                return match

        if self._1ormore_star is not None:
            match = self._1ormore_star.consume(client_context, context, words, word_no, match_type, depth+1)
            if match is not None:
                YLogger.debug(client_context, "%sMatched 1 or more star, success!", tabs)
                return match

        YLogger.debug(client_context, "%sNo match for %s, trying another path", tabs, words.word(word_no))
        return None

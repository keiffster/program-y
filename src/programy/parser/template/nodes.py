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
import subprocess
import xml.etree.ElementTree as ET
import datetime
from dateutil.relativedelta import relativedelta

from random import randint

from programy.parser.exceptions import ParserException
from programy.utils.classes.loader import ClassLoader
from programy.utils.services.service import ServiceFactory
from programy.utils.text.text import TextUtils
from programy.parser.template.maps.plural import PluralMap
from programy.parser.template.maps.singular import SingularMap
from programy.parser.template.maps.predecessor import PredecessorMap
from programy.parser.template.maps.successor import SuccessorMap

# TODO wrap every resolve method in try/catch and return "" if error

######################################################################################################################
#
class TemplateNode(object):

    def __init__(self):
        self._children = []

    @property
    def children(self):
        return self._children

    def append(self, child):
        self._children.append(child)

    def dump(self, tabs, output_func=logging.debug, verbose=True):
        self.output(tabs, output_func)

    def output(self, tabs="", output=logging.debug):
        self.output_child(self, tabs, output)

    def output_child(self, node, tabs, output=logging.debug):
        for child in node.children:
            output("%s{%s}" % (tabs, child.to_string()))
            self.output_child(child, tabs + "\t")

    def resolve_children_to_string(self, bot, clientid):
        return (" ".join([child.resolve(bot, clientid) for child in self._children])).strip()

    def resolve(self, bot, clientid):
        resolved = self.resolve_children_to_string(bot, clientid)
        logging.debug("[%s] resolved to [%s]", self.to_string(), resolved)
        return resolved

    def to_string(self):
        return "[NODE]"

    def xml_tree(self, bot, clientid):
        param = ["<template>"]
        self.to_xml_children(param, bot, clientid)
        param[0] += "</template>"
        return ET.fromstring(param[0])

    def to_xml(self, bot, clientid):
        xml = ""
        for child in self.children:
            xml += child.to_xml(bot, clientid)
        return xml

    def to_xml_children(self, param, bot, clientid):
        first = True
        for child in self.children:
            if first is False:
                param[0] += " "
            param[0] += child.to_xml(bot, clientid)
            first = False


######################################################################################################################
#
class TemplateWordNode(TemplateNode):

    def __init__(self, word):
        TemplateNode.__init__(self)
        self._word = word

    @property
    def word(self):
        return self._word

    @word.setter
    def word(self, word):
        self._word = word

    def resolve(self, bot, clientid):
        logging.debug("[%s] resolved to [%s]", self.to_string(), self.word)
        return self.word

    def to_string(self):
        return "[WORD]" + self.word

    def to_xml(self, bot, clientid):
        return self.word

######################################################################################################################
#
class TemplateRandomNode(TemplateNode):

    def __init__(self):
        TemplateNode.__init__(self)

    def resolve(self, bot, clientid):
        selection = randint(0, len(self._children))
        resolved = self._children[selection - 1].resolve(bot, clientid)
        logging.debug("[%s] resolved to [%s]", self.to_string(), resolved)
        return resolved

    def to_string(self):
        return "[RANDOM] %d" % (len(self._children))

    def to_xml(self, bot, clientid):
        xml = "<random>"
        for child in self.children:
            xml += "<li>"
            xml += child.to_xml(bot, clientid)
            xml += "</li>"
        xml += "</random>"
        return xml

######################################################################################################################
#
class TemplateSRAINode(TemplateNode):

    def __init__(self):
        TemplateNode.__init__(self)

    def resolve(self, bot, clientid):
        srai_text = self.resolve_children_to_string(bot, clientid)
        logging.debug("[%s] SRAI Text [%s]"%(self.to_string(), srai_text))

        resolved = bot.ask_question(clientid, srai_text, srai=True)
        logging.debug("[%s] resolved to [%s]", self.to_string(), resolved)
        return resolved

    def to_string(self):
        return "[SRAI]"

    def to_xml(self, bot, clientid):
        xml = "<srai>"
        for child in self.children:
            xml += child.to_xml(bot, clientid)
        xml += "</srai>"
        return xml

######################################################################################################################
#
class TemplateSrNode(TemplateNode):

    def __init__(self):
        TemplateNode.__init__(self)

    def resolve(self, bot, clientid):
        sentence = bot.get_conversation(clientid).current_question().current_sentence()

        star = sentence.matched_context.star(1)

        if star is not None:
            resolved = bot.ask_question(clientid, star, srai=True)
        else:
            logging.error("Sr node has no stars available")
            resolved = ""

        logging.debug("[%s] resolved to [%s]", self.to_string(), resolved)
        return resolved

    def to_string(self):
        return "SR"

    def to_xml(self, bot, clientid):
        xml = "<sr />"
        return xml

######################################################################################################################
#
class TemplateAttribNode(TemplateNode):

    def __init__(self):
        TemplateNode.__init__(self)

    def set_attrib(self, attrib_name, attrib_value):
        pass


######################################################################################################################
#
class TemplateIndexedNode(TemplateAttribNode):

    def __init__(self, position=1, index=1):
        TemplateAttribNode.__init__(self)
        self._position = position
        self._index = index

    @property
    def position(self):
        return self._position

    @position.setter
    def position(self, position):
        self._position = position

    @property
    def index(self):
        return self._index

    @index.setter
    def index(self, index):
        self._index = index

    def set_attrib(self, attrib_name, attrib_value):

        if attrib_name != 'index':
            raise ParserException("Invalid attribute name [%s] for this node" % (attrib_name))

        if isinstance(attrib_value, int):
            int_val = attrib_value
            self._index = int_val
        else:
            splits = attrib_value.split(",")
            if len(splits) == 1:
                try:
                    self._index = int(splits[0])
                except Exception as excep:
                    logging.exception(excep)
                    raise ParserException("None numeric format [%s] for this node [%s], either 'x' or 'x,y'", attrib_value, attrib_name)
            elif len(splits) == 2:
                try:
                    self._position = int(splits[0])
                    self._index = int(splits[1])
                except Exception as excep:
                    logging.exception(excep)
                    raise ParserException("None numeric format [%s] for this node [%s], either 'x' or 'x,y'", attrib_value, attrib_name)

        if self._index == 0:
            raise ParserException("Index values are 1 based, cannot be 0")
        if self._position == 0:
            raise ParserException("Position values are 1 based, cannot be 0")


######################################################################################################################
#
class TemplateStarNode(TemplateIndexedNode):

    def __init__(self, position=1, index=1):
        TemplateIndexedNode.__init__(self, position, index)

    def resolve(self, bot, clientid):
        conversation = bot.get_conversation(clientid)
        current_question = conversation.current_question()
        current_sentence = current_question.current_sentence()
        matched_context = current_sentence.matched_context

        resolved = matched_context.star(self.index)

        if resolved is None:
            logging.error("Star index not in range [%d]"%(self.index))
            resolved = ""

        logging.debug("Star Node [%s] resolved to [%s]", self.to_string(), resolved)
        return resolved

    def to_string(self):
        return "STAR Index=%s" % self.index

    def to_xml(self, bot, clientid):
        xml = "<star"
        if self._position > 1:
            xml += ' position="%d"' % self._position
        if self._index > 1:
            xml += ' index="%d"' % self._index
        xml += ">"
        xml += "</star>"
        return xml

######################################################################################################################
#
class TemplateSetNode(TemplateNode):

    def __init__(self):
        TemplateNode.__init__(self)
        self._name = None
        self._local = True

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, name):
        self._name = name
        
    @property
    def local(self):
        return self._local

    @local.setter
    def local(self, local):
        self._local = local
        
    def resolve_children(self, bot, clientid):
        if len(self._children) > 0:
            return self.resolve_children_to_string(bot, clientid)
        else:
            return ""

    def resolve(self, bot, clientid):
        name = self.name.resolve(bot, clientid)
        value = self.resolve_children(bot, clientid)

        """
        Todo, if local then set per the conversation
        If globals
            If exists in predicates then don't replace
            If not in predicates then set as global to the conversation
        """

        if self.local is True:
            logging.debug("[%s] resolved to local: [%s] => [%s]", self.to_string(), name, value)
            bot.get_conversation(clientid).current_question().set_predicate(name, value)
        else:
            if bot.override_predicates is False and bot.brain.properties.has_property(name):
                logging.error("Global property already exists for name [%s], ignoring set!", name)
                value = bot.brain.properties.property(name)
            else:
                if bot.brain.properties.has_property(name):
                    logging.warning("Global property already exists for name [%s], over writing!", name)
                logging.debug("[%s] resolved to global: [%s] => [%s]", self.to_string(), name, value)
                bot.get_conversation(clientid).set_predicate(name, value)

        return value

    def to_string(self):
        return "[SET [%s] - %s]" % ("Local" if self.local else "Global", self.name.to_string())

    def to_xml(self, bot, clientid):
        xml = "<set"
        if self.local:
            xml += ' var="%s"' % self.name.resolve(None, None)
        else:
            xml += ' name="%s"' % self.name.resolve(None, None)
        xml += ">"
        for child in self.children:
            xml += child.to_xml(bot, clientid)
        xml += "</set>"
        return xml

######################################################################################################################
#
class TemplateGetNode(TemplateNode):

    def __init__(self):
        TemplateNode.__init__(self)
        self._name = None
        self._local = False

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, name):
        self._name = name

    @property
    def local(self):
        return self._local

    @local.setter
    def local(self, local):
        self._local = local

    def resolve(self, bot, clientid):

        name = self.name.resolve(bot, clientid)

        """
        Todo, if local then set per the conversation
        If globals
            If exists in predicates then don't replace
            If not in predicates then set as global to the conversation
        """

        if self.local is True:
            value = bot.get_conversation(clientid).current_question().predicate(name)
            if value is None:
                logging.warning("No local var for %s, default-get used", name)
                value = bot.brain.properties.property("default-get")
                if value is None:
                    logging.error("No value for default-get defined, empty string returned")
                    value = ""
            logging.debug("[%s] resolved to local: [%s] <= [%s]", self.to_string(), name, value)
        else:
            value = bot.get_conversation(clientid).predicate(name)
            if value is None:
                value = bot.brain.predicates.predicate(name)
                if value is None:
                    value = bot.brain.properties.property("default-get")
                    if value is None:
                        logging.error("No value for default-get defined, empty string returned")
                        value = ""
            logging.debug("[%s] resolved to global: [%s] <= [%s]", self.to_string(), name, value)

        return value

    def to_string(self):
        return "[GET [%s] - %s]" % ("Local" if self.local else "Global", self.name.to_string())

    def output(self, tabs="", output=logging.debug):
        self.output_child(self, tabs, output)

    def to_xml(self, bot, clientid):
        xml = "<get"
        if self.local:
            xml += ' var="%s"' % self.name.resolve(bot, clientid)
        else:
            xml += ' name="%s"' % self.name.resolve(bot, clientid)
        xml += " />"
        return xml


######################################################################################################################
#
class TemplateMapNode(TemplateNode):

    def __init__(self):
        TemplateNode.__init__(self)
        self._name = None
        self._internal_maps = [PluralMap(), SingularMap(), PredecessorMap(), SuccessorMap()]

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, name):
        self._name = name

    def resolve_children(self, bot, clientid):
        if len(self._children) > 0:
            return self.resolve_children_to_string(bot, clientid)
        else:
            return ""

    def resolve(self, bot, clientid):
        name = self.name.resolve(bot, clientid)
        var = self.resolve_children(bot, clientid)

        internal = False
        for map in self._internal_maps:
            if map.get_name() == name:
                value = map.map(var)
                internal = True

        if internal is False:
            the_map = bot.brain.maps.map(name)
            if the_map is None:
                logging.error("No map defined for [%s], using default-map" % name)
                value = bot.brain.properties.property("default-map")
                if value is None:
                    logging.error("No value for default-map defined, empty string returned")
                    value = ""
            else:
                if var in the_map:
                    value = the_map[var]
                else:
                    logging.error("No value defined [%s] in map [%s], using default-map" % (var, name))
                    value = bot.brain.properties.property("default-map")
                    if value is None:
                        logging.error("No value for default-map defined, empty string returned")
                        value = ""

        logging.debug("MAP [%s] resolved to [%s] = [%s]", self.to_string(), name, value)
        return value

    def to_string(self):
        return "[MAP (%s)]" % (self.name.to_string())

    def output(self, tabs="", output=logging.debug):
        self.output_child(self, tabs, output=logging.debug)

    def to_xml(self, bot, clientid):
        xml = "<map "
        xml += ' name="%s"' % self.name.resolve(bot, clientid)
        xml += ">"
        for child in self.children:
            xml += child.to_xml(bot, clientid)
        xml += "</map>"
        return xml


######################################################################################################################
#
class TemplateBotNode(TemplateNode):

    def __init__(self):
        TemplateNode.__init__(self)
        self._name = None

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, name):
        self._name = name

    def resolve(self, bot, clientid):
        name = self.name.resolve(bot, clientid)
        value = bot.brain.properties.property(name)
        if value is None:
            value = bot.brain.properties.property("default-property")
            if value is None:
                value = ""

        logging.debug("[%s] resolved to [%s] = [%s]", self.to_string(), name, value)
        return value

    def to_string(self):
        return "[BOT (%s)]" % (self.name.to_string())

    def output(self, tabs="", output=logging.debug):
        self.output_child(self, tabs, output)

    def to_xml(self, bot, clientid):
        xml = "<bot "
        xml += ' name="%s"' % self.name.resolve(bot, clientid)
        xml += " />"
        return xml


######################################################################################################################
#
class TemplateConditionListItemNode(TemplateNode):

    def __init__(self, name=None, value=None, local=False, loop=False):
        TemplateNode.__init__(self)
        self._name = name
        self._value = value
        self._local = local
        self._loop = loop

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, name):
        self._name = name

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, value):
        self._value = value

    @property
    def local(self):
        return self._local

    @local.setter
    def local(self, local):
        self._local = local

    @property
    def loop(self):
        return self._loop

    @loop.setter
    def loop(self, loop):
        self._loop = loop

    def is_default(self):
        return bool(self.value is None)

    def resolve(self, bot, clientid):
        pass

    def to_string(self):
        return "[CONDITIONLIST(%s=%s)]" % (self.name, self.value)

    def to_xml(self, bot, clientid):
        xml = '<li'
        if self.name is not None:
            if self.local is True:
                xml += ' var="%s"' % self.name
            else:
                xml += ' name="%s"' % self.name
        xml += ">"
        if self.value is not None:
            xml += '<value>'
            xml += self.value.to_xml(bot, clientid)
            xml += '</value>'
        for child in self.children:
            xml += child.to_xml(bot, clientid)
        if self.loop is True:
            xml += "<loop />"
        xml += '</li>'
        return xml


class TemplateConditionNode(TemplateNode):

    def __init__(self):
        TemplateNode.__init__(self)

    def _get_predicate_value(self, bot, clientid, name, local):

        if local is False:
            value = bot.conversation(clientid).predicate(name)
        else:
            value = bot.conversation(clientid).current_question().predicate(name)

        if value is None:
            value = bot.brain.properties.property("default-get")
            if value is None:
                logging.error("No value for default-get defined, empty string returned")
                value = ""
        return value


class TemplateType1ConditionNode(TemplateConditionNode):

    def __init__(self, name, value, local=False):
        TemplateConditionNode.__init__(self)
        self._name = name
        self._value = value
        self._local = local

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, name):
        self._name = name

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, value):
        self._value = value

    @property
    def local(self):
        return self._local

    @local.setter
    def local(self, local):
        self._local = local

    def resolve(self, bot, clientid):
        value = self._get_predicate_value(bot, clientid, self.name, self.local)
        if value == self.value.resolve(bot, clientid):
            resolved = " ".join([child.resolve(bot, clientid) for child in self.children])
        else:
            resolved = ""

        logging.debug("[%s] resolved to [%s]", self.to_string(), resolved)
        return resolved

    def to_string(self):
        return "[CONDITION1(%s=%s)]" % (self.name, self.value)

    def to_xml(self, bot, clientid):
        xml = "<condition"
        if self.local is True:
            xml += ' var="%s"' % self.name
        else:
            xml += ' name="%s"' % self.name
        xml += ">"
        xml += '<value>'
        xml += self.value.to_xml(bot, clientid)
        xml += '</value>'
        for child in self.children:
            xml += child.to_xml(bot, clientid)
        xml += "</condition>"
        return xml


class TemplateConditionNodeWithChildren(TemplateConditionNode):

    def __init__(self):
        TemplateConditionNode.__init__(self)

    def get_default(self):
        for child in self.children:
            if child.is_default() is True:
                return child
        return None


class TemplateType2ConditionNode(TemplateConditionNodeWithChildren):

    def __init__(self, name, local=False):
        TemplateConditionNodeWithChildren.__init__(self)
        self.name = name
        self.local = local

    def resolve(self, bot, clientid):

        value = self._get_predicate_value(bot, clientid, self.name, self.local)

        for condition in self.children:
            if condition.is_default() is False:
                condition_value = condition.value.resolve(bot, clientid)
                #print("Value [%s] =?= [%s]" % (value, condition_value.strip()))
                if value == condition_value:
                    resolved = " ".join([child_node.resolve(bot, clientid) for child_node in condition.children])
                    logging.debug("[%s] resolved to [%s]", self.to_string(), resolved)

                    if condition.loop is True:
                        resolved = resolved.strip() + " " + self.resolve(bot, clientid)

                    return resolved

        default = self.get_default()
        if default is not None:
            resolved = " ".join([child_node.resolve(bot, clientid) for child_node in default.children])

            if default.loop is True:
                resolved = resolved.strip() + " " + self.resolve(bot, clientid)
        else:
            resolved = ""

        logging.debug("[%s] resolved to [%s]", self.to_string(), resolved)

        return resolved

    def to_string(self):
        return "[CONDITION2(%s)]" % self.name

    def to_xml(self, bot, clientid):
        xml = "<condition"
        if self.local is True:
            xml += ' var="%s"' % self.name
        else:
            xml += ' name="%s"' % self.name
        xml += ">"
        for child in self.children:
            xml += child.to_xml(bot, clientid)
        xml += "</condition>"
        return xml


class TemplateType3ConditionNode(TemplateConditionNodeWithChildren):

    def __init__(self):
        TemplateConditionNodeWithChildren.__init__(self)

    def resolve(self, bot, clientid):
        for condition in self.children:
            value = self._get_predicate_value(bot, clientid, condition.name, condition.local)
            if condition.value is not None:
                condition_value = condition.value.resolve(bot, clientid)
                if value == condition_value:
                    resolved = " ".join([child_node.resolve(bot, clientid) for child_node in condition.children])
                    logging.debug("[%s] resolved to [%s]", self.to_string(), resolved)

                    if condition.loop is True:
                        resolved = resolved.strip() + " " + self.resolve(bot, clientid).strip()

                    return resolved

        default = self.get_default()
        if default is not None:
            resolved = " ".join([child_node.resolve(bot, clientid) for child_node in default.children])

            if default.loop is True:
                resolved = resolved.strip() + " " + self.resolve(bot, clientid).strip()

        else:
            resolved = ""
        logging.debug("[%s] resolved to [%s]", self.to_string(), resolved)

        return resolved

    def to_string(self):
        return "[CONDITION3()]"

    def to_xml(self, bot, clientid):
        xml = "<condition>"
        for child in self.children:
            xml += child.to_xml(bot, clientid)
        xml += "</condition>"
        return xml



######################################################################################################################
#
class TemplateThinkNode(TemplateNode):

    def __init__(self):
        TemplateNode.__init__(self)

    def resolve(self, bot, clientid):
        resolved = self.resolve_children_to_string(bot, clientid)
        logging.debug("[%s] resolved to [%s]", self.to_string(), resolved)
        return ""

    def to_string(self):
        return "THINK"

    def to_xml(self, bot, clientid):
        xml = "<think>"
        for child in self.children:
            xml += child.to_xml(bot, clientid)
        xml += "</think>"
        return xml


######################################################################################################################
#
class TemplateLowercaseNode(TemplateNode):

    def __init__(self):
        TemplateNode.__init__(self)

    def resolve(self, bot, clientid):
        resolved = self.resolve_children_to_string(bot, clientid)
        resolved = resolved.lower()
        logging.debug("[%s] resolved to [%s]", self.to_string(), resolved)
        return resolved

    def to_string(self):
        return "LOWERCASE"

    def to_xml(self, bot, clientid):
        xml = "<lowercase>"
        for child in self.children:
            xml += child.to_xml(bot, clientid)
        xml += "</lowercase>"
        return xml


######################################################################################################################
#
class TemplateUppercaseNode(TemplateNode):

    def __init__(self):
        TemplateNode.__init__(self)

    def resolve(self, bot, clientid):
        resolved = self.resolve_children_to_string(bot, clientid)
        resolved = resolved.upper()
        logging.debug("[%s] resolved to [%s]", self.to_string(), resolved)
        return resolved

    def to_string(self):
        return "UPPERCASE"

    def to_xml(self, bot, clientid):
        xml = "<uppercase>"
        for child in self.children:
            xml += child.to_xml(bot, clientid)
        xml += "</uppercase>"
        return xml


######################################################################################################################
#
class TemplateFormalNode(TemplateNode):

    def __init__(self):
        TemplateNode.__init__(self)

    def resolve(self, bot, clientid):
        result = self.resolve_children_to_string(bot, clientid)
        return result.title()

    def to_string(self):
        return "FORMAL"

    def to_xml(self, bot, clientid):
        xml = "<formal>"
        for child in self.children:
            xml += child.to_xml(bot, clientid)
        xml += "</formal>"
        return xml


######################################################################################################################
#
class TemplateSentenceNode(TemplateNode):

    def __init__(self):
        TemplateNode.__init__(self)

    def resolve(self, bot, clientid):
        result = self.resolve_children_to_string(bot, clientid)
        first = result[:1]
        rest = result[1:]
        resolved = first.upper() + rest.lower()
        logging.debug("[%s] resolved to [%s]", self.to_string(), resolved)
        return resolved

    def to_string(self):
        return "SENTENCE"

    def to_xml(self, bot, clientid):
        xml = "<sentence>"
        for child in self.children:
            xml += child.to_xml(bot, clientid)
        xml += "</sentence>"
        return xml


######################################################################################################################
#
class TemplateExplodeNode(TemplateNode):

    def __init__(self):
        TemplateNode.__init__(self)

    def resolve(self, bot, clientid):
        result = self.resolve_children_to_string(bot, clientid)
        letters = [ch for ch in result if ch != ' ']
        resolved = " ".join(letters)
        logging.debug("[%s] resolved to [%s]", self.to_string(), resolved)
        return resolved

    def to_string(self):
        return "EXPLODE"

    def to_xml(self, bot, clientid):
        xml = "<explode>"
        for child in self.children:
            xml += child.to_xml(bot, clientid)
        xml += "</explode>"
        return xml


######################################################################################################################
#
class TemplateImplodeNode(TemplateNode):

    def __init__(self):
        TemplateNode.__init__(self)

    def resolve(self, bot, clientid):
        result = self.resolve_children_to_string(bot, clientid)
        resolved = TextUtils.strip_all_whitespace(result)
        logging.debug("[%s] resolved to [%s]", self.to_string(), resolved)
        return resolved

    def to_string(self):
        return "IMPLODE"

    def to_xml(self, bot, clientid):
        xml = "<implode>"
        for child in self.children:
            xml += child.to_xml(bot, clientid)
        xml += "</implode>"
        return xml



######################################################################################################################
#

class TemplateFirstNode(TemplateNode):

    def __init__(self):
        TemplateNode.__init__(self)

    def resolve(self, bot, clientid):
        result = self.resolve_children_to_string(bot, clientid)
        words = result.split(" ")
        if len(words) > 0:
            resolved = words[0]
        else:
            resolved = "NIL"
        logging.debug("[%s] resolved to [%s]", self.to_string(), resolved)
        return resolved

    def to_string(self):
        return "FIRST"

    def to_xml(self, bot, clientid):
        xml = "<first>"
        for child in self.children:
            xml += child.to_xml(bot, clientid)
        xml += "</first>"
        return xml


######################################################################################################################
#

class TemplateRestNode(TemplateNode):

    def __init__(self):
        TemplateNode.__init__(self)

    def resolve(self, bot, clientid):
        result = self.resolve_children_to_string(bot, clientid)
        words = result.split(" ")
        if len(words) > 1:
            resolved = " ".join(words[1:])
        else:
            resolved = "NIL"
        logging.debug("[%s] resolved to [%s]", self.to_string(), resolved)
        return resolved

    def to_string(self):
        return "REST"

    def to_xml(self, bot, clientid):
        xml = "<rest>"
        for child in self.children:
            xml += child.to_xml(bot, clientid)
        xml += "</rest>"
        return xml


######################################################################################################################
#
class TemplateIdNode(TemplateNode):

    def __init__(self):
        TemplateNode.__init__(self)

    def resolve(self, bot, clientid):
        logging.debug("[%s] resolved to [%s]", self.to_string(), clientid)
        return clientid

    def to_string(self):
        return "ID"

    def to_xml(self, bot, clientid):
        xml = "<id />"
        return xml


######################################################################################################################
#
class TemplateVocabularyNode(TemplateNode):

    def __init__(self):
        TemplateNode.__init__(self)

    def resolve(self, bot, clientid):
        set_words = bot.brain.sets.count_words_in_sets()
        pattern_words = bot.brain.aiml_parser.pattern_parser.count_words_in_patterns()
        resolved = "%d" % (set_words + pattern_words)
        logging.debug("[%s] resolved to [%s]", self.to_string(), resolved)
        return resolved

    def to_string(self):
        return "VOCABULARY"

    def to_xml(self, bot, clientid):
        xml = "<vocabulary>"
        for child in self.children:
            xml += child.to_xml(bot, clientid)
        xml += "</vocabulary>"
        return xml


######################################################################################################################
#
class TemplateProgramNode(TemplateNode):

    def __init__(self):
        TemplateNode.__init__(self)

    def resolve(self, bot, clientid):
        fullname = "AIMLBot"
        if bot.brain.properties.has_property("fullname") is True:
            fullname = bot.brain.properties.property("fullname")
        else:
            logging.error("Fullname property missing")

        version = ""
        if bot.brain.properties.has_property("version") is True:
            version = bot.brain.properties.property("version")
        else:
            logging.error("Version property missing")

        resolved = "%s %s" % (fullname, version)
        logging.debug("[%s] resolved to [%s]", self.to_string(), resolved)
        return resolved

    def to_string(self):
        return "PROGRAM"

    def to_xml(self, bot, clientid):
        xml = "<program />"
        return xml


# #####################################################################################################################
#
class TemplateDateNode(TemplateAttribNode):

    def __init__(self, date_format=None):
        TemplateAttribNode.__init__(self)
        if date_format is None:
            self._format = "%c"
        else:
            self._format = date_format

    @property
    def format(self):
        return self._format

    @format.setter
    def format(self, format):
        self._format = format

    def resolve(self, bot, clientid):
        time_now = datetime.datetime.now()
        resolved = time_now.strftime(self._format).upper()
        logging.debug("[%s] resolved to [%s]", self.to_string(), resolved)
        return resolved

    def to_string(self):
        return "DATE format=%s" % (self._format)

    def set_attrib(self, attrib_name, attrib_value):
        if attrib_name != 'format':
            raise ParserException("Invalid attribute name %s for this node" % (attrib_name))
        self._format = attrib_value

    def to_xml(self, bot, clientid):
        xml = '<date format="%s" >' % self._format
        for child in self.children:
            xml += child.to_xml(bot, clientid)
        xml += "</date>"
        return xml


######################################################################################################################
#
class TemplateIntervalNode(TemplateNode):

    def __init__(self, date_format="%c", style="days"):
        TemplateNode.__init__(self)
        self._interval_from = None
        self._interval_to = None
        if isinstance(date_format, str):
            self._format = TemplateWordNode(date_format)
        else:
            self._format = date_format
        if isinstance(style, str):
            self._style = TemplateWordNode(style)
        else:
            self._style = style

    @property
    def format(self):
        return self._format

    @format.setter
    def format(self, format):
        self._format = format

    @property
    def interval_from(self):
        return self._interval_from

    @interval_from.setter
    def interval_from(self, interval_from):
        self._interval_from = interval_from

    @property
    def interval_to(self):
        return self._interval_to

    @interval_to.setter
    def interval_to(self, interval_to):
        self._interval_to = interval_to

    @property
    def style(self):
        return self._style

    @style.setter
    def style(self, style):
        self._style = style

    def resolve(self, bot, clientid):
        try:
            format_str = self._format.resolve(bot, clientid)

            from_str = self.interval_from.resolve(bot, clientid)
            from_time = datetime.datetime.strptime(from_str, format_str)

            to_str = self.interval_to.resolve(bot, clientid)
            to_time = datetime.datetime.strptime(to_str, format_str)

            style = self._style.resolve(bot, clientid)

            diff = to_time - from_time
            difference = relativedelta(to_time, from_time)

            if style == "years":
                resolved = str(difference.years)
            elif style == "months":
                resolved = str(difference.months)
            elif style == "weeks":
                resolved = str(difference.weeks)
            elif style == "days":
                resolved = str(diff.days)
            elif style == "hours":
                resolved = str(difference.hours)
            elif style == "minutes":
                resolved = str(difference.minutes)
            elif style == "seconds":
                resolved = str(difference.seconds)
            elif style == "microseconds":
                resolved = str(difference.microseconds)
            elif style == "ymd":
                resolved = "%d years, %d months, %d days" % \
                           (difference.years, difference.months, difference.days)
            elif style == "hms":
                resolved = "%d hours, %d minutes, %d seconds" % \
                           (difference.hours, difference.minutes, difference.seconds)
            elif style == "ymdhms":
                resolved = "%d years, %d months, %d days, %d hours, %d minutes, %d seconds" % \
                           (difference.years, difference.months, difference.days,
                            difference.hours, difference.minutes, difference.seconds)
            else:
                logging.error("Unknown interval style [%s]", style)
                resolved = ""

            logging.debug("[INTERVAL] resolved to [%s]", resolved)
            return resolved

        except Exception as excep:
            logging.exception(excep)
            return ""

    def to_string(self):
        return "[INTERVAL]"

    def to_xml(self, bot, clientid):
        xml = '<interval'
        xml += ' format="%s"' % self._format.to_xml(bot, clientid)
        xml += ' style="%s"' % self._style.to_xml(bot, clientid)
        xml += '>'
        xml += '<from>'
        xml += self._interval_from.to_xml(bot, clientid)
        xml += '</from>'
        xml += '<to>'
        xml += self._interval_to.to_xml(bot, clientid)
        xml += '</to>'
        xml += '</interval>'
        return xml


######################################################################################################################
#
class TemplateSystemNode(TemplateAttribNode):

    def __init__(self):
        TemplateAttribNode.__init__(self)
        self._timeout = 0

    @property
    def timeout(self):
        return self._timeout

    @timeout.setter
    def timeout(self, timeout):
        self._timeout = timeout

    def resolve(self, bot, clientid):
        if bot.brain.configuration.allow_system_aiml is True:
            command = self.resolve_children_to_string(bot, clientid)
            process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
            result = []
            for line in process.stdout.readlines():
                byte_string = line.decode("utf-8")
                result.append(byte_string.strip())
            process.wait()
            resolved = " ".join(result)
        else:
            logging.warning("System command node disabled in config")
            resolved = ""
        logging.debug("[%s] resolved to [%s]", self.to_string(), resolved)
        return resolved

    def to_string(self):
        return "SYSTEM timeout=%s" % (self._timeout)

    def set_attrib(self, attrib_name, attrib_value):
        if attrib_name != 'timeout':
            raise ParserException("Invalid attribute name %s for this node", attrib_name)
        logging.warning("System node timeout attrib currently ignored")
        self._timeout = attrib_value

    def to_xml(self, bot, clientid):
        xml = "<system"
        if self._timeout != 0:
            xml += ' timeout="%d"' % self._timeout
        xml += ">"
        for child in self.children:
            xml += child.to_xml(bot, clientid)
        xml += "</system>"
        return xml


######################################################################################################################
#
class TemplateSizeNode(TemplateNode):

    def __init__(self):
        TemplateNode.__init__(self)

    def resolve(self, bot, clientid):
        resolved = str(bot.brain.aiml_parser.num_categories)
        logging.debug("[%s] resolved to [%s]", self.to_string(), resolved)
        return resolved

    def to_string(self):
        return "SIZE"

    def to_xml(self, bot, clientid):
        xml = "<size />"
        return xml


######################################################################################################################
#
# <input index=”n”/> is replaced with the value of the nth previous sentence input to the bot.
#
class TemplateInputNode(TemplateIndexedNode):

    def __init__(self, position=1, index=1):
        TemplateIndexedNode.__init__(self, position, index)

    def resolve(self, bot, clientid):
        conversation = bot.get_conversation(clientid)
        sentence = conversation.nth_sentence(self.index)
        resolved = sentence
        logging.debug("[%s] resolved to [%s]", self.to_string(), resolved)
        return resolved

    def to_string(self):
        return "INPUT Index=%s" % (self.index)

    def to_xml(self, bot, clientid):
        xml = "<input"
        if self._position > 1:
            xml += ' position="%d"' % self._position
        if self._index > 1:
            xml += ' index="%d"' % self._index
        xml += ">"
        xml += "</input>"
        return xml


######################################################################################################################
#
# <request index=”n”/> is replaced with the value of the nth previous multi-sentence input to the bot.
#
class TemplateRequestNode(TemplateIndexedNode):

    def __init__(self, position=1, index=1):
        TemplateIndexedNode.__init__(self, position, index)

    def resolve(self, bot, clientid):
        try:
            nth_question = self.index
            conversation = bot.get_conversation(clientid)
            question = conversation.nth_question(nth_question)
            sentences = question.combine_sentences()
            resolved = sentences
        except Exception as excep:
            logging.exception(excep)
            resolved = ""
        logging.debug("[%s] resolved to [%s]", self.to_string(), resolved)
        return resolved

    def to_string(self):
        return "REQUEST Index=%s" % (self.index)

    def to_xml(self, bot, clientid):
        xml = "<request"
        if self._position > 1:
            xml += " position='%d'" % self._position
        if self._index > 1:
            xml += " index='%d'" % self._index
        xml += ">"
        xml += "</request>"
        return xml


######################################################################################################################
#
# <response index=”n”/> is replaced with the value of the nth previous multi-sentence bot response..
#
class TemplateResponseNode(TemplateIndexedNode):

    def __init__(self, position=1, index=1):
        TemplateIndexedNode.__init__(self, position, index)

    def resolve(self, bot, clientid):
        try:
            nth_question = self.index
            conversation = bot.get_conversation(clientid)
            question = conversation.nth_question(nth_question)
            responses = question.combine_answers()
            resolved = responses
        except Exception as excep:
            logging.exception(excep)
            resolved = ""
        logging.debug("[%s] resolved to [%s]", self.to_string(), resolved)
        return resolved

    def to_string(self):
        return "RESPONSE Index=%s" % (self.index)

    def to_xml(self, bot, clientid):
        xml = "<response"
        if self._position > 1:
            xml += ' position="%d"' % self._position
        if self._index > 1:
            xml += ' index="%d"' % self._index
        xml += ">"
        xml += "</response>"
        return xml


######################################################################################################################
#
# <that />
# <that index=”n” />
# <that index="m,n" />
#
class TemplateThatNode(TemplateIndexedNode):

    def __init__(self, position=1, index=1):
        TemplateIndexedNode.__init__(self, position, index)

    def resolve(self, bot, clientid):
        try:
            nth_question = self.index
            conversation = bot.get_conversation(clientid)
            question = conversation.nth_question(nth_question)
            responses = question.combine_answers()
            resolved = responses
        except Exception as excep:
            logging.exception(excep)
            resolved = ""
        logging.debug("[%s] resolved to [%s]", self.to_string(), resolved)
        return resolved

    def to_string(self):
        return "THAT Index=%s" % (self.index)

    def to_xml(self, bot, clientid):
        xml = "<that"
        if self._position > 1:
            xml += ' position="%d"' % self._position
        if self._index > 1:
            xml += ' index="%d"' % self._index
        xml += ">"
        xml += "</that>"
        return xml


######################################################################################################################
#
class TemplateTopicStarNode(TemplateIndexedNode):

    def __init__(self, position=1, index=1):
        TemplateIndexedNode.__init__(self, position, index)

    def resolve(self, bot, clientid):
        sentence = bot.get_conversation(clientid).current_question().current_sentence()

        resolved = sentence.matched_context.topicstar(self.index)

        if resolved is None:
            logging.error("That Star index not in range [%d]" % (self.index))
            resolved = ""

        return resolved

    def to_string(self):
        return "TOPICSTAR Index=%s" % (self.index)

    def to_xml(self, bot, clientid):
        xml = "<topicstar"
        if self._position > 1:
            xml += ' position="%d"' % self._position
        if self._index > 1:
            xml += ' index="%d"' % self._index
        xml += ">"
        xml += "</topicstar>"
        return xml


######################################################################################################################
#
class TemplateThatStarNode(TemplateIndexedNode):

    def __init__(self, position=1, index=1):
        TemplateIndexedNode.__init__(self, position, index)

    def resolve(self, bot, clientid):
        question = bot.get_conversation(clientid).nth_question(1)

        sentence = question.current_sentence()

        resolved = sentence.matched_context.thatstar(self.index)

        if resolved is None:
            logging.error("That Star index not in range [%d]" % (self.index))
            resolved = ""

        return resolved

    def to_string(self):
        return "THATSTAR Index=%s" % (self.index)

    def to_xml(self, bot, clientid):
        xml = "<thatstar"
        if self._position > 1:
            xml += ' position="%d"' % self._position
        if self._index > 1:
            xml += ' index="%d"' % self._index
        xml += ">"
        xml += "</thatstar>"
        return xml


######################################################################################################################
#
class TemplatePersonNode(TemplateNode):

    def __init__(self):
        TemplateNode.__init__(self)

    def resolve(self, bot, clientid):
        string = self.resolve_children_to_string(bot, clientid)
        resolved = bot.brain.persons.personalise_string(string)
        logging.debug("[%s] resolved to [%s]", self.to_string(), resolved)
        return resolved

    def to_string(self):
        return "PERSON"

    def to_xml(self, bot, clientid):
        xml = "<person>"
        for child in self.children:
            xml += child.to_xml(bot, clientid)
        xml += "</person>"
        return xml


######################################################################################################################
#
class TemplatePerson2Node(TemplateNode):

    def __init__(self):
        TemplateNode.__init__(self)

    def resolve(self, bot, clientid):
        string = self.resolve_children_to_string(bot, clientid)
        resolved = bot.brain.person2s.personalise_string(string)
        logging.debug("[%s] resolved to [%s]", self.to_string(), resolved)
        return resolved

    def to_string(self):
        return "PERSON2"

    def to_xml(self, bot, clientid):
        xml = "<person2>"
        for child in self.children:
            xml += child.to_xml(bot, clientid)
        xml += "</person2>"
        return xml


######################################################################################################################
#
class TemplateGenderNode(TemplateNode):

    def __init__(self):
        TemplateNode.__init__(self)

    def resolve(self, bot, clientid):
        string = self.resolve_children_to_string(bot, clientid)
        resolved = bot.brain.genders.genderise_string(string)
        logging.debug("[%s] resolved to [%s]", self.to_string(), resolved)
        return resolved

    def to_string(self):
        return "GENDER"

    def to_xml(self, bot, clientid):
        xml = "<gender>"
        for child in self.children:
            xml += child.to_xml(bot, clientid)
        xml += "</gender>"
        return xml


######################################################################################################################
#
class TemplateNormalizeNode(TemplateNode):

    def __init__(self):
        TemplateNode.__init__(self)

    def resolve(self, bot, clientid):
        string = self.resolve_children_to_string(bot, clientid)
        resolved = bot.brain.normals.normalise_string(string)
        logging.debug("[%s] resolved to [%s]", self.to_string(), resolved)
        return resolved

    def to_string(self):
        return "NORMALIZE"

    def to_xml(self, bot, clientid):
        xml = "<normalize>"
        for child in self.children:
            xml += child.to_xml(bot, clientid)
        xml += "</normalize>"
        return xml


######################################################################################################################
#
class TemplateDenormalizeNode(TemplateNode):

    def __init__(self):
        TemplateNode.__init__(self)

    def resolve(self, bot, clientid):
        string = self.resolve_children_to_string(bot, clientid)
        resolved = bot.brain.denormals.denormalise_string(string)
        logging.debug("[%s] resolved to [%s]", self.to_string(), resolved)
        return resolved

    def to_string(self):
        return "DENORMALIZE"

    def to_xml(self, bot, clientid):
        xml = "<denormalize>"
        for child in self.children:
            xml += child.to_xml(bot, clientid)
        xml += "</denormalize>"
        return xml


######################################################################################################################
#
class TemplateEvalNode(TemplateNode):

    def __init__(self):
        TemplateNode.__init__(self)

    def resolve(self, bot, clientid):
        resolved = self.resolve_children_to_string(bot, clientid)
        logging.debug("[%s] resolved to [%s]", self.to_string(), resolved)
        return resolved

    def to_string(self):
        return "EVAL"

    def to_xml(self, bot, clientid):
        xml = "<eval>"
        for child in self.children:
            xml += child.to_xml(bot, clientid)
        xml += "</eval>"
        return xml


######################################################################################################################
#
class TemplateLearnNode(TemplateNode):

    def __init__(self):
        TemplateNode.__init__(self)
        self._pattern = None
        self._topic = None
        self._that = None
        self._template = None

    @property
    def pattern(self):
        return self._pattern

    @pattern.setter
    def pattern(self, pattern):
        self._pattern = pattern

    @property
    def topic(self):
        return self._topic

    @topic.setter
    def topic(self, topic):
        self._topic = topic

    @property
    def that(self):
        return self._that

    @that.setter
    def that(self, that):
        self._that = that

    @property
    def template(self):
        return self._template

    @template.setter
    def template(self, template):
        self._template = template

    def evaluate_eval_nodes(self, bot, clientid, template):

        new_template = TemplateNode()

        count = 0
        for child in template.children:
            if isinstance(child, TemplateEvalNode):
                new_word_node = TemplateWordNode(child.resolve(bot, clientid))
                new_template.children.append(new_word_node)
            else:
                new_template.children.append(child)
            count += 1

        return new_template

    def resolve_element_evals(self, bot, clientid, element):

        new_element = ET.Element(element.tag)

        new_element.text = TextUtils.strip_whitespace(element.text)

        for child in element:
            if child.tag == 'eval':
                eval_str = ET.tostring(child, 'utf-8').decode('ascii')
                eval_str = TextUtils.strip_whitespace(eval_str)
                str_val = "<template>%s</template>" % eval_str
                template = ET.fromstring(str_val)

                ast = bot.brain.aiml_parser.template_parser.parse_template_expression(template)
                resolved = ast.resolve(bot, clientid)

                new_element.text += " " + resolved
            else:
                new_element.append(child)

        new_element.text = new_element.text.upper ()

        if element.tail is not None:
            new_element.tail = TextUtils.strip_whitespace(element.tail)

        return new_element

    def resolve(self, bot, clientid):
        new_pattern = self.resolve_element_evals(bot, clientid, self._pattern)
        new_topic = self.resolve_element_evals(bot, clientid, self._topic)
        new_that = self.resolve_element_evals(bot, clientid, self._that)

        # TODO This overwrites the self._template with an evaluated one
        # What it should do is return a new template that is then added
        # to the graph
        new_template = self.evaluate_eval_nodes(bot, clientid, self._template)

        bot.brain.aiml_parser.pattern_parser.add_pattern_to_graph(new_pattern, new_topic, new_that, new_template)

        logging.debug("[%s] resolved to new pattern [[%s] [%s] [%s]", self.to_string(),
                      ET.tostring(new_pattern, 'utf-8').decode('utf-8'),
                      ET.tostring(new_topic, 'utf-8').decode('utf-8'),
                      ET.tostring(new_that, 'utf-8').decode('utf-8'))

        logging.debug("%s", self.to_xml(bot, clientid))

        return ""

    def to_string(self):
        return "LEARN"

    def to_xml(self, bot, clientid):
        xml = "<learn>"

        xml += ET.tostring(self._pattern, 'utf-8').decode('utf-8')
        xml += ET.tostring(self._topic, 'utf-8').decode('utf-8')
        xml += ET.tostring(self._that, 'utf-8').decode('utf-8')

        xml += "<template>"
        xml += self._template.to_xml(bot, clientid)
        xml += "</template>"

        xml += "</learn>"

        return xml


######################################################################################################################
#
class TemplateLearnfNode(TemplateLearnNode):

    def __init__(self):
        TemplateLearnNode.__init__(self)

    def resolve(self, bot, clientid):
        new_pattern = self.resolve_element_evals(bot, clientid, self._pattern)
        new_topic = self.resolve_element_evals(bot, clientid, self._topic)
        new_that = self.resolve_element_evals(bot, clientid, self._that)

        template = self.evaluate_eval_nodes(bot, clientid, self._template)

        bot.brain.aiml_parser.pattern_parser.add_pattern_to_graph(new_pattern, new_topic, new_that, template)

        logging.debug("[%s] resolved to new pattern [[%s] [%s] [%s]", self.to_string(),
                      ET.tostring(new_pattern, 'utf-8').decode('utf-8'),
                      ET.tostring(new_topic, 'utf-8').decode('utf-8'),
                      ET.tostring(new_that, 'utf-8').decode('utf-8'))

        bot.brain.write_learnf_to_file(bot, clientid, new_pattern, new_topic, new_that, self._template)
        return ""

    def to_string(self):
        return "LEARNF"

    def to_xml(self, bot, clientid):
        xml = "<learnf>"

        xml += ET.tostring(self._pattern, 'utf-8').decode('utf-8')
        xml += ET.tostring(self._topic, 'utf-8').decode('utf-8')
        xml += ET.tostring(self._that, 'utf-8').decode('utf-8')

        xml += "<template>"
        xml += self._template.to_xml(bot, clientid)
        xml += "</template>"

        xml += "</learnf>"

        return xml


######################################################################################################################
#
class TemplateExtensionNode(TemplateNode):

    def __init__(self):
        TemplateNode.__init__(self)
        self._path = None

    @property
    def path(self):
        return self._path

    @path.setter
    def path(self, path):
        self._path = path

    def resolve(self, bot, clientid):
        try:
            data = self.resolve_children_to_string(bot, clientid)

            new_class = ClassLoader.instantiate_class(self._path)
            if new_class is not None:
                instance = new_class()
                resolved = instance.execute(data)

                logging.debug("[%s] resolved to [%s]", self.to_string(), resolved)
                return resolved

        except Exception as excep:
            logging.exception(excep)
            logging.error("Extension [%s] failed to execute", self._path)

        return ""

    def to_string(self):
        return "EXTENSION (%s)" % self._path

    def to_xml(self, bot, clientid):
        xml = '<extension'
        xml += ' path="%s"' % self._path
        xml += '>'
        for child in self.children:
            xml += child.to_xml(bot, clientid)
        xml += '</extension>'
        return xml


######################################################################################################################
#

class TemplateSRAIXNode(TemplateNode):

    def __init__(self):
        TemplateNode.__init__(self)
        self._service = None

    @property
    def service(self):
        return self._service

    @service.setter
    def service(self, service):
        self._service = service

    def resolve(self, bot, clientid):
        resolved = self.resolve_children_to_string(bot, clientid)
        logging.debug("[%s] resolved to [%s]", self.to_string(), resolved)
        response = ""
        try:
            if self._service is not None:
                bot_service = ServiceFactory.get_service(self._service)
                response = bot_service.ask_question(bot, clientid, resolved)
                logging.debug("SRAIX service [%s] return [%s]", self._service, response)
            else:
                logging.error("Sorry SRAIX does not currently have an implementation for [%s]", self._service)
        except Exception as excep:
            logging.error("SRAIX service [%s] failed with error [%s]", self._service, str(excep))
        return response

    def to_string(self):
        return "SRAIX (service=%s)" % (self._service)

    def to_xml(self, bot, clientid):
        xml = '<sraix'
        if self._service is not None:
            xml += ' service="%s"' % self.service
        xml += '>'
        for child in self.children:
            xml += child.to_xml(bot, clientid)
        xml += '</sraix>'
        return xml

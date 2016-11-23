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
from random import randint
from programy.parser.exceptions import ParserException
from datetime import datetime
from dateutil.relativedelta import relativedelta

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

    def output(self, tabs="", output=logging.debug):
        self.output_child(self, tabs, output)

    def output_child(self, node, tabs, output=logging.debug):
        for child in node._children:
            output("%s{%s}" % (tabs, child.format()))
            self.output_child(child, tabs + "\t")

    def resolve_children_to_string(self, bot, clientid):
        return " ".join([child.resolve(bot, clientid) for child in self._children])

    def resolve(self, bot, clientid):
        resolved = " ".join([child.resolve(bot, clientid) for child in self._children])
        logging.debug("[%s] resolved to [%s]" % (self.format(), resolved))
        return resolved

    def format(self):
        return "[NODE]"


######################################################################################################################
#
class TemplateWordNode(TemplateNode):
    def __init__(self, word):
        TemplateNode.__init__(self)
        self.word = word

    def resolve(self, bot, clientid):
        logging.debug("[%s] resolved to [%s]" % (self.format(), self.word))
        return self.word

    def format(self):
        return "[WORD]" + self.word


######################################################################################################################
#
class TemplateRandomNode(TemplateNode):
    def __init__(self):
        TemplateNode.__init__(self)

    def resolve(self, bot, clientid):
        selection = randint(0, len(self._children))
        resolved = self._children[selection - 1].resolve(bot, clientid)
        logging.debug("[%s] resolved to [%s]" % (self.format(), resolved))
        return resolved

    def format(self):
        return "[RANDOM] %d" % (len(self._children))


######################################################################################################################
#
class TemplateSRAINode(TemplateNode):
    def __init__(self):
        TemplateNode.__init__(self)

    def resolve(self, bot, clientid):
        srai_text = " ".join([child.resolve(bot, clientid) for child in self._children])
        resolved = bot.ask_question(clientid, srai_text)
        logging.debug("[%s] resolved to [%s]" % (self.format(), resolved))
        return resolved

    def format(self):
        return "[SRAI]"


######################################################################################################################
#
class TemplateSrNode(TemplateNode):
    def __init__(self):
        TemplateNode.__init__(self)

    def resolve(self, bot, clientid):
        sentence = bot.get_conversation(clientid).current_question().current_sentence()

        if len(sentence.stars) > 0:
            resolved = bot.ask_question(clientid, sentence.stars[0])
        else:
            logging.error("Sr node has no stars available")
            resolved = ""
        logging.debug("[%s] resolved to [%s]" % (self.format(), resolved))
        return resolved

    def format(self):
        return "SR"


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
    def __init__(self):
        TemplateAttribNode.__init__(self)
        self._position = 1
        self._index = 1

    @property
    def index(self):
        return self._index

    def set_attrib(self, attrib_name, attrib_value):

        if attrib_name != 'index':
            raise ParserException("Invalid attribute name [%s] for this node" % (attrib_name))

        if type(attrib_value) is int:
            int_val = attrib_value
            self._index = int_val
        else:
            splits = attrib_value.split(",")
            if len(splits) == 1:
                try:
                    self._index = int(splits[0])
                except Exception as e:
                    logging.exception(e)
                    raise ParserException("None numeric format [%s] for this node [%s], either 'x' or 'x,y'" % (attrib_value, attrib_name))
            elif len(splits) == 2:
                try:
                    self._position = int(splits[0])
                    self._index = int(splits[1])
                except Exception as e:
                    logging.exception(e)
                    raise ParserException("None numeric format [%s] for this node [%s], either 'x' or 'x,y'" % (attrib_value, attrib_name))

        if self._index == 0:
            raise ParserException("Index values are 1 based, cannot be 0")
        if self._position == 0:
            raise ParserException("Position values are 1 based, cannot be 0")


######################################################################################################################
#
class TemplateStarNode(TemplateIndexedNode):
    def __init__(self):
        TemplateIndexedNode.__init__(self)

    def resolve(self, bot, clientid):
        sentence = bot.get_conversation(clientid).current_question().current_sentence()

        if self.index <= len(sentence.stars):
            resolved = sentence.stars[self.index -1]
        else:
            logging.error("Star index not in range [%d] -> [%d]" % (self.index , len(sentence.stars)))
            resolved = ""
        logging.debug("[%s] resolved to [%s]" % (self.format(), resolved))
        return resolved

    def format(self):
        return "STAR Index=%s" % self.index


######################################################################################################################
#
class TemplateSetNode(TemplateNode):
    def __init__(self):
        TemplateNode.__init__(self)
        self.name = None
        self.local = True

    def resolve_children(self, bot, clientid):
        if len(self._children) > 0:
            return " ".join([child.resolve(bot, clientid) for child in self._children])
        else:
            return ""

    def resolve(self, bot, clientid):
        name = self.name.resolve(bot, clientid)
        value = self.resolve_children(bot, clientid)

        if self.local is True:
            logging.debug("[%s] resolved to local: [%s] => [%s]" % (self.format(), name, value))
            bot.get_conversation(clientid).current_question().current_sentence().set_predicate(name, value)

        else:
            if bot.brain.properties.has_property(name):
                logging.error("Global property already exists for name [%s], ignoring set!" % name)
            else:
                logging.debug("[%s] resolved to global: [%s] => [%s]" % (self.format(), name, value))
                bot.get_conversation(clientid).set_predicate(name, value)

        return value

    def format(self):
        return "[SET [%s] - %s]" % ("Local" if self.local else "Global", self.name.format())


######################################################################################################################
#
class TemplateGetNode(TemplateNode):
    def __init__(self):
        TemplateNode.__init__(self)
        self.name = None
        self.local = False

    def resolve(self, bot, clientid):
        name = self.name.resolve(bot, clientid)
        if self.local is True:
            value = bot.get_conversation(clientid).current_question().current_sentence().predicate(name)
            if value is None:
                logging.warning("No local var for %s, default-get used" % (name))
                value = bot.brain.properties.property("default-get")
                if value is None:
                    logging.error("No value for default-get defined, empty string returned")
                    value = ""
            logging.debug("[%s] resolved to global: [%s] <= [%s]" % (self.format(), name, value))
        else:
            value = bot.get_conversation(clientid).predicate(name)
            if value is None:
                value = bot.brain.properties.property("default-get")
                if value is None:
                    logging.error("No value for default-get defined, empty string returned")
                    value = ""
            logging.debug("[%s] resolved to global: [%s] <= [%s]" % (self.format(), name, value))

        return value

    def format(self):
        return "[GET [%s] - %s]" % ("Local" if self.local else "Global", self.name.format())

    def output(self, tabs="", output=logging.debug):
        self.output_child(self, tabs, output)


######################################################################################################################
#
class TemplateMapNode(TemplateNode):
    def __init__(self):
        TemplateNode.__init__(self)
        self.name = None

    def resolve_children(self, bot, clientid):
        if len(self._children) > 0:
            return " ".join([child.resolve(bot, clientid) for child in self._children])
        else:
            return ""

    def resolve(self, bot, clientid):
        name = self.name.resolve(bot, clientid)
        map = bot.brain.maps.map(name)
        if map is None:
            value = bot.brain.properties.property("default-map")
            if value is None:
                logging.error("No value for default-map defined, empty string returned")
                value = ""
        else:
            var = self.resolve_children(bot, clientid)
            if var in map:
                value = map[var]
                if value is None:
                    logging.error("No value for default-map defined, empty string returned")
                    value = ""
            else:
                value = bot.brain.properties.property("default-map")
                if value is None:
                    logging.error("No value for default-map defined, empty string returned")
                    value = ""

        logging.debug("[%s] resolved to [%s] = [%s]" % (self.format(), name, value))
        return value

    def format(self):
        return "[MAP (%s)]" % (self.name.format())

    def output(self, tabs="", output=logging.debug):
        self.output_child(self, tabs, output=logging.debug)


######################################################################################################################
#
class TemplateBotNode(TemplateNode):
    def __init__(self):
        TemplateNode.__init__(self)
        self.name = None

    def resolve(self, bot, clientid):
        name = self.name.resolve(bot, clientid)
        value = bot.brain.properties.property(name)
        if value is None:
            value = bot.brain.properties.property("default-property")
            if value is None:
                value = ""

        logging.debug("[%s] resolved to [%s] = [%s]" % (self.format(), name, value))
        return value

    def format(self):
        return "[BOT (%s)]" % (self.name.format())

    def output(self, tabs="", output=logging.debug):
        self.output_child(self, tabs, output)


######################################################################################################################
#
class TemplateConditionNode(TemplateNode):
    def __init__(self):
        TemplateNode.__init__(self)

    def _get_predicate_value(self, bot, clientid, name, local):

        if local is False:
            value = bot.conversation(clientid).predicate(name)
        else:
            value = bot.conversation(clientid).current_question().current_sentence().predicate(name)

        if value is None:
            value = bot.brain.properties.property("default-get")
            if value is None:
                logging.error("No value for default-get defined, empty string returned")
                value = ""
        return value

    def get_default(self):
        for child in self.conditions:
            if child.is_default() is True:
                return child
        return None


class TemplateType1ConditionNode(TemplateConditionNode):
    def __init__(self):
        TemplateConditionNode.__init__(self)
        self.local = False
        self.name = None
        self.value = None
        self.loop = False

    def resolve(self, bot, clientid):
        value = self._get_predicate_value(bot, clientid, self.name, self.local)
        if value == self.value:
            resolved = " ".join([child.resolve(bot, clientid) for child in self.children])
        else:
            resolved = ""

        logging.debug("[%s] resolved to [%s]" % (self.format(), resolved))
        return resolved

    def format(self):
        return "[CONDITION1(%s=%s)]" % (self.name, self.value)


class TemplateConditionNodeWithChildren(TemplateConditionNode):
    def __init__(self):
        TemplateConditionNode.__init__(self)
        self.conditions = []


class TemplateType2ConditionNode(TemplateConditionNodeWithChildren):
    def __init__(self):
        TemplateConditionNodeWithChildren.__init__(self)
        self.name = None
        self.local = False
        self.loop = False

    def resolve(self, bot, clientid):

        value = self._get_predicate_value(bot, clientid, self.name, self.local)

        for condition in self.conditions:
            if condition.is_default() is False:
                if value == condition.value:
                    resolved = " ".join([child_node.resolve(bot, clientid) for child_node in condition._children])
                    logging.debug("[%s] resolved to [%s]" % (self.format(), resolved))

                    if condition.loop is True:
                        resolved = resolved.strip() + " " + self.resolve(bot, clientid)

                    return resolved

        default = self.get_default()
        if default is not None:
            resolved = " ".join([child_node.resolve(bot, clientid) for child_node in default._children])

            if default.loop is True:
                resolved = resolved.strip() + " " + self.resolve(bot, clientid)
        else:
            resolved = ""
        logging.debug("[%s] resolved to [%s]" % (self.format(), resolved))

        return resolved

    def format(self):
        return "[CONDITION2(%s)]" % self.name


class TemplateConditionListItemNode(TemplateNode):
    def __init__(self):
        TemplateNode.__init__(self)
        self.name = None
        self.value = None
        self.local = False
        self.loop = False

    def is_default(self):
        if self.value is None:
            return True
        else:
            return False

    def resolve(self, bot, clientid):
        pass

    def format(self):
        return "[CONDITIONLIST(%s=%s)]" % (self.name, self.value)


class TemplateType3ConditionNode(TemplateConditionNodeWithChildren):
    def __init__(self):
        TemplateConditionNodeWithChildren.__init__(self)

    def resolve(self, bot, clientid):
        for condition in self.children:
            value = self._get_predicate_value(bot, clientid, condition.name, condition.local)
            if value == condition.value:
                resolved = " ".join([child_node.resolve(bot, clientid) for child_node in condition._children])
                logging.debug("[%s] resolved to [%s]" % (self.format(), resolved))

                if condition.loop is True:
                    resolved = resolved.strip() + " " + self.resolve(bot, clientid).strip()

                return resolved

        default = self.get_default()
        if default is not None:
            resolved = " ".join([child_node.resolve(bot, clientid) for child_node in default._children])

            if default.loop is True:
                resolved = resolved.strip() + " " + self.resolve(bot, clientid).strip()

        else:
            resolved = ""
        logging.debug("[%s] resolved to [%s]" % (self.format(), resolved))

        return resolved

    def format(self):
        return "[CONDITION3()]"



######################################################################################################################
#
class TemplateThinkNode(TemplateNode):
    def __init__(self):
        TemplateNode.__init__(self)

    def resolve(self, bot, clientid):
        resolved = " ".join([child.resolve(bot, clientid) for child in self._children])
        logging.debug("[%s] resolved to [%s]" % (self.format(), resolved))
        return ""

    def format(self):
        return "THINK"


######################################################################################################################
#
class TemplateLowercaseNode(TemplateNode):
    def __init__(self):
        TemplateNode.__init__(self)

    def resolve(self, bot, clientid):
        resolved = " ".join([child.resolve(bot, clientid) for child in self._children])
        resolved = resolved.lower()
        logging.debug("[%s] resolved to [%s]" % (self.format(), resolved))
        return resolved

    def format(self):
        return "LOWERCASE"


######################################################################################################################
#
class TemplateUppercaseNode(TemplateNode):
    def __init__(self):
        TemplateNode.__init__(self)

    def resolve(self, bot, clientid):
        resolved = " ".join([child.resolve(bot, clientid) for child in self._children])
        resolved = resolved.upper()
        logging.debug("[%s] resolved to [%s]" % (self.format(), resolved))
        return resolved

    def format(self):
        return "UPPERCASE"


######################################################################################################################
#
class TemplateFormalNode(TemplateNode):
    def __init__(self):
        TemplateNode.__init__(self)

    def resolve(self, bot, clientid):
        result = " ".join([child.resolve(bot, clientid) for child in self._children])
        return result.title()

    def format(self):
        return "FORMAL"


######################################################################################################################
#
class TemplateSentenceNode(TemplateNode):
    def __init__(self):
        TemplateNode.__init__(self)

    def resolve(self, bot, clientid):
        result = " ".join([child.resolve(bot, clientid) for child in self._children])
        first = result[:1]
        rest = result[1:]
        resolved = first.upper() + rest.lower()
        logging.debug("[%s] resolved to [%s]" % (self.format(), resolved))
        return resolved

    def format(self):
        return "SENTENCE"


######################################################################################################################
#
class TemplateExplodeNode(TemplateNode):
    def __init__(self):
        TemplateNode.__init__(self)

    def resolve(self, bot, clientid):
        result = " ".join([child.resolve(bot, clientid) for child in self._children])
        letters = [ch for ch in result if ch != ' ']
        resolved = " ".join(letters)
        logging.debug("[%s] resolved to [%s]" % (self.format(), resolved))
        return resolved

    def format(self):
        return "EXPLODE"


######################################################################################################################
#
class TemplateImplodeNode(TemplateNode):
    def __init__(self):
        TemplateNode.__init__(self)

    def resolve(self, bot, clientid):
        result = " ".join([child.resolve(bot, clientid) for child in self._children])
        letters = [ch for ch in result if ch != ' ']
        resolved = "".join(letters)
        logging.debug("[%s] resolved to [%s]" % (self.format(), resolved))
        return resolved

    def format(self):
        return "IMPLODE"


######################################################################################################################
#
class TemplateIdNode(TemplateNode):
    def __init__(self):
        TemplateNode.__init__(self)

    def resolve(self, bot, clientid):
        logging.debug("[%s] resolved to [%s]" % (self.format(), clientid))
        return clientid

    def format(self):
        return "ID"


######################################################################################################################
#
class TemplateVocabularyNode(TemplateNode):
    def __init__(self):
        TemplateNode.__init__(self)

    def resolve(self, bot, clientid):
        set_words = bot.brain.sets.count_words_in_sets()
        pattern_words = bot.brain.aiml_parser.pattern_parser.count_words_in_patterns()
        resolved = "%d" % (set_words + pattern_words)
        logging.debug("[%s] resolved to [%s]" % (self.format(), resolved))
        return resolved

    def format(self):
        return "VOCABULARY"


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
        logging.debug("[%s] resolved to [%s]" % (self.format(), resolved))
        return resolved

    def format(self):
        return "PROGRAM"


######################################################################################################################
#
"""
    Code	Meaning	Example
    %a	    Weekday as locale’s abbreviated name.	Mon
    %A	    Weekday as locale’s full name.	Monday
    %w	    Weekday as a decimal number, where 0 is Sunday and 6 is Saturday.	1
    %d	    Day of the month as a zero-padded decimal number.	30
    %-d	    Day of the month as a decimal number. (Platform specific)	30
    %b	    Month as locale’s abbreviated name.	Sep
    %B	    Month as locale’s full name.	September
    %m	    Month as a zero-padded decimal number.	09
    %-m	    Month as a decimal number. (Platform specific)	9
    %y	    Year without century as a zero-padded decimal number.	13
    %Y	    Year with century as a decimal number.	2013
    %H	    Hour (24-hour clock) as a zero-padded decimal number.	07
    %-H	    Hour (24-hour clock) as a decimal number. (Platform specific)	7
    %I	    Hour (12-hour clock) as a zero-padded decimal number.	07
    %-I	    Hour (12-hour clock) as a decimal number. (Platform specific)	7
    %p	    Locale’s equivalent of either AM or PM.	AM
    %M	    Minute as a zero-padded decimal number.	06
    %-M	    Minute as a decimal number. (Platform specific)	6
    %S	    Second as a zero-padded decimal number.	05
    %-S	    Second as a decimal number. (Platform specific)	5
    %f	    Microsecond as a decimal number, zero-padded on the left.	000000
    %z	    UTC offset in the form +HHMM or -HHMM (empty string if the the object is naive).
    %Z	    Time zone name (empty string if the object is naive).
    %j	    Day of the year as a zero-padded decimal number.	273
    %-j	    Day of the year as a decimal number. (Platform specific)	273
    %U	    Week number of the year (Sunday as the first day of the week) as a zero padded decimal number.
    %W	    Week number of the year (Monday as the first day of the week) as a decimal number.
    %c	    Locale’s appropriate date and time representation.	Mon Sep 30 07:06:05 2013
    %x	    Locale’s appropriate date representation.	09/30/13
    %X	    Locale’s appropriate time representation.	07:06:05
    %%	    A literal '%' character.	%
"""

class TemplateDateNode(TemplateAttribNode):
    def __init__(self, date_format=None):
        TemplateAttribNode.__init__(self)
        if date_format is None:
            self._format = "%c"
        else:
            self._format = date_format

    def resolve(self, bot, clientid):
        time_now = datetime.now()
        resolved = time_now.strftime(self._format)
        logging.debug("[%s] resolved to [%s]" % (self.format(), resolved))
        return resolved

    def format(self):
        return "DATE format=%s" % (self._format)

    def set_attrib(self, attrib_name, attrib_value):
        if attrib_name != 'format':
            raise ParserException("Invalid attribute name %s for this node" % (attrib_name))
        self._format = attrib_value


######################################################################################################################
#
class TemplateIntervalNode(TemplateNode):
    def __init__(self, date_format="%c", style="days"):
        TemplateNode.__init__(self)
        self._format = date_format
        self._style = style
        self._from = None
        self._to = None
        if isinstance(style, str):
            self._style = TemplateWordNode(style)
        else:
            self._style = style

    def resolve(self, bot, clientid):
        try:
            format_str = self._format.resolve(bot, clientid)

            from_str = self._from.resolve(bot, clientid)
            from_time = datetime.strptime(from_str, format_str)

            to_str = self._to.resolve(bot, clientid)
            to_time = datetime.strptime(to_str, format_str)

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
                resolved = str(difference.days)
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
                           (  difference.hours, difference.minutes, difference.seconds)
            elif style == "ymdhms":
                resolved = "%d years, %d months, %d days, %d hours, %d minutes, %d seconds" % \
                           (difference.years, difference.months, difference.days,
                            difference.hours, difference.minutes, difference.seconds)
            else:
                logging.error("Unknown interval style [%s]" % (style))
                resolved = ""

            logging.debug("[%s] resolved to [%s]" % (self.format(), resolved))
            return resolved

        except Exception as e:
            logging.exception(e)
            return ""

    def format(self):
        return "[INTERVAL (format=%s, style=%s, from=%s, to=%s)]" % (
        self._format, self._style, self._from, self._to)


######################################################################################################################
#
class TemplateSystemNode(TemplateAttribNode):
    def __init__(self):
        TemplateAttribNode.__init__(self)
        self._timeout = 0

    def resolve(self, bot, clientid):
        if bot.brain._configuration.allow_system_aiml is True:
            command = " ".join([child.resolve(bot, clientid) for child in self._children])
            p = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
            result = []
            for line in p.stdout.readlines():
                byte_string = line.decode("utf-8")
                result.append(byte_string.strip())
            p.wait()
            resolved = " ".join(result)
        else:
            logging.warning("System command node disabled in config")
            resolved = ""
        logging.debug("[%s] resolved to [%s]" % (self.format(), resolved))
        return resolved

    def format(self):
        return "SYSTEM timeout=%s" % (self._timeout)

    def set_attrib(self, attrib_name, attrib_value):
        if attrib_name != 'timeout':
            raise ParserException("Invalid attribute name %s for this node" % (attrib_name))
        logging.warning("System node timeout attrib currently ignored")
        self._timeout = attrib_value


######################################################################################################################
#
class TemplateSizeNode(TemplateNode):
    def __init__(self):
        TemplateNode.__init__(self)

    def resolve(self, bot, clientid):
        resolved = str(bot.brain.aiml_parser.num_categories)
        logging.debug("[%s] resolved to [%s]" % (self.format(), resolved))
        return resolved

    def format(self):
        return "SIZE"


######################################################################################################################
#
# <input index=”n”/> is replaced with the value of the nth previous sentence input to the bot.
#
class TemplateInputNode(TemplateIndexedNode):
    def __init__(self):
        TemplateIndexedNode.__init__(self)

    def resolve(self, bot, clientid):
        conversation = bot.get_conversation(clientid)
        sentence = conversation.nth_sentence(self.index)
        resolved = sentence
        logging.debug("[%s] resolved to [%s]" % (self.format(), resolved))
        return resolved

    def format(self):
        return "INPUT Index=%s" % (self.index)


######################################################################################################################
#
# <request index=”n”/> is replaced with the value of the nth previous multi-sentence input to the bot.
#
class TemplateRequestNode(TemplateIndexedNode):
    def __init__(self):
        TemplateIndexedNode.__init__(self)

    def resolve(self, bot, clientid):
        try:
            nth_question = self.index
            conversation = bot.get_conversation(clientid)
            question = conversation.nth_question(nth_question)
            sentences = question.combine_sentences()
            resolved = sentences
        except Exception as ex:
            logging.exception(ex)
            resolved = ""
        logging.debug("[%s] resolved to [%s]" % (self.format(), resolved))
        return resolved

    def format(self):
        return "REQUEST Index=%s" % (self.index)


######################################################################################################################
#
# <response index=”n”/> is replaced with the value of the nth previous multi-sentence bot response..
#
class TemplateResponseNode(TemplateIndexedNode):
    def __init__(self):
        TemplateIndexedNode.__init__(self)

    def resolve(self, bot, clientid):
        try:
            nth_question = self.index
            conversation = bot.get_conversation(clientid)
            question = conversation.nth_question(nth_question)
            responses = question.combine_answers()
            resolved = responses
        except Exception as ex:
            logging.exception(ex)
            resolved = ""
        logging.debug("[%s] resolved to [%s]" % (self.format(), resolved))
        return resolved

    def format(self):
        return "RESPONSE Index=%s" % (self.index)


######################################################################################################################
#
# <that />
# <that index=”n” />
# <that index="m,n" />
#
class TemplateThatNode(TemplateIndexedNode):
    def __init__(self):
        TemplateIndexedNode.__init__(self)

    def resolve(self, bot, clientid):
        try:
            nth_question = self.index
            conversation = bot.get_conversation(clientid)
            question = conversation.nth_question(nth_question)
            responses = question.combine_answers()
            resolved = responses
        except Exception as ex:
            logging.exception(ex)
            resolved = ""
        logging.debug("[%s] resolved to [%s]" % (self.format(), resolved))
        return resolved

    def format(self):
        return "THAT Index=%s" % (self.index)


######################################################################################################################
#
class TemplateTopicStarNode(TemplateIndexedNode):
    def __init__(self):
        TemplateIndexedNode.__init__(self)

    def resolve(self, bot, clientid):
        try:
            sentence = bot.get_conversation(clientid).current_question().current_sentence()

            if self.index > 0:
                if self.index <= len(sentence.topicstars):
                    return sentence.topicstars[self.index - 1]
            else:
                logging.error("Topic Star index not in range [%d] -> [%d]" % (self.index, len(sentence.topicstars)))

        except Exception as e:
            logging.error("Topic Star index is not an integer value [%d]" % self.index)

        return ""

    def format(self):
        return "TOPICSTAR Index=%s" % (self.index)


######################################################################################################################
#
class TemplateThatStarNode(TemplateIndexedNode):
    def __init__(self):
        TemplateIndexedNode.__init__(self)

    def resolve(self, bot, clientid):
        try:
            sentence = bot.get_conversation(clientid).current_question().current_sentence()

            if self.index > 0:
                if self.index <= len(sentence.thatstars):
                    return sentence.thatstars[self.index - 1]
            else:
                logging.error("That Star index not in range [%d] -> [%d]" % (self.index, len(sentence.thatstars)))

        except Exception as e:
            logging.error("That Star index is not an integer value [%d]" % self.index)

        return ""

    def format(self):
        return "THATSTAR Index=%s" % (self.index)


######################################################################################################################
#
class TemplatePersonNode(TemplateNode):
    def __init__(self):
        TemplateNode.__init__(self)

    def resolve(self, bot, clientid):
        string = " ".join([child.resolve(bot, clientid) for child in self._children])
        resolved = bot.brain.persons.personalise_string(string)
        logging.debug("[%s] resolved to [%s]" % (self.format(), resolved))
        return resolved

    def format(self):
        return "PERSON"


######################################################################################################################
#
class TemplatePerson2Node(TemplateNode):
    def __init__(self):
        TemplateNode.__init__(self)

    def resolve(self, bot, clientid):
        string = " ".join([child.resolve(bot, clientid) for child in self._children])
        resolved = bot.brain.person2s.personalise_string(string)
        logging.debug("[%s] resolved to [%s]" % (self.format(), resolved))
        return resolved

    def format(self):
        return "PERSON2"


######################################################################################################################
#
class TemplateGenderNode(TemplateNode):
    def __init__(self):
        TemplateNode.__init__(self)

    def resolve(self, bot, clientid):
        string = " ".join([child.resolve(bot, clientid) for child in self._children])
        resolved = bot.brain.genders.genderise_string(string)
        logging.debug("[%s] resolved to [%s]" % (self.format(), resolved))
        return resolved

    def format(self):
        return "GENDER"


######################################################################################################################
#
class TemplateNormalizeNode(TemplateNode):
    def __init__(self):
        TemplateNode.__init__(self)

    def resolve(self, bot, clientid):
        string = " ".join([child.resolve(bot, clientid) for child in self._children])
        resolved = bot.brain.normals.normalise_string(string)
        logging.debug("[%s] resolved to [%s]" % (self.format(), resolved))
        return resolved

    def format(self):
        return "NORMALIZE"


######################################################################################################################
#
class TemplateDenormalizeNode(TemplateNode):
    def __init__(self):
        TemplateNode.__init__(self)

    def resolve(self, bot, clientid):
        string = " ".join([child.resolve(bot, clientid) for child in self._children])
        resolved = bot.brain.denormals.denormalise_string(string)
        logging.debug("[%s] resolved to [%s]" % (self.format(), resolved))
        return resolved

    def format(self):
        return "DENORMALIZE"


######################################################################################################################
######################################################################################################################
######################################################################################################################
######################################################################################################################
######################################################################################################################
######################################################################################################################
######################################################################################################################
######################################################################################################################

######################################################################################################################
#
class TemplateSRAIXNode(TemplateNode):
    def __init__(self):
        TemplateNode.__init__(self)
        self.host = None
        self.botid = None
        self.hint = None
        self.apikey = None
        self.service = None

    def resolve(self, bot, clientid):
        resolved = "SRAIX -> " + " ".join([child.resolve(bot, clientid) for child in self._children])
        logging.debug("[%s] resolved to [%s]" % (self.format(), resolved))
        return resolved

    def format(self):
        return "[SRAIX (host=%s, botid=%s, hint=%s, apikey=%s, service=%s)]" % (
            self.host, self.botid, self.hint, self.apikey, self.service)


######################################################################################################################
#
class TemplateLearnNode(TemplateNode):
    def __init__(self):
        TemplateNode.__init__(self)

    def resolve(self, bot, clientid):
        logging.debug("[%s] resolved to nothing" % (self.format()))
        return ""

def format(self):
        return "[LEARN]"


######################################################################################################################
#
class TemplateLearnfNode(TemplateNode):
    def __init__(self):
        TemplateNode.__init__(self)

    def resolve(self, bot, clientid):
        logging.debug("[%s] resolved to nothing" % (self.format()))
        return ""

    def format(self):
        return "[LEARNF]"


######################################################################################################################
#
class TemplateEvalNode(TemplateNode):
    def __init__(self):
        TemplateNode.__init__(self)

    def resolve(self, bot, clientid):
        return "EVAL"

    def format(self):
        return "EVAL"



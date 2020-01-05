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
import datetime
from dateutil.relativedelta import relativedelta
from programy.utils.logging.ylogger import YLogger
from programy.parser.template.nodes.base import TemplateNode
from programy.utils.text.text import TextUtils
from programy.parser.template.nodes.word import TemplateWordNode
from programy.parser.exceptions import ParserException


class TemplateIntervalNode(TemplateNode):

    def __init__(self):
        TemplateNode.__init__(self)
        self._interval_format = None
        self._style = None
        self._interval_from = None
        self._interval_to = None

    @property
    def interval_format(self) -> TemplateNode:
        return self._interval_format

    @interval_format.setter
    def interval_format(self, interval_format: TemplateNode):
        if isinstance(interval_format, TemplateNode):
           self._interval_format = interval_format
        else:
            self._interval_format = TemplateWordNode(interval_format)

    @property
    def interval_from(self) -> TemplateNode:
        return self._interval_from

    @interval_from.setter
    def interval_from(self, interval_from):
        if isinstance(interval_from, TemplateNode):
            self._interval_from = interval_from
        else:
            self._interval_from = TemplateWordNode(interval_from)

    @property
    def interval_to(self) -> TemplateNode:
        return self._interval_to

    @interval_to.setter
    def interval_to(self, interval_to):
        if isinstance(interval_to, TemplateNode):
            self._interval_to = interval_to
        else:
            self._interval_to = TemplateWordNode(interval_to)

    @property
    def style(self) -> TemplateNode:
        return self._style

    @style.setter
    def style(self, style):
        if isinstance(style, TemplateNode):
            self._style = style
        else:
            self._style = TemplateWordNode(style)

    def resolve_to_string(self, client_context):
        if self.interval_format is not None:
            format_str = self.interval_format.resolve(client_context)
        else:
            format_str = "%c"

        from_str = self.interval_from.resolve(client_context)
        from_time = datetime.datetime.strptime(from_str, format_str)

        to_str = self.interval_to.resolve(client_context)
        to_time = datetime.datetime.strptime(to_str, format_str)

        diff = to_time - from_time
        difference = relativedelta(to_time, from_time)

        resolved = ""
        style = self.style.resolve(client_context)

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
            YLogger.error(client_context, "Unknown interval style [%s]", style)
            resolved = ""

        YLogger.debug(client_context, "[INTERVAL] resolved to [%s]", resolved)
        return resolved

    def to_string(self):
        return "[INTERVAL]"

    def to_xml(self, client_context):
        xml = '<interval'
        if self.interval_format is not None:
            xml += ' format="%s"' % self.interval_format.to_xml(client_context)
        if self.style is not None:
            xml += ' style="%s"' % self.style.to_xml(client_context)
        xml += '>'
        if self.interval_from is not None:
            xml += '<from>'
            xml += self.interval_from.to_xml(client_context)
            xml += '</from>'
        if self.interval_to is not None:
            xml += '<to>'
            xml += self.interval_to.to_xml(client_context)
            xml += '</to>'
        xml += '</interval>'
        return xml

    #######################################################################################################
    # INTERVAL_EXPRESSION ::== <interval>
    # 							(DATE_ATTRIBUTE_TAGS)
    # 							<style>(TEMPLATE_EXPRESSION)</style>
    # 							<from>(TEMPLATE_EXPRESSION)</from>
    # 							<to>(TEMPLATE_EXPRESSION)</to>
    # 						</interval>

    def parse_expression(self, graph, expression):

        if 'format' in expression.attrib:
            self._interval_format = graph.get_word_node(expression.attrib['format'])

        if 'style' in expression.attrib:
            self._style = graph.get_word_node(expression.attrib['style'])

        if 'from' in expression.attrib:
            self._interval_from = graph.get_word_node(expression.attrib['from'])

        if 'to' in expression.attrib:
            self._interval_to = graph.get_word_node(expression.attrib['to'])

        head_text = self.get_text_from_element(expression)
        self.parse_text(graph, head_text)

        for child in expression:
            tag_name = TextUtils.tag_from_text(child.tag)

            if tag_name == 'format':
                self._interval_format = graph.get_word_node(self.get_text_from_element(child))

            elif tag_name == 'style':
                node = graph.get_base_node()
                node.parse_text(graph, self.get_text_from_element(child))
                for sub_child in child:
                    graph.parse_tag_expression(sub_child, node)
                    node.parse_text(graph, self.get_text_from_element(child))
                self._style = node

            elif tag_name == 'from':
                node = graph.get_base_node()
                node.parse_text(graph, self.get_text_from_element(child))
                for sub_child in child:
                    graph.parse_tag_expression(sub_child, node)
                    node.parse_text(graph, self.get_text_from_element(child))
                self._interval_from = node

            elif tag_name == 'to':
                node = graph.get_base_node()
                node.parse_text(graph, self.get_text_from_element(child))
                for sub_child in child:
                    graph.parse_tag_expression(sub_child, node)
                    node.parse_text(graph, self.get_text_from_element(child))
                self._interval_to = node
            else:
                raise ParserException("No children allows in interval")

            tail_text = self.get_tail_from_element(child)
            self.parse_text(graph, tail_text)

        if self.interval_format is None:
            YLogger.warning(self, "Interval node, format missing, defaulting to '%c'!")
            self._interval_format = TemplateWordNode("%c")

        if self.style is None:
            YLogger.warning(self, "style node, format missing, defaulting to 'days'!")
            self._style = TemplateWordNode("days")

        if self.interval_from is None:
            raise ParserException("interval_from node, format missing !")

        if self.interval_to is None:
            raise ParserException(self, "interval_to node, format missing !")

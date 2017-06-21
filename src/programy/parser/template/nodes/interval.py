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
import datetime
from dateutil.relativedelta import relativedelta
from programy.parser.template.nodes.base import TemplateNode
from programy.parser.template.nodes.word import TemplateWordNode


class TemplateIntervalNode(TemplateNode):

    def __init__(self):
        TemplateNode.__init__(self)
        self._format = None
        self._style = None
        self._interval_from = None
        self._interval_to = None

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

    #######################################################################################################
    # INTERVAL_EXPRESSION ::== <interval>
    # 							(DATE_ATTRIBUTE_TAGS)
    # 							<style>(TEMPLATE_EXPRESSION)</style>
    # 							<from>(TEMPLATE_EXPRESSION)</from>
    # 							<to>(TEMPLATE_EXPRESSION)</to>
    # 						</interval>

    def parse_expression(self, graph, expression):

        if 'format' in expression.attrib:
            self.format = graph.get_word_node(expression.attrib['format'])

        head_text = self.get_text_from_element(expression)
        self.parse_text(graph, head_text)

        for child in expression:
            if child.tag == 'format':
                self.format = graph.get_word_node(self.get_text_from_element(child))
            elif child.tag == 'style':
                node = graph.get_base_node()
                node.parse_text(graph, self.get_text_from_element(child))
                for sub_child in child:
                    graph.parse_tag_expression(sub_child, node)
                    node.parse_text(self.get_text_from_element(child))
                self.style = node

            elif child.tag == 'from':
                node = graph.get_base_node()
                node.parse_text(graph, self.get_text_from_element(child))
                for sub_child in child:
                    graph.parse_tag_expression(sub_child, node)
                    node.parse_text(graph, self.get_text_from_element(child))
                self.interval_from = node

            elif child.tag == 'to':
                node = graph.get_base_node()
                node.parse_text(graph, self.get_text_from_element(child))
                for sub_child in child:
                    graph.parse_tag_expression(sub_child, node)
                    node.parse_text(graph, self.get_text_from_element(child))
                self.interval_to = node
            else:
                graph.parse_tag_expression(child, self)

            tail_text = self.get_tail_from_element(child)
            self.parse_text(graph, tail_text)

        if self.format is None:
            logging.warning("Interval node, format missing, defaulting to 'c%%'!")
            self.format = "%c"
        if self.style is None:
            logging.warning("style node, format missing, defaulting to 'days'!")
            self.style = "days"
        if self.interval_from is None:
            logging.warning("interval_from node, format missing !")
        if self.interval_to is None:
            logging.warning("interval_to node, format missing !")


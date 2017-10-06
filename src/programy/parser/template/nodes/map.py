"""
Copyright (c) 2016-17 Keith Sterling http://www.keithsterling.com

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

import logging

from programy.parser.template.nodes.base import TemplateNode
from programy.parser.exceptions import ParserException
from programy.utils.text.text import TextUtils

class TemplateMapNode(TemplateNode):

    def __init__(self):
        TemplateNode.__init__(self)
        self._name = None

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, name):
        self._name = name

    def resolve_children(self, bot, clientid):
        if self._children:
            return self.resolve_children_to_string(bot, clientid)
        return ""

    def get_default_value(self, bot):
        value = bot.brain.properties.property("default-map")
        if value is None:
            value = bot.brain.properties.property("default-map")
            if value is None:
                if logging.getLogger().isEnabledFor(logging.ERROR):
                    logging.error("No value for default-map defined, empty string returned")
                value = ""
        return value

    def resolve_to_string(self, bot, clientid):
        name = self.name.resolve(bot, clientid).upper()
        var = self.resolve_children(bot, clientid).upper()

        if bot.brain.dynamics.is_dynamic_map(name) is True:
            value = bot.brain.dynamics.dynamic_map(bot, clientid, name, var)
        else:
            if bot.brain.maps.contains(name) is False:
                if logging.getLogger().isEnabledFor(logging.ERROR):
                    logging.error("No map defined for [%s], using default-map as value", var)
                value = self.get_default_value(bot)
            else:
                the_map = bot.brain.maps.map(name)
                if var in the_map:
                    value = the_map[var]
                else:
                    if logging.getLogger().isEnabledFor(logging.ERROR):
                        logging.error("No value defined for [%s], using default-map as value", var)
                    value = self.get_default_value(bot)

        if logging.getLogger().isEnabledFor(logging.DEBUG):
            logging.debug("MAP [%s] resolved to [%s] = [%s]", self.to_string(), name, value)
        return value

    def resolve(self, bot, clientid):
        try:
            return self.resolve_to_string(bot, clientid)
        except Exception as excep:
            logging.exception(excep)
            return ""

    def to_string(self):
        return "[MAP (%s)]" % (self.name.to_string())

    def to_xml(self, bot, clientid):
        xml = "<map "
        xml += ' name="%s"' % self.name.resolve(bot, clientid)
        xml += ">"
        xml += self.children_to_xml(bot, clientid)
        xml += "</map>"
        return xml

    # ######################################################################################################
    # MAP_EXPRESSION ::=
    # <map name="WORD">TEMPLATE_EXPRESSION</map> |
    # <map><name>TEMPLATE_EXPRESSION</name>TEMPLATE_EXPRESSION</map>

    def parse_expression(self, graph, expression):

        name_found = False

        if 'name' in expression.attrib:
            self.name = self.parse_attrib_value_as_word_node(graph, expression, 'name')
            name_found = True

        self.parse_text(graph, self.get_text_from_element(expression))

        for child in expression:
            tag_name = TextUtils.tag_from_text(child.tag)

            if tag_name == 'name':
                self.name = self.parse_children_as_word_node(graph, child)
                name_found = True

            else:
                graph.parse_tag_expression(child, self)

            self.parse_text(graph, self.get_tail_from_element(child))

        if name_found is False:
            raise ParserException("Name not found in map", xml_element=expression)

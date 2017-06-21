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

from programy.parser.template.maps.plural import PluralMap
from programy.parser.template.maps.singular import SingularMap
from programy.parser.template.maps.predecessor import PredecessorMap
from programy.parser.template.maps.successor import SuccessorMap
from programy.parser.template.nodes.base import TemplateNode
from programy.parser.exceptions import ParserException

class TemplateMapNode(TemplateNode):

    def __init__(self):
        TemplateNode.__init__(self)
        self._name = None
        self._internal_maps = {PluralMap.get_name(): PluralMap(),
                               SingularMap.get_name(): SingularMap(),
                               PredecessorMap.get_name(): PredecessorMap(),
                               SuccessorMap.get_name(): SuccessorMap()}

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
        try:
            name = self.name.resolve(bot, clientid).upper()
            var = self.resolve_children(bot, clientid).upper()

            if name in self._internal_maps:
                map = self._internal_maps[name]
                value = map.map(var)
            else:
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
        except Exception as excep:
            logging.exception(excep)
            return ""

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

            if child.tag == 'name':
                self.name = self.parse_children_as_word_node(graph, child)
                name_found = True

            else:
                graph.parse_tag_expression(child, self)

            self.parse_text(graph, self.get_tail_from_element(child))

        if name_found is False:
            raise ParserException("Error, name not found", xml_element=expression)


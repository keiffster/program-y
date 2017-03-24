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

class TemplateMapNode(TemplateNode):

    def __init__(self):
        TemplateNode.__init__(self)
        self._name = None
        # TODO Load this from configuration file
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

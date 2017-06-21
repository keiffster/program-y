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

from programy.utils.classes.loader import ClassLoader
from programy.parser.template.nodes.base import TemplateNode


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
                resolved = instance.execute(bot, clientid, data)

                logging.debug("[%s] resolved to [%s]", self.to_string(), resolved)
                return resolved

        except Exception as excep:
            logging.exception(excep)
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

    #######################################################################################################
    # EXTENSION_EXPRESSION ::== <extension>
    #                               <path>programy.etension.SomeModule</path>
    #                               parameters
    # 						</extension>

    def parse_expression(self, graph, expression):

        if 'path' in expression.attrib:
            self.path = expression.attrib['path']

        head_text = self.get_text_from_element(expression)
        self.parse_text(graph, head_text)

        for child in expression:
            if child.tag == 'path':
                self.path = self.get_text_from_element(child)
            else:
                graph.parse_tag_expression(child, self)

            tail_text = self.get_tail_from_element(child)
            self.parse_text(graph, tail_text)


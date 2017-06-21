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
import xml.etree.ElementTree as ET

from programy.parser.exceptions import ParserException
from programy.parser.template.factory import TemplateNodeFactory

class TemplateGraph(object):

    def __init__(self, aiml_parser=None):
        self._aiml_parser = aiml_parser
        self.node_lookups = None

        template_nodes = None
        if aiml_parser is not None:
            if aiml_parser._brain is not None:
                template_nodes = aiml_parser._brain.configuration.template_nodes

        self._template_factory = TemplateNodeFactory()
        self._template_factory.load_nodes_config_from_file(template_nodes)

    #
    # TEMPLATE_EXPRESSION ::== TEXT | TAG_EXPRESSION | (TEMPLATE_EXPRESSION)*
    #
    def parse_template_expression(self, pattern):
        node = self.get_base_node()
        node.parse_template_node(self, pattern)
        return node

    def get_node_class_by_name(self, name):
        if self._template_factory.exists(name):
            return self._template_factory.new_node_class(name)
        else:
            raise ParserException("No node [%s] registered in Template Node Factory"%(name))

    # Helper function to return TemplateNode
    def get_base_node(self):
        base_class = self.get_node_class_by_name('base')
        return base_class()

    # Helper function to return TemplateWordNode
    def get_word_node(self, text):
        word_class = self.get_node_class_by_name('word')
        return word_class(text)

    def parse_tag_expression(self, expression, branch):
        if self._template_factory.exists(expression.tag):
            node_instance = self._template_factory.new_node_class(expression.tag)()
            node_instance.parse_expression(self, expression)
            branch.children.append(node_instance)
        else:
            self.parse_unknown_as_text_node(expression,branch)

    def parse_oob_expression(self, expression, branch):
        raise ParserException("Error, oob not implemented yet!", xml_element=expression)

    #######################################################################################################
    # 	UNKNONWN NODE
    #   When its a node we don't know, add it as a text node. This deals with html nodes creeping into the text
    def parse_unknown_as_text_node(self, expression, branch):
        value = ET.tostring(expression, encoding="utf-8", method='xml').decode("utf-8")
        tag = expression.tag
        tail = expression.tail
        text_node = self.get_word_node(text="<%s />"%tag)
        branch.children.append(text_node)
        text_node.parse_text(self, tail)

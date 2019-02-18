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

from programy.parser.exceptions import ParserException
from programy.utils.text.text import TextUtils

class TemplateGraph(object):

    def __init__(self, aiml_parser):
        self._aiml_parser = aiml_parser
        self._template_factory = aiml_parser.brain.template_factory

    @property
    def aiml_parser(self):
        return self._aiml_parser

    @property
    def template_factory(self):
        return self._template_factory

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
        tag_name = TextUtils.tag_from_text(expression.tag)
        if self._template_factory.exists(tag_name):
            if tag_name == "condition":
                node_instance = self._template_factory.new_node_class(tag_name)()
            else:
                node_instance = self._template_factory.new_node_class(tag_name)()
            node_instance.parse_expression(self, expression)
            branch.children.append(node_instance)
        else:
            self.parse_unknown_as_xml_node(expression, branch)

    #######################################################################################################
    # 	UNKNONWN NODE
    #   When its a node we don't know, add it as a text node. This deals with html nodes creeping into the text
    def parse_unknown_as_xml_node(self, expression, branch):
        xml_node_class = self.get_node_class_by_name('xml')
        xml_node = xml_node_class()
        branch.children.append(xml_node)
        xml_node.parse_expression(self, expression)

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

from programy.utils.logging.ylogger import YLogger

from programy.parser.template.nodes.base import TemplateNode
from programy.parser.exceptions import ParserException
from programy.utils.text.text import TextUtils


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

    def resolve_children(self, client_context):
        if self._children:
            return self.resolve_children_to_string(client_context)
        return ""

    def resolve_to_string(self, client_context):

        conversation = client_context.bot.get_conversation(client_context)
        name = self.name.resolve(client_context)
        value = self.resolve_children(client_context)

        if self.local is True:
            YLogger.debug(client_context, "[%s] resolved to local: [%s] => [%s]", self.to_string(), name, value)
            conversation.current_question().set_property(name, value)

        elif client_context.brain.dynamics.is_dynamic_var(name) is True:
            client_context.brain.dynamics.set_dynamic_var(client_context, name, value)

        else:
            if client_context.bot.override_properties is False and client_context.brain.properties.has_property(name):
                YLogger.error(client_context, "Global property already exists for name [%s], ignoring set!", name)
                value = client_context.brain.properties.property(name)

            else:
                if client_context.brain.properties.has_property(name):
                    YLogger.warning(client_context, "Global property already exists for name [%s], over writing!", name)
                YLogger.debug(client_context, "[%s] resolved to global: [%s] => [%s]", self.to_string(), name, value)
                conversation.set_property(name, value)

        YLogger.debug(client_context, "[%s] resolved to [%s]", self.to_string(), value)

        return value

    def to_string(self):
        return "[SET [%s] - %s]" % ("Local" if self.local else "Global", self.name.to_string())

    def to_xml(self, client_context):
        xml = "<set"
        if self.local:
            xml += ' var="%s"' % self.name.resolve(client_context)
        else:
            xml += ' name="%s"' % self.name.resolve(client_context)
        xml += ">"
        xml += self.children_to_xml(client_context)
        xml += "</set>"
        return xml

    # ######################################################################################################
    # SET_PREDICATE_EXPRESSION ::==
    # <set name="WORD">TEMPLATE_EXPRESSION</set> |
    # <set><name>TEMPLATE_EXPRESSION</name>TEMPLATE_EXPRESSION</set> |
    # <set var="WORD">TEMPLATE_EXPRESSION</set> |
    # <set><var>TEMPLATE_EXPRESSION</var>TEMPLATE_EXPRESSION</set>

    def parse_expression(self, graph, expression):

        name_found = False
        var_found = False

        if 'name' in expression.attrib:
            self.name = self.parse_attrib_value_as_word_node(graph, expression, 'name')
            self.local = False
            name_found = True

        if 'var' in expression.attrib:
            self.name = self.parse_attrib_value_as_word_node(graph, expression, 'var')
            self.local = True
            var_found = True

        self.parse_text(graph, self.get_text_from_element(expression))

        for child in expression:
            tag_name = TextUtils.tag_from_text(child.tag)

            if tag_name == 'name':
                self.name = self.parse_children_as_word_node(graph, child)
                self.local = False
                name_found = True

            elif tag_name == 'var':
                self.name = self.parse_children_as_word_node(graph, child)
                self.local = True
                var_found = True

            else:
                graph.parse_tag_expression(child, self)

            self.parse_text(graph, self.get_tail_from_element(child))

        if name_found is True and var_found is True:
            raise ParserException("Set node has both name AND var values", xml_element=expression)

        if name_found is False and var_found is False:
            raise ParserException("Set node has both name AND var values", xml_element=expression)

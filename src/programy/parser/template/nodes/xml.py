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
import xml.etree.ElementTree as ET

from programy.parser.template.nodes.attrib import TemplateAttribNode
from programy.parser.template.nodes.word import TemplateWordNode
from programy.parser.template.nodes.word import TemplateNode
from programy.utils.text.text import TextUtils


class TemplateXMLNode(TemplateAttribNode):

    def __init__(self):
        TemplateAttribNode.__init__(self)
        self._name = None
        self._attribs = {}

    @property
    def attribs(self):
        return self._attribs

    def set_attrib(self, attrib_name, attrib_value):
        self._attribs[attrib_name] = attrib_value

    def resolve_to_string(self, client_context):
        return self.to_xml(client_context)

    def to_string(self):
        return "[XML]"

    def to_xml(self, client_context):
        if self._name is not None:
            xml = "<%s"%self._name
            for attrib_name in self._attribs:
                attrib_node = self._attribs[attrib_name]
                attrib_value = attrib_node.to_xml(client_context)
                escaped = TextUtils.html_escape(attrib_value)
                escaped = escaped.replace(" ", "")
                xml += ' %s="%s"' % (attrib_name, escaped)
            xml += ">"
            child_xml = self.children_to_xml(client_context)
            xml += child_xml
            xml += "</%s>"%self._name
            return xml
        return ""

    def resolve(self, client_context):
        if self._name is not None:
            xml = "<%s"%self._name
            for attrib_name in self._attribs:
                attrib_node = self._attribs[attrib_name]
                attrib_value = attrib_node.resolve(client_context)
                escaped = TextUtils.html_escape(attrib_value)
                escaped = escaped.replace(" ", "")
                xml += ' %s="%s"' % (attrib_name, escaped)
            xml += ">"
            child_xml = self.children_to_xml(client_context)
            xml += child_xml
            xml += "</%s>"%self._name
            return xml
        return ""

    def parse_expression(self, graph, expression):
        self._parse_node_with_attribs(graph, expression)

    def _parse_node_with_attribs(self, graph, expression):

        try:
            self._name = TextUtils.tag_from_text(expression.tag)

            for attrib_name in expression.attrib:
                attrib_value = expression.attrib[attrib_name]
                if "<" in attrib_value and ">" in attrib_value:
                    start = attrib_value.find("<")
                    end = attrib_value.rfind(">")

                    front = attrib_value[:start]
                    middle = attrib_value[start:end+1]
                    back = attrib_value[end+1:]

                    root = TemplateNode()
                    root.append(TemplateWordNode(front))

                    xml = ET.fromstring(middle)
                    xml_node = TemplateNode()
                    graph.parse_tag_expression(xml, xml_node)
                    root.append(xml_node)

                    root.append(TemplateWordNode(back))

                    self.set_attrib(attrib_name, root)

                else:
                    self.set_attrib(attrib_name, TemplateWordNode(attrib_value))

            self.parse_text(graph, self.get_text_from_element(expression))

            for child in expression:
                graph.parse_tag_expression(child, self)
                self.parse_text(graph, self.get_tail_from_element(child))

        except Exception as e:
            print(e)
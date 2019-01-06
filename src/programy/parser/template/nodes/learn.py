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

from programy.parser.template.nodes.base import TemplateNode
from programy.parser.template.nodes.eval import TemplateEvalNode
from programy.utils.text.text import TextUtils
from programy.parser.exceptions import ParserException

class LearnCategory(object):

    def __init__(self, pattern, topic, that, template):
        self._pattern = pattern
        self._topic = topic
        self._that = that
        self._template = template
        self._children = []

    @property
    def pattern(self):
        return self._pattern

    @pattern.setter
    def pattern(self, pattern):
        self._pattern = pattern

    @property
    def topic(self):
        return self._topic

    @topic.setter
    def topic(self, topic):
        self._topic = topic

    @property
    def that(self):
        return self._that

    @that.setter
    def that(self, that):
        self._that = that

    @property
    def template(self):
        return self._template

    @template.setter
    def template(self, template):
        self._template = template

    @property
    def children(self):
        return self._children

    def append(self, category):
        self._children.append(category)

    def to_string(self):
        return "[CATEGORY]"


class TemplateLearnNode(TemplateNode):

    def __init__(self):
        TemplateNode.__init__(self)

    def evaluate_eval_nodes(self, client_context, template):

        new_template = client_context.brain.aiml_parser.template_parser.get_base_node()

        count = 0
        for child in template.children:
            if isinstance(child, TemplateEvalNode):
                new_word_node = client_context.brain.aiml_parser.template_parser.get_word_node(child.resolve(client_context))
                new_template.children.append(new_word_node)
            else:
                new_template.children.append(child)
            count += 1

        return new_template

    def resolve_element_evals(self, client_context, element):

        new_element = ET.Element(element.tag)

        new_element.text = TextUtils.strip_whitespace(element.text)

        for child in element:
            tag_name = TextUtils.tag_from_text(child.tag)

            if tag_name == 'eval':
                eval_str = ET.tostring(child, 'utf-8').decode('ascii')
                eval_str = TextUtils.strip_whitespace(eval_str)
                str_val = "<template>%s</template>" % eval_str
                template = ET.fromstring(str_val)

                ast = client_context.brain.aiml_parser.template_parser.parse_template_expression(template)
                resolved = ast.resolve(client_context)

                new_element.text += " " + resolved
            else:
                new_element.append(child)

        new_element.text = new_element.text.upper()

        if element.tail is not None:
            new_element.tail = TextUtils.strip_whitespace(element.tail)

        return new_element

    def _create_new_category(self, client_context, category, userid="*"):
        new_pattern = self.resolve_element_evals(client_context, category.pattern)
        new_topic = self.resolve_element_evals(client_context, category.topic)
        new_that = self.resolve_element_evals(client_context, category.that)

        new_template = self.evaluate_eval_nodes(client_context, category.template)

        client_context.brain.aiml_parser.pattern_parser.add_pattern_to_graph(new_pattern, new_topic, new_that, new_template, learn=True, userid=client_context.userid)

        YLogger.debug(client_context, "[%s] resolved to new pattern [[%s] [%s] [%s]", self.to_string(),
                      ET.tostring(new_pattern, 'utf-8').decode('utf-8'),
                      ET.tostring(new_topic, 'utf-8').decode('utf-8'),
                      ET.tostring(new_that, 'utf-8').decode('utf-8'))

        return LearnCategory(new_pattern, new_topic, new_that, new_template)

    def resolve_to_string(self, client_context):
        for category in self.children:
            self._create_new_category(client_context, category, userid=client_context.userid)
        return ""

    def to_string(self):
        return "[LEARN]"

    def children_to_xml(self, client_context):
        xml = ""
        for category in self.children:
            xml += "<category>"
            xml += ET.tostring(category.pattern, 'utf-8').decode('utf-8')
            xml += ET.tostring(category.topic, 'utf-8').decode('utf-8')
            xml += ET.tostring(category.that, 'utf-8').decode('utf-8')
            xml += "<template>"
            xml += category.template.to_xml(client_context)
            xml += "</template>"
            xml += "</category>"
        return xml

    def to_xml(self, client_context):
        xml = "<learn>"
        xml += self.children_to_xml(client_context)
        xml += "</learn>"
        return xml

    def parse_expression(self, graph, expression):

        for child in expression:
            tag_name = TextUtils.tag_from_text(child.tag)

            if tag_name == 'category':
                parsed = graph.aiml_parser.parse_category(child, namespace=None, topic_element=None, add_to_graph=False)
                learn_category = LearnCategory(parsed[0], parsed[1], parsed[2], parsed[3])
                self.children.append(learn_category)

            elif tag_name == 'topic':
                raise ParserException("Not supported yet")

            else:
                raise ParserException("Invalid tag [%s] found in <learn>"%tag_name)

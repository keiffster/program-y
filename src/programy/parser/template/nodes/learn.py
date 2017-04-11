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

from programy.utils.text.text import TextUtils
from programy.parser.template.nodes.base import TemplateNode
from programy.parser.template.nodes.eval import TemplateEvalNode
from programy.parser.template.nodes.word import TemplateWordNode

class NewTemplate(object):

    def __init__(self, pattern, topic, that, template):
        self._pattern = pattern
        self._topic = topic
        self._that = that
        self._template = template

class TemplateLearnNode(TemplateNode):

    def __init__(self):
        TemplateNode.__init__(self)
        self._pattern = None
        self._topic = None
        self._that = None
        self._template = None

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

    def evaluate_eval_nodes(self, bot, clientid, template):

        new_template = TemplateNode()

        count = 0
        for child in template.children:
            if isinstance(child, TemplateEvalNode):
                new_word_node = TemplateWordNode(child.resolve(bot, clientid))
                new_template.children.append(new_word_node)
            else:
                new_template.children.append(child)
            count += 1

        return new_template

    def resolve_element_evals(self, bot, clientid, element):

        new_element = ET.Element(element.tag)

        new_element.text = TextUtils.strip_whitespace(element.text)

        for child in element:
            if child.tag == 'eval':
                eval_str = ET.tostring(child, 'utf-8').decode('ascii')
                eval_str = TextUtils.strip_whitespace(eval_str)
                str_val = "<template>%s</template>" % eval_str
                template = ET.fromstring(str_val)

                ast = bot.brain.aiml_parser.template_parser.parse_template_expression(template)
                resolved = ast.resolve(bot, clientid)

                new_element.text += " " + resolved
            else:
                new_element.append(child)

        new_element.text = new_element.text.upper ()

        if element.tail is not None:
            new_element.tail = TextUtils.strip_whitespace(element.tail)

        return new_element

    def _create_new_template(self, bot, clientid):
        new_pattern = self.resolve_element_evals(bot, clientid, self._pattern)
        new_topic = self.resolve_element_evals(bot, clientid, self._topic)
        new_that = self.resolve_element_evals(bot, clientid, self._that)

        new_template = self.evaluate_eval_nodes(bot, clientid, self._template)

        bot.brain.aiml_parser.pattern_parser.add_pattern_to_graph(new_pattern, new_topic, new_that, new_template)

        logging.debug("[%s] resolved to new pattern [[%s] [%s] [%s]", self.to_string(),
                      ET.tostring(new_pattern, 'utf-8').decode('utf-8'),
                      ET.tostring(new_topic, 'utf-8').decode('utf-8'),
                      ET.tostring(new_that, 'utf-8').decode('utf-8'))

        return NewTemplate(new_pattern, new_topic, new_that, new_template)

    def resolve(self, bot, clientid):
        try:
            self._create_new_template(bot, clientid)
            return ""
        except Exception as excep:
            logging.exception(excep)
            return ""

    def to_string(self):
        return "LEARN"

    def to_xml(self, bot, clientid):
        xml = "<learn>"

        xml += ET.tostring(self._pattern, 'utf-8').decode('utf-8')
        xml += ET.tostring(self._topic, 'utf-8').decode('utf-8')
        xml += ET.tostring(self._that, 'utf-8').decode('utf-8')

        xml += "<template>"
        xml += self._template.to_xml(bot, clientid)
        xml += "</template>"

        xml += "</learn>"

        return xml

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

from programy.utils.classes.loader import ClassLoader
from programy.parser.template.nodes.learn import TemplateLearnNode


class TemplateLearnfNode(TemplateLearnNode):

    def __init__(self):
        TemplateLearnNode.__init__(self)

    def resolve(self, bot, clientid):
        new_pattern = self.resolve_element_evals(bot, clientid, self._pattern)
        new_topic = self.resolve_element_evals(bot, clientid, self._topic)
        new_that = self.resolve_element_evals(bot, clientid, self._that)

        template = self.evaluate_eval_nodes(bot, clientid, self._template)

        bot.brain.aiml_parser.pattern_parser.add_pattern_to_graph(new_pattern, new_topic, new_that, template)

        logging.debug("[%s] resolved to new pattern [[%s] [%s] [%s]", self.to_string(),
                      ET.tostring(new_pattern, 'utf-8').decode('utf-8'),
                      ET.tostring(new_topic, 'utf-8').decode('utf-8'),
                      ET.tostring(new_that, 'utf-8').decode('utf-8'))

        bot.brain.write_learnf_to_file(bot, clientid, new_pattern, new_topic, new_that, self._template)
        return ""

    def to_string(self):
        return "LEARNF"

    def to_xml(self, bot, clientid):
        xml = "<learnf>"

        xml += ET.tostring(self._pattern, 'utf-8').decode('utf-8')
        xml += ET.tostring(self._topic, 'utf-8').decode('utf-8')
        xml += ET.tostring(self._that, 'utf-8').decode('utf-8')

        xml += "<template>"
        xml += self._template.to_xml(bot, clientid)
        xml += "</template>"

        xml += "</learnf>"

        return xml


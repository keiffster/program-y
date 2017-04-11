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
        try:
            new_template = self._create_new_template(bot, clientid)
            bot.brain.write_learnf_to_file(bot, clientid, new_template._pattern, new_template._topic, new_template._that, new_template._template)
            return ""
        except Exception as excep:
            logging.exception(excep)
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


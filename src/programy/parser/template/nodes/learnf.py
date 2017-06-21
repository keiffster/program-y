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
import os
import xml.etree.ElementTree as ET

from programy.parser.template.nodes.learn import TemplateLearnNode


class TemplateLearnfNode(TemplateLearnNode):

    def __init__(self):
        TemplateLearnNode.__init__(self)

    def resolve(self, bot, clientid):
        try:
            for category in self.children:
                new_node = self._create_new_category(bot, clientid, category)
                self.write_learnf_to_file(bot, clientid, new_node)
            return ""
        except Exception as excep:
            logging.exception(excep)
            return ""

    def to_string(self):
        return "LEARNF"

    def to_xml(self, bot, clientid):
        xml = "<learnf>"
        xml += self.children_to_xml(bot, clientid)
        xml += "</learnf>"
        return xml

    def write_learnf_to_file(self, bot, clientid, category):
        learnf_path = "%s/learnf%s" % (bot.brain._configuration.aiml_files.files, bot.brain._configuration.aiml_files.extension)
        logging.debug("Writing learnf to %s", learnf_path)

        if os.path.isfile(learnf_path) is False:
            file = open(learnf_path, "w+")
            file.write('<?xml version="1.0" encoding="UTF-8"?>\n')
            file.write('<aiml>\n')
            file.write('</aiml>\n')
            file.close()

        tree = ET.parse(learnf_path)
        root = tree.getroot()

        # Add our new element
        child = ET.Element("category")
        child.append(category.pattern)
        child.append(category.topic)
        child.append(category.that)
        child.append(category.template.xml_tree(bot, clientid))

        root.append(child)

        tree.write(learnf_path, method="xml")

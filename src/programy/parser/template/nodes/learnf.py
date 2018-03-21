"""
Copyright (c) 2016-2018 Keith Sterling http://www.keithsterling.com

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
import os
import xml.etree.ElementTree as ET

from programy.parser.template.nodes.learn import TemplateLearnNode


class TemplateLearnfNode(TemplateLearnNode):

    def __init__(self):
        TemplateLearnNode.__init__(self)

    def resolve_to_string(self, client_context):
        for category in self.children:
            new_node = self._create_new_category(client_context, category)
            self.write_learnf_to_file(client_context, new_node)
        return ""

    def resolve(self, client_context):
        try:
            return self.resolve_to_string(client_context)
        except Exception as excep:
            YLogger.exception(client_context, excep)
            return ""

    def to_string(self):
        return "LEARNF"

    def to_xml(self, client_context):
        xml = "<learnf>"
        xml += self.children_to_xml(client_context)
        xml += "</learnf>"
        return xml

    def write_learnf_to_file(self, client_context, category):
        learnf_path = client_context.brain.configuration.defaults.learn_filename
        YLogger.debug(client_context, "Writing learnf to %s", learnf_path)

        if os.path.isfile(learnf_path) is False:
            file = open(learnf_path, "w+", encoding="utf-8")
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
        child.append(category.template.xml_tree(client_context))

        root.append(child)

        tree.write(learnf_path, method="xml")

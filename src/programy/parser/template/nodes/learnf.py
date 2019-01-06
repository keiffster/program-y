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
import os
import xml.etree.ElementTree as ET

from programy.parser.template.nodes.learn import TemplateLearnNode
from programy.storage.factory import StorageFactory

class TemplateLearnfNode(TemplateLearnNode):

    def __init__(self):
        TemplateLearnNode.__init__(self)

    def resolve_to_string(self, client_context):
        for category in self.children:
            new_node = self._create_new_category(client_context, category)
            self.save_learnf(client_context, new_node)
        return ""

    def to_string(self):
        return "[LEARNF]"

    def to_xml(self, client_context):
        xml = "<learnf>"
        xml += self.children_to_xml(client_context)
        xml += "</learnf>"
        return xml

    def save_learnf(self, client_context, category):

        if client_context.bot.client.storage_factory.entity_storage_engine_available(StorageFactory.LEARNF) is True:
            YLogger.info(self, "Saving binary brain to [%s]", StorageFactory.LEARNF)

            storage_engine = client_context.bot.client.storage_factory.entity_storage_engine(StorageFactory.LEARNF)
            learnf_storage = storage_engine.learnf_store()

            learnf_storage.save_learnf(client_context, category)

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

######################################################################################################################
#
class TemplateNode(object):

    def __init__(self):
        self._children = []

    @property
    def children(self):
        return self._children

    def append(self, child):
        self._children.append(child)

    def dump(self, tabs, output_func=logging.debug, verbose=True):
        self.output(tabs, output_func)

    def output(self, tabs="", output=logging.debug):
        self.output_child(self, tabs, output)

    def output_child(self, node, tabs, output=logging.debug):
        for child in node.children:
            output("%s{%s}" % (tabs, child.to_string()))
            self.output_child(child, tabs + "\t")

    def resolve_children_to_string(self, bot, clientid):
        return (" ".join([child.resolve(bot, clientid) for child in self._children])).strip()

    def resolve(self, bot, clientid):
        try:
            resolved = self.resolve_children_to_string(bot, clientid)
            logging.debug("[%s] resolved to [%s]", self.to_string(), resolved)
            return resolved
        except Exception as excep:
            logging.exception(excep)
            return ""

    def to_string(self):
        return "[NODE]"

    def xml_tree(self, bot, clientid):
        param = ["<template>"]
        self.to_xml_children(param, bot, clientid)
        param[0] += "</template>"
        return ET.fromstring(param[0])

    def to_xml(self, bot, clientid):
        xml = ""
        for child in self.children:
            xml += child.to_xml(bot, clientid)
        return xml

    def to_xml_children(self, param, bot, clientid):
        first = True
        for child in self.children:
            if first is False:
                param[0] += " "
            param[0] += child.to_xml(bot, clientid)
            first = False


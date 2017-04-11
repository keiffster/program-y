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

from programy.parser.template.nodes.condchild import TemplateConditionNodeWithChildren


class TemplateType2ConditionNode(TemplateConditionNodeWithChildren):

    def __init__(self, name, local=False):
        TemplateConditionNodeWithChildren.__init__(self)
        self.name = name
        self.local = local

    def resolve(self, bot, clientid):
        try:
            value = self._get_predicate_value(bot, clientid, self.name, self.local)

            for condition in self.children:
                if condition.is_default() is False:
                    condition_value = condition.value.resolve(bot, clientid)
                    #print("Value [%s] =?= [%s]" % (value, condition_value.strip()))
                    if value == condition_value:
                        resolved = " ".join([child_node.resolve(bot, clientid) for child_node in condition.children])
                        logging.debug("[%s] resolved to [%s]", self.to_string(), resolved)

                        if condition.loop is True:
                            resolved = resolved.strip() + " " + self.resolve(bot, clientid)

                        return resolved

            default = self.get_default()
            if default is not None:
                resolved = " ".join([child_node.resolve(bot, clientid) for child_node in default.children])

                if default.loop is True:
                    resolved = resolved.strip() + " " + self.resolve(bot, clientid)
            else:
                resolved = ""

            logging.debug("[%s] resolved to [%s]", self.to_string(), resolved)
            return resolved

        except Exception as excep:
            logging.exception(excep)
            return ""

    def to_string(self):
        return "[CONDITION2(%s)]" % self.name

    def to_xml(self, bot, clientid):
        xml = "<condition"
        if self.local is True:
            xml += ' var="%s"' % self.name
        else:
            xml += ' name="%s"' % self.name
        xml += ">"
        for child in self.children:
            xml += child.to_xml(bot, clientid)
        xml += "</condition>"
        return xml

"""
Copyright (c) 2016-17 Keith Sterling http://www.keithsterling.com

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

from programy.parser.template.nodes.triple import TemplateTripleNode


class TemplateUniqNode(TemplateTripleNode):

    def __init__(self, subject=None, predicate=None, obj=None):
        TemplateTripleNode.__init__(self, subject, predicate, obj)
        self._node_name = "uniq"

    def execute_query(self, bot, clientid):

        # First resolve subj, pred and obj
        subj = self._subject.resolve(bot, clientid)
        pred = self._predicate.resolve(bot, clientid)
        obj = self._object.resolve(bot, clientid)

        # Now see if any are variables rather than data
        if subj.startswith("?"):
            subj_val = None
        else:
            subj_val = subj

        if pred.startswith("?"):
            pred_val = None
        else:
            pred_val = pred

        if obj.startswith("?"):
            obj_val = None
        else:
            obj_val = obj

        triples = bot.brain.triples.match(subject_name=subj_val, predicate_name=pred_val, object_name=obj_val)

        results = []
        for triple in triples:
            result = []
            if subj.startswith("?"):
                result.append(triple[0])
            if pred.startswith("?"):
                result.append(triple[1])
            if obj.startswith("?"):
                result.append(triple[2])
            results.append(result)

        return self.results_to_text(results)

    def results_to_text(self, results):
        text = ""
        for result in results:
            text += "("
            first = True
            for item in result:
                if first is False:
                    text += ", "
                first = False
                text += item
            text += ")"
        return text

    def resolve(self, bot, clientid):
        try:
            resolved = self.execute_query(bot, clientid)
            logging.debug("[%s] resolved to [%s]", self.to_string(), resolved)
            return resolved
        except Exception as excep:
            logging.exception(excep)
            return ""

    def to_string(self):
        return "UNIQ"

    def to_xml(self, bot, clientid):
        xml = "<uniq>"
        xml += self.children_to_xml(bot, clientid)
        xml += "</uniq>"
        return xml

    #######################################################################################################
    # UNIQ_EXPRESSION ::== <person>TEMPLATE_EXPRESSION</person>

    def parse_expression(self, graph, expression):
        super(TemplateUniqNode, self).parse_expression(graph, expression)



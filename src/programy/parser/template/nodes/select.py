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

from programy.parser.template.nodes.base import TemplateNode
from programy.parser.exceptions import ParserException
from programy.utils.text.text import TextUtils


class SelectQuery(object):

    def __init__(self, type, subj, pred, obj):
        self._type = type
        self._subj = subj
        self._pred = pred
        self._obj = obj

    def to_xml(self, bot, clientid):
        xml = ""
        xml += "<%s>" % self._type
        xml += "<subj>%s</subj>"%self._subj
        xml += "<pred>%s</pred>" % self._pred
        xml += "<obj>%s</obj>" % self._obj
        xml += "</%s>" % self._type
        return xml

    def execute_query(self, bot, clientid):

        # First resolve subj, pred and obj
        subj = self._subj.resolve(bot, clientid)
        pred = self._pred.resolve(bot, clientid)
        obj = self._obj.resolve(bot, clientid)

        # Now see if any are variables rather than data
        if subj.startswith("?"):
            subj_var = subj
            subj_val = None
        else:
            subj_var = None
            subj_val = subj

        if pred.startswith("?"):
            pred_var = pred
            pred_val = None
        else:
            pred_var = None
            pred_val = pred

        if obj.startswith("?"):
            obj_var = obj
            obj_val = None
        else:
            obj_var = None
            obj_val = obj

        # If first query, get results and set variables
        # If subsequent query, using variables and check for result

        # Query using subj, pred and obj data
        if self._type == "q":
            triples = bot.brain.triples.match(subject_name=subj_val, predicate_name=pred_val, object_name=obj_val)
        else:
            triples = bot.brain.triples.not_match(subject_name=subj_val, predicate_name=pred_val, object_name=obj_val)

        results = []
        for triple in triples:
            results.append(((subj_var, triple[0]),(pred_var, triple[1]),(obj_var, triple[2])))
        return results


class QueryProcessor(object):

    def process_triples(self, triples, return_vars):
        results = []
        if len(return_vars) == 0:
            for triple in triples:
                results.append([triple[0][1], triple[1][1], triple[2][1]])
        else:
            for triple in triples:
                result = []
                for var in return_vars:
                    if triple[0][0] == var:
                        result.append(triple[0][1])
                    elif triple[1][0] == var:
                        result.append(triple[1][1])
                    elif triple[2][0] == var:
                        result.append(triple[2][1])
                results.append(result)
        return results

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

    def process_queries(self, bot, clientid, return_vars, queries ):
        first_query = queries[0]
        first_triples = first_query.execute_query(bot, clientid)
        results = self.process_triples(first_triples, return_vars)

        if len(queries) > 1:
            for query in queries[1:]:
                next_triples = query.execute_query(bot, clientid)
                next_results = self.process_triples(next_triples, return_vars)
                for result in results:
                    if result not in next_results:
                        results.remove(result)

            if len(results) == 0:
                return ""

        return self.results_to_text(results)


class TemplateSelectNode(TemplateNode):

    def __init__(self):
        TemplateNode.__init__(self)
        self._vars = []
        self._queries = []
        self._processor = QueryProcessor()

    def resolve(self, bot, clientid):
        try:
            resolved = self._processor.process_queries(bot, clientid, self._vars, self._queries)
            logging.debug("[%s] resolved to [%s]", self.to_string(), resolved)
            return resolved
        except Exception as excep:
            logging.exception(excep)
            return ""

    def to_string(self):
        return "SELECT"

    def to_xml(self, bot, clientid):
        xml = "<select>"
        xml += "<vars>"
        for var in self._vars:
            xml += "?%s "%var
        xml += "</vars>"
        for query in self._queries:
            xml += query.to_xml(bot, clientid)
        xml += "</select>"
        return xml

    #######################################################################################################
    # SELECT_EXPRESSION ::== <person>TEMPLATE_EXPRESSION</person>

    def parse_vars(self, vars):
        var_splits = vars.split(" ")
        for var_name in var_splits:
            self._vars.append(var_name)

    def parse_query(self, graph, query_name, query):
        for child in query:
            tag_name = TextUtils.tag_from_text(child.tag)

            if tag_name == 'subj':
                subj = self.parse_children_as_word_node(graph, child)
            elif tag_name == 'pred':
                pred = self.parse_children_as_word_node(graph, child)
            elif tag_name == 'obj':
                obj = self.parse_children_as_word_node(graph, child)
            else:
                logging.warning ("Unknown tag name [%s] in select query"%tag_name)

        if subj is None:
            raise ParserException("<subj> element missing from select query")

        if pred is None:
            raise ParserException("<pred> element missing from select query")

        if obj is None:
            raise ParserException("<obj> element missing from select query")

        self._queries.append(SelectQuery(query_name, subj, pred, obj))

    def parse_expression(self, graph, expression):

        vars = expression.findall('vars')

        if len(vars) > 0:
            if len(vars) > 1:
                logging.warning ("Multiple <vars> found in select tag, using first")
            self.parse_vars(vars[0].text)

        queries = expression.findall('./')
        for query in queries:
            tag_name = TextUtils.tag_from_text(query.tag)
            if tag_name == 'q' or tag_name == 'notq':
                self.parse_query(graph, tag_name, query)

        if len(self.children) > 0:
            raise ParserException("<select> node should not contains child text, use <select><vars></vars><q></q></select> only")



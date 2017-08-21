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
import pickle
import json

from programy.parser.template.nodes.base import TemplateNode
from programy.parser.exceptions import ParserException
from programy.utils.text.text import TextUtils
from programy.rdf.select import RDFSelectStatement
from programy.rdf.query import RDFQuery

class TemplateSelectNode(TemplateNode):

    def __init__(self, query=None):
        TemplateNode.__init__(self)
        if query is None:
            self._query = RDFSelectStatement()
        else:
            self._query = query


    @property
    def query(self):
        return self._query

    def encode_tuples(self, bot, tuples):
        return json.dumps(tuples)
        #return pickle._dumps(tuples)

    def resolve(self, bot, clientid):
        try:
            results = self.query.execute(bot, clientid)
            resolved = json.dumps(results)
            if logging.getLogger().isEnabledFor(logging.DEBUG): logging.debug("[%s] resolved to [%s]", self.to_string(), resolved)
            return resolved
        except Exception as excep:
            logging.exception(excep)
            return ""

    def to_string(self):
        return "SELECT"

    def to_xml(self, bot, clientid):
        xml = "<select>"
        xml += self.query.to_xml(bot, clientid)
        xml += "</select>"
        return xml

    #######################################################################################################
    # SELECT_EXPRESSION ::== <person>TEMPLATE_EXPRESSION</person>

    def parse_vars(self, vars):
        var_splits = vars.split(" ")
        for var_name in var_splits:
            self._query._vars.append(var_name)

    def parse_query(self, graph, query_name, query):

        if query_name == "q":
            query_type = RDFQuery.QUERY
        else:
            query_type = RDFQuery.NOT_QUERY

        for child in query:
            tag_name = TextUtils.tag_from_text(child.tag)

            if tag_name == 'subj':
                subj = self.parse_children_as_word_node(graph, child)
            elif tag_name == 'pred':
                pred = self.parse_children_as_word_node(graph, child)
            elif tag_name == 'obj':
                obj = self.parse_children_as_word_node(graph, child)
            else:
                if logging.getLogger().isEnabledFor(logging.WARNING): logging.warning ("Unknown tag name [%s] in select query"%tag_name)

        if subj is None:
            raise ParserException("<subj> element missing from select query")

        if pred is None:
            raise ParserException("<pred> element missing from select query")

        if obj is None:
            raise ParserException("<obj> element missing from select query")

        self._query._queries.append(RDFQuery(subj, pred, obj, query_type))

    def parse_expression(self, graph, expression):

        vars = expression.findall('vars')

        if len(vars) > 0:
            if len(vars) > 1:
                if logging.getLogger().isEnabledFor(logging.WARNING): logging.warning ("Multiple <vars> found in select tag, using first")
            self.parse_vars(vars[0].text)

        queries = expression.findall('./')
        for query in queries:
            tag_name = TextUtils.tag_from_text(query.tag)
            if tag_name == 'q' or tag_name == 'notq':
                self.parse_query(graph, tag_name, query)

        if len(self.children) > 0:
            raise ParserException("<select> node should not contains child text, use <select><vars></vars><q></q></select> only")



"""
Copyright (c) 2016-17 Keith Sterling http://www.keithsterling.com

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


class RDFSelectStatement(object):

    def __init__(self, variables=None, queries=None):
        self.set_variables(variables)
        self.set_queries(queries)

    def set_variables(self, variables):
        if variables is None:
            self._vars = []
        else:
            self._vars = variables[:]

    @property
    def vars(self):
        return self._vars

    def set_queries(self, queries):
        if queries is None:
            self._queries = []
        else:
            self._queries = queries[:]

    @property
    def queries(self):
        return self._queries

    def to_xml(self, bot, clientid):
        xml = ""
        xml += "<vars>"
        for var in self._vars:
            xml += "%s"%var
        xml += "</vars>"
        for query in self._queries:
            xml += query.to_xml(bot, clientid)
        return xml

    def execute(self, bot, clientid):

        query_params = []
        for query in self._queries:
            query_params.append([query.subject.resolve(bot, clientid), query.predicate.resolve(bot, clientid), query.obj.resolve(bot, clientid)])

        results = bot.brain.rdf.multi_match(query_params)
        return results
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


from programy.rdf.resultset import RDFQueryResultSet


class RDFSelectStatement(object):

    def __init__(self, vars=[], queries=[]):
        self._vars = vars[:]
        self._queries = queries[:]

    @property
    def vars(self):
        return self._vars

    @property
    def queries(self):
        return self._queries

    def execute(self, bot, clientid):

        query = self._queries[0]
        query.to_string(bot, clientid)
        resultset = query.execute(bot, clientid)

        if len(self._queries) > 1:
            for query in self._queries[1:]:
                for result in resultset.results:
                    next_resultset = query.execute(bot, clientid, result)
                resultset = next_resultset

        str = ""
        for result in resultset.results:
            for var in self.vars:
                str += "("
                if result[0][0] == var:
                    str += var
                    str += ", "
                    str += result[0][1]
                if result[1][0] == var:
                    str += var
                    str += ", "
                    str += result[1][1]
                if result[2][0] == var:
                    str += var
                    str += ", "
                    str += result[2][1]
                str += ")"

        return str

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


class RDFQueryResultSet(object):
    def __init__(self, subject, predicate, object, results):
        self._subject = subject
        self._predicate = predicate
        self._object = object
        self._results = results

    @property
    def subject(self):
        return self._subject

    @property
    def predicate(self):
        return self._predicate

    @property
    def object(self):
        return self._object

    @property
    def results(self):
        return self._results

    def get_variable_value(self, var_name, result):
        if self.subject == var_name:
            return result.subject
        if self.predicate == var_name:
            return result.predicate
        if self.object == var_name:
            return result.object

    def to_string(self, eol="\n"):
        str = ""
        for entity in self._results:
            str += entity.to_string(self)
            str += eol
        return str
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

from programy.mappings.base import TripleStringCollection

class TriplesCollection(TripleStringCollection):

    def __init__(self):
        TripleStringCollection.__init__(self)

    def get_split_char(self):
        return ":"

    def split_line(self, line):
        return self.split_line_by_char(line)

    def has_subject(self, subject):
        return self.has_primary(subject)

    def has_predicate(self, subject, predicate):
        return self.has_secondary(subject, predicate)

    def has_objective(self, subject, predicate, objective):
        value = self.value(subject, predicate)
        if value is not None:
            return bool(value == objective)
        return False

    def objective(self, subject, predicate):
        return self.value(subject, predicate)

    def add_triple(self, subject, predicate, objective):
        if subject not in self.triples:
            self.triples[subject] = {}
        self.triples[subject][predicate] = objective

    def delete_triple(self, subject, predicate=None, objective=None):
        if subject in self.triples:
            if predicate is None:
                del self.triples[subject]
            elif len(self.triples[subject]) == 0:
                del self.triples[subject]
            elif predicate in self.triples[subject]:
                if objective is None or objective == self.triples[subject][predicate]:
                    del self.triples[subject][predicate]

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


class RDFStore(object):

    def add_rdf(self, name, subject, predicate, objct):
        raise NotImplementedError("add_rdf missing from RDF Store")

    def load_all(self, set_collection, subdir=True, set_ext=".txt"):
        raise NotImplementedError("load_all_rds missing from RDF Store")

    def load(self, rdf_collection, rdf_name):
        raise NotImplementedError("load missing from RDF Store")

    def split_into_fields(self, line):
        splits = self.split_line_by_char(line)
        if len(splits) > 3:
            return [splits[0], splits[1], self.get_split_char().join(splits[2:])]
        return splits

    def get_split_char(self):
        return ":"

    def split_line_by_char(self, line):
        splits = line.split(self.get_split_char())
        return splits

    def process_line(self, name, fields, id=None):
        if len(fields) == 3:
            subject = fields[0].strip().strip('"')
            predicate = fields[1].strip().strip('"')
            obj = fields[2].strip().strip('"')

            return self.add_rdf(name, subject, predicate, obj)
        return False
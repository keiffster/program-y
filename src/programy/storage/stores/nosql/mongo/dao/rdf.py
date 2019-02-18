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

class RDF(object):

    def __init__(self, name, subject, predicate, object):
        self.id = None
        self.name = name
        self.subject = subject
        self.predicate = predicate
        self.object = object

    def __repr__(self):
        return "<RDF(id='%d', name='%s', subject='%s', predicate='%s', object='%s')>" % (self.id, self.name, self.subject, self.predicate, self.object)

    def to_document(self):
        document = {"name": self.name,
                    "subject": self.subject,
                    "predicate": self.predicate,
                    "object": self.object}
        if self.id is not None:
            document['_id'] = self.id
        return document

    @staticmethod
    def from_document(data):
        rdf = RDF(None, None, None, None)
        if '_id' in data:
            rdf.id = data['_id']
        if 'name' in data:
            rdf.name = data['name']
        if 'subject' in data:
            rdf.subject = data['subject']
        if 'predicate' in data:
            rdf.predicate = data['predicate']
        if 'object' in data:
            rdf.object = data['object']
        return rdf

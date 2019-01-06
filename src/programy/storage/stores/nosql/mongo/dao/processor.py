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
from programy.storage.stores.utils import DAOUtils


class Processor(object):

    def __init__(self, classname):
        self.id = None
        self.classname = classname

    def to_document(self):
        document = {"classname": self.classname}
        if self.id is not None:
            document['_id'] = self.id
        return document


class PreProcessor(Processor):

    def __init__(self, classname):
        Processor.__init__(self, classname)

    def __repr__(self):
        return "<PreProcessor(id='%s', classname='%s')>" % (
        DAOUtils.valid_id(self.id), self.classname)

    @staticmethod
    def from_document(data):
        lookup = PreProcessor(None)
        if '_id' in data:
            lookup.id = data['_id']
        if 'classname' in data:
            lookup.classname = data['classname']
        return lookup



class PostProcessor(Processor):

    def __init__(self, classname):
        Processor.__init__(self, classname)

    def __repr__(self):
        return "<PostProcessor(id='%s', classname='%s')>" % (
        DAOUtils.valid_id(self.id), self.classname)

    @staticmethod
    def from_document(data):
        lookup = PostProcessor(None)
        if '_id' in data:
            lookup.id = data['_id']
        if 'classname' in data:
            lookup.classname = data['classname']
        return lookup

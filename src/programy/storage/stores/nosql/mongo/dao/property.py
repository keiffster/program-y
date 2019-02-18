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

class Property(object):

    def __init__(self, name, value):
        self.id = None
        self.name = name
        self.value = value

    def __repr__(self):
        return "<Property(id='%s', name='%s', value='%s')>" % (DAOUtils.valid_id(self.id), self.name, self.value)

    def to_document(self):
        document = {"name": self.name,
                    "value": self.value}
        if self.id is not None:
            document['_id'] = self.id
        return document

    @staticmethod
    def from_document(data):
        property = Property(None, None)
        if '_id' in data:
            property.id = data['_id']
        if 'name' in data:
            property.name = data['name']
        if 'value' in data:
            property.value = data['value']
        return property


class DefaultVariable(Property):

    def __init__(self, name, value):
        Property.__init__(self, name, value)

    def __repr__(self):
        return "<DefaultVariable(id='%s', name='%s', value='%s')>" % (DAOUtils.valid_id(self.id), self.name, self.value)

    @staticmethod
    def from_document(data):
        property = DefaultVariable(None, None)
        if '_id' in data:
            property.id = data['_id']
        if 'name' in data:
            property.name = data['name']
        if 'value' in data:
            property.value = data['value']
        return property


class Regex(Property):

    def __init__(self, name, value):
        Property.__init__(self, name, value)

    def __repr__(self):
        return "<Regex(id='%s', name='%s', value='%s')>" % (DAOUtils.valid_id(self.id), self.name, self.value)

    @staticmethod
    def from_document(data):
        property = Regex(None, None)
        if '_id' in data:
            property.id = data['_id']
        if 'name' in data:
            property.name = data['name']
        if 'value' in data:
            property.value = data['value']
        return property


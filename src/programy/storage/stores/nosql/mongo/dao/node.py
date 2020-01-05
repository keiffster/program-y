"""
Copyright (c) 2016-2020 Keith Sterling http://www.keithsterling.com

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


class Node():

    def __init__(self, name, node_class):
        self.id = None
        self.name = name
        self.node_class = node_class

    def to_document(self):
        document = {"name": self.name,
                    "node_class": self.node_class}
        if self.id is not None:
            document['_id'] = self.id
        return document


class PatternNode(Node):

    def __init__(self, name, node_class):
        Node.__init__(self, name, node_class)

    def __repr__(self):
        return "<PatternNode(id='%s', name='%s', node_class='%s')>" % (
            DAOUtils.valid_id(self.id), self.name, self.node_class)

    @staticmethod
    def from_document(data):
        node = PatternNode(None, None)
        node.id = DAOUtils.get_value_from_data(data, '_id')
        node.name = DAOUtils.get_value_from_data(data, 'name')
        node.node_class = DAOUtils.get_value_from_data(data, 'node_class')
        return node


class TemplateNode(Node):

    def __init__(self, name, node_class):
        Node.__init__(self, name, node_class)

    def __repr__(self):
        return "<TemplateNode(id='%s', name='%s', node_class='%s')>" % (
            DAOUtils.valid_id(self.id), self.name, self.node_class)

    @staticmethod
    def from_document(data):
        node = TemplateNode(None, None)
        node.id = DAOUtils.get_value_from_data(data, '_id')
        node.name = DAOUtils.get_value_from_data(data, 'name')
        node.node_class = DAOUtils.get_value_from_data(data, 'node_class')
        return node

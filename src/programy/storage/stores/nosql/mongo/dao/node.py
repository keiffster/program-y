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


class Node(object):

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

    def from_document(data):
        node = PatternNode(None, None)
        if '_id' in data:
            node.id = data['_id']
        if 'name' in data:
            node.name = data['name']
        if 'node_class' in data:
            node.node_class = data['node_class']
        return node


class TemplateNode(Node):

    def __init__(self, name, node_class):
        Node.__init__(self, name, node_class)

    def __repr__(self):
        return "<TemplateNode(id='%s', name='%s', node_class='%s')>" % (
        DAOUtils.valid_id(self.id), self.name, self.node_class)

    def from_document(data):
        node = PatternNode(None, None)
        if '_id' in data:
            node.id = data['_id']
        if 'name' in data:
            node.name = data['name']
        if 'node_class' in data:
            node.node_class = data['node_class']
        return node

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

class Variables(object):

    def __init__(self, clientid, userid, variables):
        self.id = None
        self.clientid = clientid
        self.userid = userid
        self.variables = variables

    def __repr__(self):
        return "<Variables(id='%d', clientid='%s', userid='%s', variables='%s')>" % (self.id, self.clientid, self.userid, self.variables)

    def to_document(self):
        document = {"clientid": self.clientid,
                    "userid": self.userid,
                    "variables": self.variables}
        if self.id is not None:
            document['_id'] = self.id
        return document

    @staticmethod
    def from_document(data):
        property = Variables(None, None, None)
        if '_id' in data:
            property.id = data['_id']
        if 'clientid' in data:
            property.clientid = data['clientid']
        if 'userid' in data:
            property.userid = data['userid']
        if 'variables' in data:
            property.variables = {}
            for key, value in data['variables'].items():
                property.variables[key] = value
        return property

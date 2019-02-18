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


class Category(object):

    def __init__(self, groupid, userid, topic, that, pattern, template, id=None):
        self.id = id

        self.groupid = groupid
        self.userid = userid
        self.topic = topic
        self.that = that
        self.pattern = pattern
        self.template = template

    def __repr__(self):
        return "<Category(id='%s', groupid='%s', userid='%s', topic='%s', that='%s', pattern='%s', template='%s'>" % \
               (DAOUtils.valid_id(self.id), DAOUtils.valid_id(self.groupid), DAOUtils.valid_id(self.userid),
                self.topic, self.that, self.pattern, self.template)

    def to_document(self):
        document = {"groupid": self.groupid,
                    "userid": self.userid,
                    "topic": self.topic,
                    "that": self.that,
                    "pattern": self.pattern,
                    "template": self.template}
        if self.id is not None:
            document['_id'] = self.id
        return document

    @staticmethod
    def from_document(data):

        id = DAOUtils.get_value_from_data(data, '_id')
        groupid = DAOUtils.get_value_from_data(data, 'groupid')
        userid = DAOUtils.get_value_from_data(data, 'userid')
        topic = DAOUtils.get_value_from_data(data, 'topic')
        that = DAOUtils.get_value_from_data(data, 'that')
        pattern = DAOUtils.get_value_from_data(data, 'pattern')
        template = DAOUtils.get_value_from_data(data, 'template')

        return Category(id=id, groupid=groupid, userid=userid, topic=topic, that=that, pattern=pattern, template=template)

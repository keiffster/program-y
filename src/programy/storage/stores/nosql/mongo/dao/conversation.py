"""
Copyright (c) 2016-2018 Keith Sterling http://www.keithsterling.com

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

class Conversation(object):

    def __init__(self, clientid, userid, botid, brainid, depth, question, response):
        self.id = None

        self.clientid = clientid
        self.userid = userid
        self.botid = botid
        self.brainid = brainid
        self.depth = depth

        self.question = question
        self.response = response

    def __repr__(self):
        return "<Conversation(id='%s', client='%s', user='%s', bot='%s', brain='%s', depth='%d', question='%s', response='%s')" % \
               (self.id, self.clientid, self.userid, self.botid, self.brainid, self.depth, self.question,
                self.response)

    def to_document(self):
        document = {"clientid": self.clientid,
                    "userid": self.userid,
                    "botid": self.botid,
                    "brainid": self.brainid,
                    "depth": self.depth,
                    "question": self.question,
                    "response": self.response}
        if self.id is not None:
            document['_id'] = self.id
        return document

    @staticmethod
    def from_document(data):
        conversation = Conversation(None, None, None, None, None, None, None)
        if '_id' in data:
            conversation.id = data['_id']
        if 'clientid' in data:
            conversation.clientid = data['clientid']
        if 'botid' in data:
            conversation.botid = data['botid']
        if 'brainid' in data:
            conversation.brainid = data['brainid']
        if 'depth' in data:
            conversation.depth = data['depth']
        if 'question' in data:
            conversation.question = data['question']
        if 'response' in data:
            conversation.response = data['response']
        return conversation
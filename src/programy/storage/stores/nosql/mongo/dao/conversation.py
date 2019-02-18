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
from programy.dialog.conversation import Conversation as Convo

class Conversation(object):

    def __init__(self, client_context, conversation):
        self.id = None

        if client_context is None:
            self.clientid = None
            self.userid = None
            self.botid = None
            self.brainid = None
        else:
            self.clientid = client_context.client.id
            self.userid = client_context.userid
            self.botid = client_context.bot.id
            self.brainid = client_context.brain.id

        self.conversation = conversation

    def __repr__(self):
        return "<Conversation(id='%s', client='%s', user='%s', bot='%s', brain='%s', depth='%d', question='%s', response='%s')" % \
               (self.id, self.clientid, self.userid, self.botid, self.brainid, self.depth)

    def to_document(self):
        document = {"clientid": self.clientid,
                    "userid": self.userid,
                    "botid": self.botid,
                    "brainid": self.brainid,
                    "conversation": self.conversation.to_json()}
        if self.id is not None:
            document['_id'] = self.id
        return document

    @staticmethod
    def from_document(client_context, data):
        conversation = Conversation(client_context, None)
        if '_id' in data:
            conversation.id = data['_id']
        if 'clientid' in data:
            conversation.clientid = data['clientid']
        if 'userid' in data:
            conversation.userid = data['userid']
        if 'botid' in data:
            conversation.botid = data['botid']
        if 'brainid' in data:
            conversation.brainid = data['brainid']

        if 'conversation' in data:
            conversation.conversation = Convo(client_context)
            conversation.conversation.from_json(client_context, data['conversation'])

        return conversation
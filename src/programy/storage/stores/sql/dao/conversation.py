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

from sqlalchemy import Column, Integer, String

from programy.storage.stores.sql.base import Base
from programy.storage.stores.utils import DAOUtils


class Conversation(Base):
    __tablename__ = 'conversations'

    id = Column(Integer, primary_key=True)

    clientid = Column(String(16))
    userid = Column(String(16))
    botid = Column(String(16))
    brainid = Column(String(16))
    question = Column(Integer)
    sentence = Column(String(512))
    response = Column(String(512))

    def __repr__(self):
        return "<Conversation(id='%s', clientid='%s', userid='%s', botid='%s', brainid='%s', question='%s', sentence='%s', response='%s'>" % \
               (DAOUtils.valid_id(self.id),
                self.clientid,
                self.userid,
                self.botid,
                self.brainid,
                self.question,
                self.sentence,
                self.response)


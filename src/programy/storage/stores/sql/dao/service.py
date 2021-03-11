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
from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import Boolean
from programy.storage.stores.sql.base import Base
from programy.storage.stores.utils import DAOUtils


class Service(Base):
    __tablename__ = 'services'

    id = Column(Integer, primary_key=True)
    type = Column(String(48))
    name = Column(String(48))
    category = Column(String(48))
    service_class = Column(String(512))
    default_response = Column(String(128))
    default_srai = Column(String(48))
    default_aiml = Column(String(512))
    success_prefix = Column(String(128))
    load_default_aiml = Column(Boolean(), nullable=False, default=True)
    url = Column(String(100))
    rest_timeout = Column(Integer)
    rest_retries = Column(String(512))

    def __repr__(self):
        if self.type == 'rest':
            return "<Service(id='%s', type='%s', name='%s', category='%s', service_class='%s', " \
                   "default_response='%s', default_srai='%s', default_aiml='%s', " \
                   "load_default_aiml='%s', " \
                   "success_prefix='%s', " \
                   "url='%s', " \
                   "rest_timeout='%s', rest_retries='%s'" \
                   ")>" % (
                DAOUtils.valid_id(self.id), self.type, self.name, self.category, self.service_class,
                self.default_response, self.default_srai, self.default_aiml,
                "False" if self.load_default_aiml is False else "True",
                self.success_prefix,
                self.url,
                self.rest_timeout, self.rest_retries)
        else:
            return "<Service(id='%s', type='%s', name='%s', category='%s', service_class='%s', " \
                   "default_response='%s', default_srai='%s', default_aiml='%s', load_default_aiml='%r', " \
                   "success_prefix='%s', " \
                   "url='%s' " \
                   ")>" % (
                DAOUtils.valid_id(self.id), self.type, self.name, self.category, self.service_class,
                    self.default_response, self.default_srai, self.default_aiml,
                    "False" if self.load_default_aiml is False else "True",
                    self.success_prefix,
                    self.url
                    )


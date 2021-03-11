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


class Service:

    def __init__(self, type=None, name=None, category=None, service_class=None,
                 default_response=None, default_srai=None, default_aiml=None, load_default_aiml=True,
                 success_prefix=None, url=None,
                 rest_timeout=None, rest_retries=None):
        self.id = None
        self.type = type
        self.name = name
        self.category = category
        self.service_class = service_class
        self.default_response = default_response
        self.default_srai = default_srai
        self.default_aiml = default_aiml
        self.load_default_aiml = load_default_aiml
        self.success_prefix = success_prefix
        self.url = url
        self.rest_timeout = rest_timeout
        self.rest_retries = rest_retries

    def to_document(self):
        document = {"type": self.type,
                    "name": self.name,
                    "category": self.category,
                    "service_class": self.service_class,
                    "default_response": self.default_response,
                    "default_srai": self.default_srai,
                    "default_aiml": self.default_aiml,
                    "success_prefix": self.success_prefix,
                    "load_default_aiml": self.load_default_aiml,
                    "url": self.url,
                    "rest_timeout": self.rest_timeout,
                    "rest_retries": self.rest_retries
                    }
        if self.id is not None:
            document['_id'] = self.id
        return document

    def __repr__(self):
        if self.type == 'rest':
            return "<Service(id='%s', type='%s', name='%s', category='%s', service_class='%s, " \
                   "default_response='%s', default_srai='%s', default_aiml='%s', load_default_aiml='%s', " \
                   "success_prefix='%s', " \
                   "url='%s', " \
                   "rest_timeout='%s', rest_retries='%s'" \
                   ")>" % (
                DAOUtils.valid_id(self.id), self.type, self.name, self.category, self.service_class,
                self.default_response, self.default_srai, self.default_aiml, self.load_default_aiml,
                self.success_prefix,
                self.url,
                self.rest_timeout, self.rest_retries)
        else:
            return "<Service(id='%s', type='%s', name='%s', category='%s', service_class='%s'" \
                   "default_response='%s', default_srai='%s', default_aiml='%s', load_default_aiml='%s', " \
                   "success_prefix='%s', " \
                   "url='%s'" \
                   ")>" % (
                DAOUtils.valid_id(self.id), self.type, self.name, self.category, self.service_class,
                    self.default_response, self.default_srai, self.default_aiml, self.load_default_aiml,
                    self.success_prefix, self.url)

    @staticmethod
    def from_document(data):
        service = Service()
        service.id = DAOUtils.get_value_from_data(data, '_id')
        service.type = DAOUtils.get_value_from_data(data, 'type')
        service.name = DAOUtils.get_value_from_data(data, 'name')
        service.category = DAOUtils.get_value_from_data(data, 'category')
        service.default_response = DAOUtils.get_value_from_data(data, 'default_response')
        service.default_srai = DAOUtils.get_value_from_data(data, 'default_srai')
        service.default_aiml = DAOUtils.get_value_from_data(data, 'default_aiml')
        service.success_prefix = DAOUtils.get_value_from_data(data, 'success_prefix')
        service.url = DAOUtils.get_value_from_data(data, 'url')
        service.rest_timeout = DAOUtils.get_value_from_data(data, 'rest_timeout')
        service.rest_retries = DAOUtils.get_value_from_data(data, 'rest_retries')
        return service

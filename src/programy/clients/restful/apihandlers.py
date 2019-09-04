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
from abc import ABCMeta, abstractmethod

from datetime import datetime


class APIHandler(object):
    __metaclass__ = ABCMeta

    UNKNOWN = "Unknown"

    def __init__(self, bot_client):
        self._bot_client = bot_client

    @abstractmethod
    def process_request(self, rest_request, method='GET'):
        raise NotImplementedError()

    @abstractmethod
    def format_success_response(self, userid, question, answer, metadata=None):
        raise NotImplementedError()

    @abstractmethod
    def format_error_response(self, userid, question, error, metadata=None):
        raise NotImplementedError()


class APIHandler_V1_0(APIHandler):

    QUESTION = 'question'
    USERID = 'userid'

    def __init__(self, bot_client):
        APIHandler.__init__(self, bot_client)

    def process_request(self, request, method='GET'):
        question = APIHandler.UNKNOWN
        userid = APIHandler.UNKNOWN

        try:
            question = self._bot_client.get_variable(request, APIHandler_V1_0.QUESTION, method)
            userid = self._bot_client.get_variable(request, APIHandler_V1_0.USERID, method)

            answer = self._bot_client.ask_question(userid, question)

            return self.format_success_response(userid, question, answer), 200

        except Exception as excep:
            return self.format_error_response(userid, question, str(excep)), 500

    def format_success_response(self, userid, question, answer, metadata=None):
        return {'response': {"question": question,
                             "answer": answer,
                             "userid": userid}}

    def format_error_response(self, userid, question, error, metadata=None):
        client_context =  self._bot_client.create_client_context(userid)
        return {"response": {"question": question,
                             "answer": client_context.bot.default_response,
                             "userid": userid,
                             "error": error}}


class APIHandler_V2_0(APIHandler):

    QUERY = "query"
    USERID = 'userId'
    LANG = "lang"
    location = "location"

    def __init__(self, bot_client):
        APIHandler.__init__(self, bot_client)

    def process_request(self, request, method='GET'):
        query = APIHandler_V2_0.UNKNOWN
        userid =  APIHandler_V2_0.UNKNOWN
        #lang =  APIHandler_V2_0.UNKNOWN
        #location =  APIHandler_V2_0.UNKNOWN

        try:
            print(request)
            query = self._bot_client.get_variable(request, APIHandler_V2_0.QUERY, method)
            userid = self._bot_client.get_variable(request, APIHandler_V2_0.USERID, method)
            #lang = self._bot_client.get_variable(request, APIHandler_V2_0.LANG, method)
            #location = self._bot_client.get_variable(request, APIHandler_V2_0.LOCATION, method)

            metadata = {}
            answer = self._bot_client.ask_question(userid, query, metadata)

            return self.format_success_response(userid, query, answer, metadata), 200

        except Exception as excep:
            return self.format_error_response(userid, query, str(excep), None), 500

    def _get_timestamp(self):
        return datetime.timestamp(datetime.now())

    def format_success_response(self, userid, question, answer, metadata):
        payload = {'response': {"query": question,
                             "userId": userid,
                             "timestamp": self._get_timestamp(),
                             "text": answer,
                             },
                    'status': {
                        'code': 200,
                        'message': 'success'
                    }}

        if metadata is not None:
            payload["meta"] = {
                    "botName": metadata['botName'],
                    "version": metadata['version'],
                    "copyright": metadata['copyright'],
                    "authors": metadata['authors']
                }

        return payload

    def format_error_response(self, userid, query, error, metadata):
        payload = {'response': {"query": query,
                                "userId": userid,
                                "timestamp": self._get_timestamp(),
                             },
                'status': {
                    'code': 500,
                    'message': error
                }}

        if metadata is not None:
            payload["meta"] = {
                    "botName": metadata['botName'],
                    "version": metadata['version'],
                    "copyright": metadata['copyright'],
                    "authors": metadata['authors']
                }

        return payload

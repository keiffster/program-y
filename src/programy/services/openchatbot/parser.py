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
from programy.utils.logging.ylogger import YLogger

import json

from programy.services.openchatbot.response import OpenChatBotMeta
from programy.services.openchatbot.response import OpenChatBotStatus
from programy.services.openchatbot.response import OpenChatBotResponse


class OpenChatBotResponseParser(object):

    def __init__(self):
        self.status = None
        self.response = None
        self.meta = None

    def get_response(self, payload):
        if 'response' in payload:
            return OpenChatBotResponse.parse(payload['response'])
        return None

    def get_status(self, payload):
        if 'status' in payload:
            return OpenChatBotStatus.parse(payload['status'])
        return None

    def get_meta(self, payload):
        if 'meta' in payload:
            return OpenChatBotMeta.parse(payload['meta'])
        return None

    def parse_response(self, text):
        try:
            payload = json.loads(text)
            if payload is None:
                YLogger.error(None, "No json payload available")
                return False

        except Exception as exe:
            YLogger.exception(None, "Not valid json in response", exe)
            return False

        self.response = self.get_response(payload)
        if self.response is None:
            return False

        self.status = self.get_status(payload)
        if self.status is None:
            return False

        self.meta = self.get_meta(payload)

        if self.status.code == 200:
            return True

        return False

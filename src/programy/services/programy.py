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
import json
from urllib.parse import quote

from programy.services.rest import GenericRESTService
from programy.config.brain.service import BrainServiceConfiguration


class ProgramyRESTService(GenericRESTService):

    def __init__(self, config: BrainServiceConfiguration, api=None):
        GenericRESTService.__init__(self, config, api)

    def _format_payload(self, client_context, question):
        return {'question': question, "userid": client_context.userid}

    def _format_get_url(self, url, client_context, question):
        return "%s?question=%s&userid=%s"%(url, quote(question), client_context.userid)

    def _parse_response(self, text):
        data = json.loads(text)
        if data:
            if 'response' in data[0]:
                if 'answer' in data[0]['response']:
                    return data[0]['response']['answer']
        return ""

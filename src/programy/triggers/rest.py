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

import requests
import json

from programy.triggers.config import TriggerConfiguration
from programy.context import ClientContext
from programy.triggers.manager import TriggerManager


class RestTriggerManager(TriggerManager):

    def __init__(self, config: TriggerConfiguration):
        TriggerManager.__init__(self, config)

    def post_data(self, api_url_base, headers, payload):
        return requests.post(api_url_base, headers=headers, json=payload)

    def trigger(self, event: str, client_context: ClientContext = None, additional: {} = None) -> bool:

        if client_context is not None:
            assert isinstance(client_context, ClientContext)

        YLogger.debug(client_context, "Event triggered [%s]", event)

        payload = {'event': event}

        if client_context is not None:
            conversation = client_context.bot.get_conversation(client_context)
            payload['conversation'] = conversation.to_json()

        if additional is not None:
            payload['additional'] = additional

        api_url_base = self._config.value("url")
        api_method = self._config.value("method")
        api_token = self._config.value("token")

        headers = {'Content-Type': 'application/json'}
        if api_token is not None:
            headers['Authorisation'] = 'Bearer %s'%api_token

        if api_method is None or api_method.upper() == 'POST':
            response = self.post_data(api_url_base, headers=headers, payload=payload)

            if response.status_code == 200:
                return True

            YLogger.error(None, "Failed to send trigger info via REST [%d]", response.status_code)

        return False

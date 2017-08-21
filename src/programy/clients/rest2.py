"""
Copyright (c) 2016-17 Keith Sterling http://www.keithsterling.com

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated
documentation files (the "Software"), to deal in the Software without restriction, including without limitation
the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software,
and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO
THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT,
TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
"""

#
# curl 'http://localhost:5000/api/v1.0/ask?question=hello+world&sessionid=1234567890'
#

import logging
from sanic import Sanic
from sanic.response import json
from sanic.exceptions import ServerError

from programy.clients.client import BotClient
from programy.config.sections.client.rest import RestConfiguration

class RestBotClient(BotClient):

    def __init__(self, argument_parser=None):
        BotClient.__init__(self, argument_parser)

    def set_environment(self):
        self.bot.brain.properties.add_property("env", "REST")

    def get_client_configuration(self):
        return RestConfiguration()

rest_client = None

print("Initiating REST Service...")
app = Sanic()

# Enter you API keys, here, alternatively store in a db or file and load at startup
# This is an exmaple, and therefore not suitable for production
api_keys = [
]

def is_apikey_valid(apikey):
    if apikey in api_keys:
        return True
    else:
        return False

# Example Usage
#
# curl 'http://localhost:5000/api/v1.0/ask?question=hello+world&sessionid=1234567890'
#
@app.route('/api/v1.0/ask', methods=['GET'])
async def ask(request):
    
    if rest_client.configuration.client_configuration.use_api_keys is True:
        if 'apikey' not in request.raw_args or request.raw_args['apikey'] is None:
            if logging.getLogger().isEnabledFor(logging.ERROR): logging.error("Unauthorised access - api required but missing")
            return json({'error': 'Unauthorized access'})

        apikey = request.raw_args['apikey']
        if is_apikey_valid(apikey) is False:
            if logging.getLogger().isEnabledFor(logging.ERROR): logging.error("'Unauthorised access - invalid api key")
            return json({'error': 'Unauthorized access'})

    if 'question' not in request.raw_args or request.raw_args['question'] is None:
        print("'question' missing from request")
        if logging.getLogger().isEnabledFor(logging.ERROR): logging.error("'question' missing from request")
        raise ServerError("'question' missing from request", status_code=500)

    question = request.raw_args['question']

    if 'sessionid' not in request.raw_args or request.raw_args['sessionid'] is None:
        print("'sessionid' missing from request")
        if logging.getLogger().isEnabledFor(logging.ERROR): logging.error("'sessionid' missing from request")
        raise ServerError("'sessionid' missing from request", status_code=500)

    sessionid = request.raw_args['sessionid']

    try:
        response = rest_client.bot.ask_question(sessionid, question)
        if response is None:
            answer = rest_client.bot.default_response
            rest_client.log_unknown_response(question)
        else:
            answer = response
            rest_client.log_response(question, response)

        response = {"question": question,
                    "answer": answer,
                    "sessionid": sessionid
                   }

        return json({'response': response})

    except Exception as excep:
        response = {"question": question,
                    "answer": rest_client.bot.default_response,
                    "sessionid": sessionid,
                    "error": str(excep)
                   }

        return json({'response': response})

if __name__ == '__main__':

    print("Loading, please wait...")
    rest_client = RestBotClient()

    def run():

        print("REST Client running on %s:%s" % (rest_client.configuration.client_configuration.host,
                                                rest_client.configuration.client_configuration.port))

        if rest_client.configuration.client_configuration.debug is True:
            print("REST Client running in debug mode")

        app.run(host=rest_client.configuration.client_configuration.host,
                port=rest_client.configuration.client_configuration.port,
                debug=rest_client.configuration.client_configuration.debug,
                workers=4)

    run()

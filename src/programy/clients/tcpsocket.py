"""
Copyright (c) 2016-17 Keith Sterling http://www.keithsterling.com

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

import socket
import json

from programy.clients.client import BotClient
from programy.config.sections.client.socket import SocketConfiguration

class SocketBotClient(BotClient):

    def __init__(self, argument_parser=None):
        BotClient.__init__(self, "Socket", argument_parser)

    def set_environment(self):
        self.bot.brain.properties.add_property("env", "Console")

    def get_client_configuration(self):
        return SocketConfiguration()

    def add_client_arguments(self, parser=None):
        return

    def parse_args(self, arguments, parsed_args):
        return

    def run(self):
        # create a socket object
        serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # get local machine name
        host = self.configuration.client_configuration.host
        port = self.configuration.client_configuration.port
        debug = self.configuration.client_configuration.debug
        queue = self.configuration.client_configuration.queue
        max_buffer = self.configuration.client_configuration.max_buffer

        if debug is True:
            print("TCP Socket server now listening on %s:%d"%(host, port))

        # bind to the port
        serversocket.bind((host, port))

        # queue up to 5 requests
        serversocket.listen(queue)

        running = True
        while running:
            clientsocket = None
            try:
                # establish a connection
                clientsocket, addr = serversocket.accept()

                json_data = clientsocket.recv(max_buffer).decode()
                if debug is True:
                    print("Received:", json_data)
                receive_payload = json.loads(json_data, encoding="utf-8")

                question = None
                if 'question' in receive_payload:
                    question = receive_payload['question']
                if question is None or question == "":
                    raise Exception("Clientid missing from payload")

                clientid= None
                if 'clientid' in receive_payload:
                    clientid = receive_payload['clientid']
                if clientid is None or clientid == "":
                    raise Exception ("Clientid missing from payload")

                answer = self.bot.ask_question(clientid, question, responselogger=self)

                return_payload = {"result": "OK", "answer": answer, "clientid": clientid}
                json_data = json.dumps(return_payload)
                if debug is True:
                    print("Sent:", json_data)

                clientsocket.send(json_data.encode('utf-8'))

            except KeyboardInterrupt:
                running = False
                if debug is True:
                    print("Cleaning up and exiting...")

            except Exception as e:
                print(e)
                if e.message is None:
                    return_payload = {"result": "ERROR", "message": "Unknown"}
                else:
                    return_payload = {"result": "ERROR", "message": e.message}
                json_data = json.dumps(return_payload)
                if debug is True:
                    print("Sent:", json_data)

                clientsocket.send(json_data.encode('utf-8'))

            finally:
                if clientsocket is not None:
                    clientsocket.close()


if __name__ == '__main__':

    def run():
        print("Loading, please wait...")
        console_app = SocketBotClient()
        console_app.run()

    run()



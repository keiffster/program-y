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
import socket
import json

from programy.clients.events.client import EventBotClient
from programy.clients.events.tcpsocket.config import SocketConfiguration
from programy.clients.render.json import JSONRenderer


class ClientConnection(object):

    def __init__(self, clientsocket, addr, max_buffer):
        self._clientsocket = clientsocket
        self._addr = addr
        self._max_buffer = max_buffer

    def receive_data(self):
        json_data = self._clientsocket.recv(self._max_buffer).decode()
        YLogger.debug(self, "Received: %s", json_data)
        return json.loads(json_data, encoding="utf-8")

    def send_response(self, userid, answer):
        return_payload = {"result": "OK", "answer": answer, "userid": userid}
        json_data = json.dumps(return_payload)

        YLogger.debug(self, "Sent %s:", json_data)

        self._clientsocket.send(json_data.encode('utf-8'))

    def send_error(self, error):
        if hasattr(error, 'message') is True:
            return_payload = {"result": "ERROR", "message": error.message}
        elif hasattr(error, 'msg') is True:
            return_payload = {"result": "ERROR", "message": error.msg}
        else:
            return_payload = {"result": "ERROR", "message": str(error)}

        json_data = json.dumps(return_payload)

        YLogger.debug(self, "Sent: %s", json_data)

        self._clientsocket.send(json_data.encode('utf-8'))

    def close(self):
        if self._clientsocket is not None:
            self._clientsocket.close()
            self._clientsocket = None


class SocketFactory(object):

    def create_socket(self, family=socket.AF_INET, type=socket.SOCK_STREAM):
        return socket.socket(family, type)


class SocketConnection(object):
    
    def __init__(self, host, port, queue, max_buffer=1024, factory=SocketFactory()):
        self._socket_connection = self._create_socket(host, port, queue, factory)
        self._max_buffer = max_buffer

    def _create_socket(self, host, port, queue, factory):
        # create a socket object
        serversocket = factory.create_socket()
        # bind to the port
        serversocket.bind((host, port))
        # queue up to 5 requests
        serversocket.listen(queue)
        return serversocket

    def accept_connection(self):
        # establish a connection
        clientsocket, addr = self._socket_connection.accept()
        return ClientConnection(clientsocket, addr, self._max_buffer )


class SocketBotClient(EventBotClient):

    def __init__(self, argument_parser=None):
        EventBotClient.__init__(self, "Socket", argument_parser)

        print("TCP Socket Client server now listening on %s:%d"%(self._host, self._port))
        self._server_socket = self.create_socket_connection(self._host, self._port, self._queue, self._max_buffer)

        self._renderer = JSONRenderer(self)

    def get_client_configuration(self):
        return SocketConfiguration()

    def parse_configuration(self):
        self._host = self.configuration.client_configuration.host
        self._port = self.configuration.client_configuration.port
        self._queue = self.configuration.client_configuration.queue
        self._max_buffer = self.configuration.client_configuration.max_buffer

    def extract_question(self, receive_payload):
        question = None
        if 'question' in receive_payload:
            question = receive_payload['question']
        if question is None or question == "":
            raise Exception("Clientid missing from payload")
        return question

    def extract_userid(self, receive_payload):
        userid = None
        if 'userid' in receive_payload:
            userid = receive_payload['userid']
        if userid is None or userid == "":
            raise Exception("Clientid missing from payload")
        return userid

    def create_socket_connection(self, host, port, queue, max_buffer):
        return SocketConnection(host, port, queue, max_buffer)

    def process_question(self, client_context, question):
        self._questions += 1
        return client_context.bot.ask_question(client_context , question, responselogger=self)

    def render_response(self, client_context, response):
        # Calls the renderer which handles RCS context, and then calls back to the client to show response
        self._renderer.render(client_context, response)

    def process_response(self, client_context, response):
        self._client_connection.send_response(client_context.userid, response)

    def wait_and_answer(self):
        running = True
        try:
            self._client_connection = self._server_socket.accept_connection()

            receive_payload = self._client_connection.receive_data()

            question = self.extract_question(receive_payload)
            userid = self.extract_userid(receive_payload)

            client_context = self.create_client_context(userid)
            answer = self.process_question(client_context, question)

            self.render_response(client_context, answer)

        except KeyboardInterrupt:
            running = False
            YLogger.debug(self, "Cleaning up and exiting...")

        except Exception as e:
            if self._client_connection is not None:
                self._client_connection.send_error(e)

        finally:
            if self._client_connection is not None:
                self._client_connection.close()

        return running


if __name__ == '__main__':

    print("Initiating TCP Socket Client...")

    def run():
        tcpsocket_app = SocketBotClient()
        tcpsocket_app.run()

    run()



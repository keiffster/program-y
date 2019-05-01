import unittest
import socket

from programy.clients.events.tcpsocket.client import SocketConnection
from programy.clients.events.tcpsocket.client import SocketBotClient
from programy.clients.events.tcpsocket.config import SocketConfiguration

from programytest.clients.arguments import MockArgumentParser


class MockSocket(object):

    def __init__(self):
        self._recv = ""
        self._send = None

    def bind(self, host_port):
        pass

    def listen(self, queue):
        pass

    def accept(self):
        return self, "127.0.0.1"

    def recv(self, max_buffer):
        return bytes(self._recv, "utf-8")

    def send(self, data):
        self._send = data.decode()

    def close(self):
        pass


class MockSocketFactory(object):

    def __init__(self, socket=None):
        if socket is not None:
            self._socket = socket
        else:
            self._socket = MockSocket()

    def create_socket(self, family=socket.AF_INET, type=socket.SOCK_STREAM):
        return self._socket


class MockSocketBotClient(SocketBotClient):

    def __init__(self, socket, argument_parser=None):
        self._socket = socket
        SocketBotClient.__init__(self, argument_parser)
        self.response = ""

    def create_socket_connection(self, host, port, queue, max_buffer):
        return SocketConnection(host, port, queue, max_buffer, factory=MockSocketFactory(self._socket))

    def process_question(self, client_context, question):
        return self.response


class SocketBotClientTests(unittest.TestCase):

    def test_init(self):
        arguments = MockArgumentParser()
        client = MockSocketBotClient( MockSocket(), arguments)
        self.assertIsNotNone(client)
        self.assertEqual('ProgramY AIML2.0 Client', client.get_description())
        self.assertIsInstance(client.get_client_configuration(), SocketConfiguration)

    def test_extract_payload(self):
        arguments = MockArgumentParser()
        client = MockSocketBotClient(MockSocket(), arguments)

        receive_payload = {"userid": "user12345",
                           "question": "Test Question"}

        question = client.extract_question(receive_payload)
        self.assertEqual("Test Question", question)

        userid = client.extract_userid(receive_payload)
        self.assertEqual("user12345", userid)

    def test_wait_and_answer(self):
        arguments = MockArgumentParser()
        mock_socket = MockSocket()
        mock_socket._recv =  '{"userid": "user1234", "question": "Test Question"}'
        client = MockSocketBotClient(mock_socket, arguments)
        client.response = "Hello"
        client.wait_and_answer()
        self.assertEqual('{"result": "OK", "answer": {"type": "text", "text": "Hello"}, "userid": "user1234"}', mock_socket._send)

    def test_wait_and_answer_no_response(self):
        arguments = MockArgumentParser()
        mock_socket = MockSocket()
        mock_socket._recv =  ''
        client = MockSocketBotClient(mock_socket, arguments)
        client.response = ""
        client.wait_and_answer()
        self.assertEqual('{"result": "ERROR", "message": "Expecting value"}', mock_socket._send)

    def test_wait_and_answer_invalid_response(self):
        arguments = MockArgumentParser()
        mock_socket = MockSocket()
        mock_socket._recv =  'This is rubbish'
        client = MockSocketBotClient(mock_socket, arguments)
        client.wait_and_answer()
        self.assertEqual('{"result": "ERROR", "message": "Expecting value"}', mock_socket._send)

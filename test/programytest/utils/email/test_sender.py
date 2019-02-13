import unittest

from programy.utils.email.sender import EmailSender
from programy.utils.email.config import EmailConfiguration


class MockSMTPServer(object):

    def __init__(self, host, port):
        self._ehlo = False
        self._starttls = False
        self._login = False
        self._send_message = False
        self._quit = False

    def ehlo(self):
        self._ehlo = True

    def starttls(self):
        self._starttls = True

    def login(self, username, password):
        self._login = True

    def send_message(self, msg):
        self._send_message = True

    def quit(self):
        self._quit = True


class TestEmailSender(EmailSender):

    def __init__(self, config: EmailConfiguration):
        EmailSender.__init__(self, config)

    def _smtp_server(self, host, port):
        return MockSMTPServer(host, port)


class EmailSenderTests(unittest.TestCase):
    
    def test_send(self):

        config = EmailConfiguration()
        
        sender = EmailSender(config)
        
        sender.send("fred@west.com", "New patio", "Do you need any help with the slabs?")
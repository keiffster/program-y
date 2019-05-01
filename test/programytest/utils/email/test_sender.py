import unittest
import os

from programy.utils.email.sender import EmailSender
from programy.utils.email.config import EmailConfiguration


class MockSMTPServer(object):

    def __init__(self, host, port):
        self.did_ehlo = False
        self.did_starttls = False
        self.did_login = False
        self.did_send_message = False
        self.did_quit = False

    def ehlo(self):
        self.did_ehlo = True

    def starttls(self):
        self.did_starttls = True

    def login(self, username, password):
        self.did_login = True

    def send_message(self, msg):
        self.did_send_message = True

    def quit(self):
        self.did_quit = True


class MockEmailSender(EmailSender):

    def __init__(self, config: EmailConfiguration, mock_sender):
        EmailSender.__init__(self, config)
        self.mock_sender = mock_sender

    def _smtp_server(self, host, port):
        return self.mock_sender


class EmailSenderTests(unittest.TestCase):
    
    def test_send_message(self):

        config = EmailConfiguration()
        
        sender = MockEmailSender(config, mock_sender=MockSMTPServer("127.0.0.1", 80))
        
        sender.send("fred@west.com", "New patio", "Do you need any help with the slabs?")

        self.assertTrue(sender.mock_sender.did_ehlo)
        self.assertTrue(sender.mock_sender.did_starttls)
        self.assertTrue(sender.mock_sender.did_login)
        self.assertTrue(sender.mock_sender.did_quit)

    def test_send_message_multiple_recipients(self):
        config = EmailConfiguration()

        sender = MockEmailSender(config, mock_sender=MockSMTPServer("127.0.0.1", 80))

        sender.send(["fred@west.com", "mary@west.com"], "New patio", "Do you need any help with the slabs?")

        self.assertTrue(sender.mock_sender.did_ehlo)
        self.assertTrue(sender.mock_sender.did_starttls)
        self.assertTrue(sender.mock_sender.did_login)
        self.assertTrue(sender.mock_sender.did_quit)

    def test_send_message_with_text_file_attachment(self):
        config = EmailConfiguration()

        sender = MockEmailSender(config, mock_sender=MockSMTPServer("127.0.0.1", 80))

        attachment = os.path.dirname(__file__) + os.sep + "test.txt"

        sender.send("fred@west.com", "New patio", "Do you need any help with the slabs?", [attachment])

        self.assertTrue(sender.mock_sender.did_ehlo)
        self.assertTrue(sender.mock_sender.did_starttls)
        self.assertTrue(sender.mock_sender.did_login)
        self.assertTrue(sender.mock_sender.did_quit)

    #def test_send_message_with_text_image_attachment(self):
    #def test_send_message_with_text_audio_attachment(self):
    #def test_send_message_with_unknown_file_attachment(self):

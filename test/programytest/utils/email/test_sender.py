import os
import unittest
from email.mime.multipart import MIMEMultipart
from programy.utils.email.config import EmailConfiguration
from programy.utils.email.sender import EmailSender


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


class MockResult:

    def __init__(self, items):
        self._items = items

    def items(self):
        return self._items.items()


class MockEmailSender(EmailSender):

    def __init__(self, config: EmailConfiguration, mock_sender, result=None, ctype=None, attachment_encoding=None):
        EmailSender.__init__(self, config)
        self.mock_sender = mock_sender
        self._result = result
        self._ctype = ctype
        self._attachment_encoding = attachment_encoding

    def _smtp_server(self, host, port):
        return self.mock_sender

    def _guess_mime_type(self, path):
        if self._ctype is None and self._attachment_encoding is None:
            return super(MockEmailSender, self)._guess_mime_type(path)

        return self._ctype, self._attachment_encoding

    def _send_message(self, host, port, username, password, msg):
        if self._result is not None:
            return self._result
        return super(MockEmailSender, self)._send_message(host, port, username, password, msg)


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

    def test_send_message_with_image_attachment(self):
        config = EmailConfiguration()

        sender = MockEmailSender(config, mock_sender=MockSMTPServer("127.0.0.1", 80))

        attachment = os.path.dirname(__file__) + os.sep + "robbie.png"

        sender.send("fred@west.com", "New patio", "Do you need any help with the slabs?", [attachment])

        self.assertTrue(sender.mock_sender.did_ehlo)
        self.assertTrue(sender.mock_sender.did_starttls)
        self.assertTrue(sender.mock_sender.did_login)
        self.assertTrue(sender.mock_sender.did_quit)

    def test_send_message_with_audio_attachment(self):
        config = EmailConfiguration()

        sender = MockEmailSender(config, mock_sender=MockSMTPServer("127.0.0.1", 80))

        attachment = os.path.dirname(__file__) + os.sep + "audio.mp3"

        sender.send("fred@west.com", "New patio", "Do you need any help with the slabs?", [attachment])

        self.assertTrue(sender.mock_sender.did_ehlo)
        self.assertTrue(sender.mock_sender.did_starttls)
        self.assertTrue(sender.mock_sender.did_login)
        self.assertTrue(sender.mock_sender.did_quit)

    def test_send_message_with_application_file_attachment(self):
        config = EmailConfiguration()

        sender = MockEmailSender(config, mock_sender=MockSMTPServer("127.0.0.1", 80))

        attachment = os.path.dirname(__file__) + os.sep + "something.pdf"

        sender.send("fred@west.com", "New patio", "Do you need any help with the slabs?", [attachment])

        self.assertTrue(sender.mock_sender.did_ehlo)
        self.assertTrue(sender.mock_sender.did_starttls)
        self.assertTrue(sender.mock_sender.did_login)
        self.assertTrue(sender.mock_sender.did_quit)

    def test_send_message_with_unknown_file_attachment(self):
        config = EmailConfiguration()

        sender = MockEmailSender(config, mock_sender=MockSMTPServer("127.0.0.1", 80))

        attachment = os.path.dirname(__file__) + os.sep + "unknown.???"

        sender.send("fred@west.com", "New patio", "Do you need any help with the slabs?", [attachment])

        self.assertFalse(sender.mock_sender.did_ehlo)

    def test_send_message_with_known_attachment(self):
        config = EmailConfiguration()

        sender = MockEmailSender(config, mock_sender=MockSMTPServer("127.0.0.1", 80))

        attachment = os.path.dirname(__file__) + os.sep + "audio.mp3"

        sender.send("fred@west.com", "New patio", "Do you need any help with the slabs?", [(attachment, None, attachment)])

        self.assertTrue(sender.mock_sender.did_ehlo)
        self.assertTrue(sender.mock_sender.did_starttls)
        self.assertTrue(sender.mock_sender.did_login)
        self.assertTrue(sender.mock_sender.did_quit)

    def test_get_ctype_and_attachment(self):
        config = EmailConfiguration()

        sender = MockEmailSender(config, mock_sender=MockSMTPServer("127.0.0.1", 80))

        attachment = os.path.dirname(__file__) + os.sep + "test.txt"

        sender._get_ctype_and_attachment(attachment, "utf-8")

    def test_get_ctype_and_attachment_ctype_none(self):
        config = EmailConfiguration()

        sender = MockEmailSender(config, mock_sender=MockSMTPServer("127.0.0.1", 80), ctype=None, attachment_encoding=None)

        attachment = os.path.dirname(__file__) + os.sep + "test.txt"

        ctype, attachment_encoding = sender._get_ctype_and_attachment(attachment, "ascii")

        self.assertEquals("text/plain", ctype)
        self.assertEquals("ascii", attachment_encoding)

    def test_get_ctype_and_attachment_both_none(self):
        config = EmailConfiguration()

        sender = MockEmailSender(config, mock_sender=MockSMTPServer("127.0.0.1", 80), ctype=None, attachment_encoding=None)

        attachment = os.path.dirname(__file__) + os.sep + "test.txt"

        ctype, attachment_encoding = sender._get_ctype_and_attachment(attachment, None)

        self.assertEquals("text/plain", ctype)
        self.assertEquals("utf-8", attachment_encoding)

    def test_get_ctype_and_attachment_attachment_not_nonw(self):
        config = EmailConfiguration()

        sender = MockEmailSender(config, mock_sender=MockSMTPServer("127.0.0.1", 80), ctype=None, attachment_encoding="utf-8")

        attachment = os.path.dirname(__file__) + os.sep + "test.txt"

        ctype, attachment_encoding = sender._get_ctype_and_attachment(attachment, None)

        self.assertEquals("application/octet-stream", ctype)
        self.assertEquals("utf-8", attachment_encoding)

    def test_add_attachement_no_ctype_no_encoding(self):
        config = EmailConfiguration()

        sender = MockEmailSender(config, mock_sender=MockSMTPServer("127.0.0.1", 80))

        msg = MIMEMultipart()

        attachment = os.path.dirname(__file__) + os.sep + "test.txt"

        sender._add_attachement(msg, attachment, ctype=None, encoding=None)

        self.assertEquals([('Content-Type', 'multipart/mixed'), ('MIME-Version', '1.0')], msg.items())
        self.assertEquals(1, len(msg.get_payload()))

    def test_add_attachement_no_ctype_no_encoding_compressed(self):
        config = EmailConfiguration()

        sender = MockEmailSender(config, mock_sender=MockSMTPServer("127.0.0.1", 80))

        msg = MIMEMultipart()

        attachment = os.path.dirname(__file__) + os.sep + "something.zip"

        sender._add_attachement(msg, attachment, ctype=None, encoding=None)

        self.assertEquals([('Content-Type', 'multipart/mixed'), ('MIME-Version', '1.0')], msg.items())
        self.assertEquals(1, len(msg.get_payload()))

    def test_add_attachement_no_ctype_encoding_compressed(self):
        config = EmailConfiguration()

        sender = MockEmailSender(config, mock_sender=MockSMTPServer("127.0.0.1", 80))

        msg = MIMEMultipart()

        attachment = os.path.dirname(__file__) + os.sep + "something.zip"

        sender._add_attachement(msg, attachment, ctype=None, encoding="utf-8")

        self.assertEquals([('Content-Type', 'multipart/mixed'), ('MIME-Version', '1.0')], msg.items())
        self.assertEquals(1, len(msg.get_payload()))

    def test_add_attachement_ctype_no_encoding(self):
        config = EmailConfiguration()

        sender = MockEmailSender(config, mock_sender=MockSMTPServer("127.0.0.1", 80))

        msg = MIMEMultipart()

        attachment = os.path.dirname(__file__) + os.sep + "test.txt"

        sender._add_attachement(msg, attachment, ctype='text/plain', encoding=None)

        self.assertEquals([('Content-Type', 'multipart/mixed'), ('MIME-Version', '1.0')], msg.items())
        self.assertEquals(1, len(msg.get_payload()))

    def test_add_attachement_ctype_ecoding(self):
        config = EmailConfiguration()

        sender = MockEmailSender(config, mock_sender=MockSMTPServer("127.0.0.1", 80))

        msg = MIMEMultipart()

        attachment = os.path.dirname(__file__) + os.sep + "test.txt"

        sender._add_attachement(msg, attachment, ctype='text/plain', encoding="utf-8")

        self.assertEquals([('Content-Type', 'multipart/mixed'), ('MIME-Version', '1.0')], msg.items())
        self.assertEquals(1, len(msg.get_payload()))

    def test_send_message_none_result(self):
        config = EmailConfiguration()

        sender = MockEmailSender(config, mock_sender=MockSMTPServer("127.0.0.1", 80), result=MockResult(None))

        sender.send("fred@west.com", "New patio", "Do you need any help with the slabs?")

    def test_send_message_empty_result(self):
        config = EmailConfiguration()

        sender = MockEmailSender(config, mock_sender=MockSMTPServer("127.0.0.1", 80), result=MockResult([]))

        sender.send("fred@west.com", "New patio", "Do you need any help with the slabs?")

    def test_send_message_single_result(self):
        config = EmailConfiguration()

        sender = MockEmailSender(config, mock_sender=MockSMTPServer("127.0.0.1", 80), result=MockResult({1: "Failed"}))

        sender.send("fred@west.com", "New patio", "Do you need any help with the slabs?")

    def test_send_message_multi_result(self):
        config = EmailConfiguration()

        sender = MockEmailSender(config, mock_sender=MockSMTPServer("127.0.0.1", 80), result=MockResult({1: "Failed", 2: "Bad"}))

        sender.send("fred@west.com", "New patio", "Do you need any help with the slabs?")

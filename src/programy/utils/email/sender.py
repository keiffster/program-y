import smtplib

import mimetypes

from email import encoders
from email.mime.audio import MIMEAudio
from email.mime.base import MIMEBase
from email.mime.image import MIMEImage
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


class Configuration(object):

    def __init__(self):
        self._host      = None
        self._port      = None
        self._username  = None
        self._password  = None
        self._from_addr  = None


class Email(object):

    def __init__(self, config):
        self._host      = config._host
        self._port      = config._port
        self._username  = config._username
        self._password  = config._password
        self._from_addr = config._from_addr
        if config._from_addr is None:
            self._from_addr = self._username

        self._to = []
        self._subject = None
        self._message = None
        self._attachments = []

    def add_to(self, address):
        self._to.append(address)

    def set_message(self, text):
        self._message = text

    def add_mine_attachments(self, msg, attachments):
        for attachment in attachments:
            self.add_attachement(msg, attachment)

    def add_attachement(self, msg, path, ctype=None, encoding=None):

        if ctype is None:
            ctype, encoding = mimetypes.guess_type(path)
            if  ctype is None:
                # No guess could be made, or the file is encoded (compressed), so
                # use a generic bag-of-bits type.
                ctype = 'application/octet-stream'

        maintype, subtype = ctype.split('/', 1)

        if maintype == 'text':
            with open(path) as fp:
                # Note: we should handle calculating the charset
                attach = MIMEText(fp.read(), _subtype=subtype)
        elif maintype == 'image':
            with open(path, 'rb') as fp:
                attach = MIMEImage(fp.read(), _subtype=subtype)
        elif maintype == 'audio':
            with open(path, 'rb') as fp:
                attach = MIMEAudio(fp.read(), _subtype=subtype)
        else:
            with open(path, 'rb') as fp:
                attach = MIMEBase(maintype, subtype)
                attach.set_payload(fp.read())
            # Encode the payload using Base64
            encoders.encode_base64(attach)

        msg.attach(attach)

    def send(self, to, subject, message, attachments=[]):

        if attachments:
            msg = MIMEMultipart()
            msg.attach(MIMEText(message))
            self.add_mime_attachements(msg, attachments)
        else:
            msg = MIMEText(message)

        msg['Subject'] = subject
        msg['From'] = self._from_addr
        msg['To'] = to


        print("Starting")
        server=smtplib.SMTP(self._host, config._port)
        server.ehlo()
        print("TLS")
        server.starttls()
        print("Logging in")
        server.login(config._username, config._password)
        print("Sending")
        server.send_message(msg)
        print("Quiting")
        server.quit()


if __name__ == '__main__':

    config = Configuration()
    config._host = 'smtp.gmail.com'
    config._port = 587
    config._username = "email-address"
    config._password = "password"

    email = Email(config)
    email.send("keiffster@gmail.com", "ServusAI is great", "Did you know Servus AI is amazing!")



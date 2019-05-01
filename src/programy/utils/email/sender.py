from programy.utils.logging.ylogger import YLogger

import smtplib
import mimetypes

from email import encoders
from email.mime.audio import MIMEAudio
from email.mime.base import MIMEBase
from email.mime.image import MIMEImage
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

from programy.utils.email.config import EmailConfiguration


class EmailSender(object):

    def __init__(self, config: EmailConfiguration):
        self._config = config
        self._attachments = []

    def _add_mine_attachments(self, msg, attachments):
        for attachment in attachments:
            self._add_attachement(msg, attachment)

    def _add_attachement(self, msg, path, ctype=None, encoding=None):

        if ctype is None:
            ctype, attachment_encoding = mimetypes.guess_type(path)
            if ctype is None:
                # No guess could be made, or the file is encoded (compressed), so
                # use a generic bag-of-bits type.
                ctype = 'application/octet-stream'

            if attachment_encoding is None:
                if encoding is not None:
                    attachment_encoding = encoding

                else:
                    attachment_encoding = "utf-8"

        maintype, subtype = ctype.split('/', 1)

        if maintype == 'text':
            with open(path, encoding=attachment_encoding) as fp:
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

            encoders.encode_base64(attach)

        msg.attach(attach)

    def _smtp_server(self, host, port):
        return smtplib.SMTP(host, port)

    def _send_message(self, host, port, username, password, msg, attachments=[]):

        if attachments:
            self._add_mine_attachments(msg, attachments)

        YLogger.info(self, "Email sender starting")
        server = self._smtp_server(host, port)
        server.ehlo()
        server.starttls()
        YLogger.info(self, "Email sender logging in")
        server.login(username, password)
        YLogger.info(self, "Email sender sending")
        result = server.send_message(msg)
        YLogger.info(self, "Email sender quiting")
        server.quit()
        return result

    def send(self, to, subject, message, attachments=[]):

        try:
            if attachments:
                YLogger.info(self, "Email sender adding mime attachment")
                msg = MIMEMultipart()
                msg.attach(MIMEText(message))
                self._add_mine_attachments(msg, attachments)
            else:
                msg = MIMEText(message)

            msg['Subject'] = subject
            msg['From'] = self._config._from_addr
            msg['To'] = to

            result = self._send_message(self._config.host, self._config.port, self._config.username, self._config.password, msg, attachments)
            for email, error in result.items():
                YLogger.error(None, "Email send failed [%s] = [%d] - [%s]"%(email, error[0], error[1]))

        except Exception as e:
            YLogger.exception(self, "Email sender failed", e)





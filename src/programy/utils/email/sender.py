import smtplib
import mimetypes
from email import encoders
from email.mime.audio import MIMEAudio
from email.mime.base import MIMEBase
from email.mime.image import MIMEImage
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from programy.utils.logging.ylogger import YLogger
from programy.utils.email.config import EmailConfiguration


class EmailSender:

    def __init__(self, config: EmailConfiguration):
        self._config = config
        self._attachments = []

    def _add_mine_attachments(self, msg, attachments):
        for attachment in attachments:
            if isinstance(attachment, tuple):
                self._add_attachement(msg, attachment[0], attachment[1], attachment[2])
            else:
                self._add_attachement(msg, attachment)

    def _guess_mime_type(self, path):
        return mimetypes.guess_type(path)

    def _split_ctype(self, ctype):
        return ctype.split('/', 1)

    def _get_ctype_and_attachment(self, path, encoding):

        ctype, attachment_encoding = self._guess_mime_type(path)

        if ctype is None:
            # No guess could be made, or the file is encoded (compressed), so
            # use a generic bag-of-bits type.
            ctype = 'application/octet-stream'

        if attachment_encoding is None:
            if encoding is not None:
                attachment_encoding = encoding

            else:
                # No guess could be made, so we default to utf-8
                attachment_encoding = "utf-8"

        return ctype, attachment_encoding

    def _attach_text(self, msg, path, encoding, subtype):
        with open(path, encoding=encoding) as fp:
            # Note: we should handle calculating the charset
            attach = MIMEText(fp.read(), _subtype=subtype)
            msg.attach(attach)

    def _attach_image(self, msg, path, subtype):
        with open(path, 'rb') as fp:
            attach = MIMEImage(fp.read(), _subtype=subtype)
            msg.attach(attach)

    def _attach_audio(self, msg, path, subtype):
        with open(path, 'rb') as fp:
            attach = MIMEAudio(fp.read(), _subtype=subtype)
            msg.attach(attach)

    def _attach_binary(self, msg, path, mimetype, subtype):
        # No specific mime type, so we shoot for a binary file
        with open(path, 'rb') as fp:
            attach = MIMEBase(mimetype, subtype)
            attach.set_payload(fp.read())
            encoders.encode_base64(attach)
            msg.attach(attach)

    def _add_attachement(self, msg, path, ctype=None, encoding=None):

        if ctype is None:
            ctype, encoding = self._get_ctype_and_attachment(path, encoding)

        if encoding is None:
            encoding = "utf-8"

        mimetype, subtype = self._split_ctype(ctype)

        if mimetype == 'text':
            self._attach_text(msg, path, encoding, subtype)

        elif mimetype == 'image':
            self._attach_image(msg, path, subtype)

        elif mimetype == 'audio':
            self._attach_audio(msg, path, subtype)

        else:
            self._attach_binary(msg, path, mimetype, subtype)

    def _smtp_server(self, host, port):
        return smtplib.SMTP(host, port)     # pragma: no cover

    def _send_message(self, host, port, username, password, msg):

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

    def send(self, to, subject, message, attachments=None):

        try:
            if attachments:
                YLogger.info(self, "Email sender adding mime attachment")
                msg = MIMEMultipart()
                msg.attach(MIMEText(message))
                self._add_mine_attachments(msg, attachments)
            else:
                msg = MIMEText(message)

            msg['Subject'] = subject
            msg['From'] = self._config.from_addr
            msg['To'] = to

            result = self._send_message(self._config.host,
                                        self._config.port,
                                        self._config.username,
                                        self._config.password,
                                        msg)

            if result:
                for email, error in result.items():
                    YLogger.error(None, "Email send failed: [%d] - [%s]", email, error)

        except Exception as e:
            YLogger.exception(self, "Email sender failed", e)

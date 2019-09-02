import unittest

from programy.extensions.admin.transcript import TranscriptAdminExtension
from programy.dialog.sentence import Sentence
from programy.dialog.question import Question

from programytest.client import TestClient


class TranscriptAdminExtensionClient(TestClient):

    def __init__(self):
        TestClient.__init__(self)

    def load_configuration(self, arguments):
        super(TranscriptAdminExtensionClient, self).load_configuration(arguments)


class TranscriptAdminExtensionTests(unittest.TestCase):

    def test_transcripts_no_questions_without_props(self):
        client = TranscriptAdminExtensionClient()
        client_context = client.create_client_context("testid")

        client_context.bot.get_conversation(client_context)

        extension = TranscriptAdminExtension()
        self.assertIsNotNone(extension)

        result = extension.execute(client_context, "")
        self.assertIsNotNone(result)
        self.assertEqual("Questions:<br /><ul></ul><br />", result)

    def test_transcripts_questions_without_props(self):
        client = TranscriptAdminExtensionClient()
        client_context = client.create_client_context("testid")

        question = Question.create_from_sentence(Sentence(client_context, "Hello World"))
        conversation = client_context.bot.get_conversation(client_context)
        conversation.record_dialog(question)

        extension = TranscriptAdminExtension()
        self.assertIsNotNone(extension)

        result = extension.execute(client_context, "")
        self.assertIsNotNone(result)
        self.assertEqual("Questions:<br /><ul><li>Hello World - </li></ul><br />", result)

    def test_transcripts_questions_with_props(self):
        client = TranscriptAdminExtensionClient()
        client_context = client.create_client_context("testid")

        question = Question.create_from_sentence(Sentence(client_context, "Hello World"))
        conversation = client_context.bot.get_conversation(client_context)
        conversation.record_dialog(question)

        extension = TranscriptAdminExtension()
        self.assertIsNotNone(extension)

        result = extension.execute(client_context, "PROPERTIES")
        self.assertIsNotNone(result)
        self.assertEqual("Questions:<br /><ul><li>Hello World - </li></ul><br />Properties:<br /><ul><li>topic = *</li></ul><br />", result)

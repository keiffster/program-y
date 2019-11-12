import os
import unittest
from programy.utils.files.filewriter import ConversationFileWriter
from programy.utils.files.filewriter import FileWriterConfiguration
from programytest.utils.files.utils import get_os_specific_path


class ConversationFileWriterTests(unittest.TestCase):

    def test_init(self):
        filename = get_os_specific_path() + os.sep + "conversation.txt"
        config = FileWriterConfiguration(filename=filename, fileformat="txt", mode="a", encoding="utf-8",
                                         delete_on_start=False)

        writer = ConversationFileWriter(config)
        self.assertIsNotNone(writer)

        writer.log_question_and_answer("client1", "question", "answer")
        self.assertTrue(os.path.exists(filename))

        if os.path.exists(filename):
            os.remove(filename)
            self.assertFalse(os.path.exists(filename))

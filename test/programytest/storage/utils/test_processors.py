import unittest
import os
from programy.storage.utils.processors import TextFile
from programy.storage.utils.processors import CSVFileReader
from programy.storage.utils.processors import CSVFileWriter


def get_temp_dir():
    if os.name == 'posix':                                              # pragma: no cover
        return '/tmp'                                                   # pragma: no cover
    elif os.name == 'nt':                                               # pragma: no cover
        import tempfile                                                 # pragma: no cover
        return tempfile.gettempdir()                                    # pragma: no cover
    else:                                                               # pragma: no cover
        raise Exception("Unknown operating system [%s]" % os.name)      # pragma: no cover


class MockTextFileWriter:

    def format_row_as_text(self, elements):
        return ", ".join(elements)


class TextFileTests(unittest.TestCase):

    def test_text_file_processors(self):

        filename = get_temp_dir() + os.sep + "mytemp.txt"
        if os.path.exists(filename):
            os.remove(filename)

        self.assertFalse(os.path.exists(filename))

        processor = TextFile(filename, mode="w")
        processor.write_line(["1", "2"], MockTextFileWriter())
        processor.flush()
        processor.close()

        self.assertTrue(os.path.exists(filename))
        os.remove(filename)


class MockCSVProcessor:

    def __init__(self, result):
        self.contents = None
        self.result = result

    def process_line(self, name, line):
        self.contents = line
        return self.result


class CSVFileReaderWriterTests(unittest.TestCase):

    def test_csv_file_writer_reader_success(self):

        filename = get_temp_dir() + os.sep + "mytemp.csv"
        if os.path.exists(filename):
            os.remove(filename)

        self.assertFalse(os.path.exists(filename))

        writer = CSVFileWriter(filename)
        writer.write_line(["A", "B", "C"])
        writer.flush()
        writer.close()

        reader = CSVFileReader(filename)
        processor = MockCSVProcessor(True)
        count, success = reader.process_lines("TEST", processor)
        self.assertEquals(count, 1)
        self.assertEquals(success, 1)
        reader.close()

        self.assertTrue(os.path.exists(filename))
        os.remove(filename)

    def test_csv_file_writer_reader_fail(self):

        filename = get_temp_dir() + os.sep + "mytemp.csv"
        if os.path.exists(filename):
            os.remove(filename)

        self.assertFalse(os.path.exists(filename))

        writer = CSVFileWriter(filename)
        writer.write_line(["A", "B", "C"])
        writer.flush()
        writer.close()

        reader = CSVFileReader(filename)
        processor = MockCSVProcessor(False)
        count, success = reader.process_lines("TEST", processor)
        self.assertEquals(count, 1)
        self.assertEquals(success, 0)
        reader.close()

        self.assertTrue(os.path.exists(filename))
        os.remove(filename)

import unittest

from programy.nlp.pos import PartsOfSpeechTagger


class NGramsCreatorTests(unittest.TestCase):

    def test_tag_string(self):

        tags = PartsOfSpeechTagger.tag_string("Python is a high-level, general-purpose programming language.")
        self.assertIsNotNone(tags)
        self.assertEqual([('Python', 'NNP'),
                           ('is', 'VBZ'),
                           ('a', 'DT'),
                           ('high-level', 'JJ'),
                           ('general-purpose', 'JJ'),
                           ('programming', 'NN'),
                           ('language', 'NN')],
                          tags)

    def test_type_to_string(self):

        self.assertEqual("Proper noun, singular", PartsOfSpeechTagger.tag_to_string("NNP"))
        self.assertEqual("Unknown", PartsOfSpeechTagger.tag_to_string(""))
        self.assertEqual("Unknown", PartsOfSpeechTagger.tag_to_string("Rubbish"))
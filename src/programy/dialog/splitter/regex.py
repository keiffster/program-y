import re

from programy.dialog.splitter.splitter import SentenceSplitter

class RegexSentenceSplitter(SentenceSplitter):

    def __init__(self, config):
        SentenceSplitter.__init__(self, config)

    def split(self, text):
        sentences = re.split('[:;,.?!]', text)
        return [self.remove_punctuation(s).strip() for s in sentences]



import re

from programy.dialog.splitter.splitter import SentenceSplitter

class SpacySentenceSplitter(SentenceSplitter):

    def __init__(self, config):
        SentenceSplitter.__init__(self, config)

    def split(self, text):
        raise NotImplementedError()

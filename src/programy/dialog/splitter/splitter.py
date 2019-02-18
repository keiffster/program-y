"""
Copyright (c) 2016-2019 Keith Sterling http://www.keithsterling.com

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated
documentation files (the "Software"), to deal in the Software without restriction, including without limitation
the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software,
and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the
Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO
THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT,
TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
"""
from programy.utils.logging.ylogger import YLogger

import re

from programy.utils.classes.loader import ClassLoader
from programy.config.bot.splitter import BotSentenceSplitterConfiguration
from programy.activate import Activatable

class SentenceSplitter(Activatable):

    ALL_PUNCTUATION = re.compile(r'[:\'";,.?!\(\)\-"]')

    def __init__(self, splitter_config):
        Activatable.__init__(self)

        assert (splitter_config is not None)
        assert (isinstance(splitter_config, BotSentenceSplitterConfiguration))

        self._configuration = splitter_config

    def split(self, text):
        raise NotImplementedError()

    def remove_punctuation(self, text):
        return SentenceSplitter.ALL_PUNCTUATION.sub('', text)

    @staticmethod
    def initiate_sentence_splitter(splitter_config):
        if splitter_config.classname is not None:
            try:
                YLogger.info(None, "Loading sentence splitter from class [%s]", splitter_config.classname)
                splitter_class = ClassLoader.instantiate_class(splitter_config.classname)
                sentence_splitter = splitter_class(splitter_config)
                return sentence_splitter
            except Exception as excep:
                YLogger.exception(None, "Failed to initiate sentence splitter", excep)
        else:
            YLogger.warning(None, "No configuration setting for sentence splitter!")

        return None

from programy.utils.logging.ylogger import YLogger

import re

from programy.utils.classes.loader import ClassLoader
from programy.config.bot.splitter import BotSentenceSplitterConfiguration


class SentenceSplitter(object):

    ALL_PUNCTUATION = re.compile('[:\'";,.?!\(\)\-"]')

    def __init__(self, splitter_config):

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

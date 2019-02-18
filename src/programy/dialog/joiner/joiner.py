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

from programy.config.bot.joiner import BotSentenceJoinerConfiguration
from programy.utils.classes.loader import ClassLoader

class SentenceJoiner(object):
    
    def __init__(self, joiner_config):

        assert (joiner_config is not None)
        assert (isinstance(joiner_config, BotSentenceJoinerConfiguration))

        self._configuration = joiner_config

    def combine_answers(self, answers, srai):
        final_sentences = []
        for sentence in answers:
            if sentence:

                # Capitalise the start of each sentence
                if sentence[0].isalpha():
                    sentence = sentence[0].upper() + sentence[1:]

                # If it ends with a terminator, keep the terminator, otherwise add a full stop
                if self.ends_with_terminator(sentence):
                    final_sentences.append(sentence)
                else:
                    if srai is False:
                        final_sentences.append(sentence+self._configuration.terminator)
                    else:
                        final_sentences.append(sentence)

        return " ".join([sentence for sentence in final_sentences])

    def ends_with_terminator(self, sentence):
        for ch in self._configuration.join_chars:
            if sentence.endswith(ch):
                return True
        return False

    @staticmethod
    def initiate_sentence_joiner(joiner_config):
        if joiner_config.classname is not None:
            try:
                YLogger.info(None, "Loading sentence joiner from class [%s]", joiner_config.classname)
                joiner_class = ClassLoader.instantiate_class(joiner_config.classname)
                sentence_joiner = joiner_class(joiner_config)
                return sentence_joiner
            except Exception as excep:
                YLogger.exception(None, "Failed to initiate sentence joiner", excep)
        else:
            YLogger.warning(None, "No configuration setting for sentence joiner!")

        return None

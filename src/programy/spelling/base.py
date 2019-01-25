"""
Copyright (c) 2016-2019 Keith Sterling http://www.keithsterling.com

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated
documentation files (the "Software"), to deal in the Software without restriction, including without limitation
the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software,
and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions
of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO
THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT,
TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
"""
from programy.utils.logging.ylogger import YLogger

from abc import ABCMeta, abstractmethod

from programy.utils.classes.loader import ClassLoader
from programy.activate import Activatable


class SpellingChecker(Activatable):
    __metaclass__ = ABCMeta

    def __init__(self, spelling_config=None):
        Activatable.__init__(self)
        self.spelling_config = spelling_config

    def initialise(self, storage_factory):
        pass

    @abstractmethod
    def correct(self, phrase):
        raise NotImplementedError()

    @staticmethod
    def initiate_spellchecker(spelling_config, storage_factory):
        if spelling_config.classname is not None:
            try:
                YLogger.info(None, "Loading spelling checker from class [%s]", spelling_config.classname)
                spell_class = ClassLoader.instantiate_class(spelling_config.classname)
                spell_checker = spell_class(spelling_config)
                spell_checker.initialise(storage_factory)
                return spell_checker
            except Exception as excep:
                YLogger.exception(None, "Failed to initiate spellcheker", excep)
        else:
            YLogger.warning(None, "No configuration setting for spelling checker!")

        return None
    
    def check_spelling_before(self, client_context, each_sentence):
        if self.is_active():
            if self.spelling_config.check_before is True:
                text = each_sentence.text()
                corrected = self.correct(text)
                YLogger.debug(client_context, "Spell Checker corrected [%s] to [%s]", text, corrected)
                each_sentence.replace_words(corrected)

        else:
            YLogger.debug(client_context, "Spelling is switched off.")

    def check_spelling_and_retry(self, client_context, each_sentence):
        if self.is_active():
            if self.spelling_config.check_and_retry is True:
                text = each_sentence.text()
                corrected = self.correct(text)
                YLogger.debug(client_context, "Spell Checker corrected [%s] to [%s]", text, corrected)
                each_sentence.replace_words(corrected)
                response = client_context.brain.ask_question(client_context, each_sentence)
                return response

        else:
            YLogger.debug(client_context, "Spelling is switched off.")

        return None


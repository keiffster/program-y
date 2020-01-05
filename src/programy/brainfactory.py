"""
Copyright (c) 2016-2020 Keith Sterling http://www.keithsterling.com

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
from abc import ABC
from abc import abstractmethod
from programy.brain import Brain
from programy.utils.classes.loader import ClassLoader
from programy.utils.logging.ylogger import YLogger


class BrainSelector(ABC):

    def __init__(self, configuration):
        self._configuration = configuration

    @abstractmethod
    def select_brain(self):
        raise NotImplementedError()  # pragma: no cover


class DefaultBrainSelector(BrainSelector):

    def __init__(self, configuration, brains):
        BrainSelector.__init__(self, configuration)
        self._brains = brains
        self._iterator = None
        self._set_iterator()

    def _set_iterator(self):
        self._iterator = iter(self._brains.values())

    def select_brain(self):
        try:
            return next(self._iterator)

        except StopIteration:
            self._set_iterator()

            try:
                return next(self._iterator)
            except StopIteration:
                pass

        return None


class BrainFactory:

    def __init__(self, bot):
        self._brains = {}
        self._brain_selector = None
        self.loads_brains(bot)
        self.load_brain_selector(bot.configuration)

    def brainids(self):
        return list(self._brains.keys())

    def brain(self, brainid):
        if brainid in self._brains:
            return self._brains[brainid]
        else:
            return None

    def loads_brains(self, bot):
        for config in bot.configuration.configurations:
            brain = Brain(bot, config)
            self._brains[brain.id] = brain

    def load_brain_selector(self, configuration):
        if configuration.brain_selector is None:
            self._brain_selector = DefaultBrainSelector(configuration, self._brains)
        else:
            try:
                self._brain_selector = ClassLoader.instantiate_class(configuration.brain_selector)(configuration,
                                                                                                   self._brains)
            except Exception as excep:
                YLogger.exception_nostack(self, "Failed to load defined brain selector, loadiing default", excep)
                self._brain_selector = DefaultBrainSelector(configuration, self._brains)

    def select_brain(self):
        return self._brain_selector.select_brain()

    def get_question_counts(self):
        brains = []
        for brainid, brain in self._brains.items():
            brains.append({"id": brainid,
                           "questions": brain.num_questions})
        return brains

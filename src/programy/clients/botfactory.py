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
from programy.bot import Bot
from programy.utils.classes.loader import ClassLoader
from abc import abstractmethod, ABCMeta


class BotSelector(object):
    __metaclass__ = ABCMeta

    def __init__(self, configuration):
        self._configuration = configuration

    @abstractmethod
    def select_bot(self, bots):
        raise NotImplementedError()


class DefaultBotSelector(BotSelector):

    def __init__(self, configuration, bots):
        BotSelector.__init__(self, configuration)
        self._iterator = None
        self._bots = bots
        self._set_iterator()

    def _set_iterator(self):
        if self._bots:
            self._iterator = iter(self._bots.values())

    def select_bot(self):
        try:
            if self._iterator:
                return next (self._iterator)

        except StopIteration:
            self._set_iterator()

            try:
                if self._iterator:
                    return next(self._iterator)
            except StopIteration:
                pass

        return None


class BotFactory(object):

    def __init__(self, client, configuration):
        self._client = client
        self._bots = {}
        self._bot_selector = None

        self.load_bots(configuration)
        self.load_bot_selector(configuration)

    def botids(self):
        return self._bots.keys()

    def bot(self, id):
        if id in self._bots:
            return self._bots[id]
        else:
            return None

    def load_bots(self, configuration):
        for config in configuration.configurations:
            bot = Bot(config, client=self._client)
            self._bots[bot.id] = bot

    def load_bot_selector(self, configuration):
        if configuration.bot_selector is None:
            self._bot_selector = DefaultBotSelector(configuration, self._bots)
        else:
            try:
                self._bot_selector = ClassLoader.instantiate_class(configuration.bot_selector)(configuration, self._bots)
            except Exception as e:
                self._bot_selector = DefaultBotSelector(configuration, self._bots)

    def select_bot(self):
        return self._bot_selector.select_bot()

    def get_question_counts(self):
        bots = []
        for botid, bot in self._bots.items():
            brains = bot.get_question_counts()
            bots.append({"id": botid,
                         "questions": bot.num_questions,
                         "brains": brains})
        return bots


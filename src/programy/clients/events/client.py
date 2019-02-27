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

from programy.clients.client import BotClient


class EventBotClient(BotClient):

    def __init__(self, id, argument_parser=None):
        self._running = False
        BotClient.__init__(self, id, argument_parser=argument_parser)

    def prior_to_run_loop(self):
        pass

    def run_loop(self):
        self._running = True
        while self._running is True:
            self._running = self.wait_and_answer()

    def wait_and_answer(self):
        raise NotImplementedError("You must override this and implement the logic wait for a question and send an answer back")

    def post_run_loop(self):
        pass

    def run(self):

        if self.arguments.noloop is False:
            YLogger.info(self, "Entering conversation loop...")

            self.startup()

            self.prior_to_run_loop()

            self.run_loop()

            self.post_run_loop()

            self.shutdown()

        else:
            YLogger.debug(self, "noloop set to True, exiting...")

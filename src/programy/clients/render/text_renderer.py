"""
Copyright (c) 2016-2018 Keith Sterling http://www.keithsterling.com

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

from pymessenger.bot import Bot

from programy.clients.renderer import RichMediaRenderer


class TextRenderer(RichMediaRenderer):

    def __init__(self):
        RichMediaRenderer.__init__(self)

    def handle_text(self, userid, text):
        self._bot.send_message(userid, text)

    def handle_url_button(self, userid, text, url):
        pass

    def handle_postback_button(self, userid, text, postback):
        pass

    def handle_link(self, userid, text, url):
        pass

    def handle_image(self, userid, url):
        pass

    def handle_video(self, userid, url):
        pass

    def handle_card(self, userid, image, title, substitle, buttons):
        pass

    def handle_carousel(self, userid, cards):
        pass

    def handle_reply(self, userid, text, postback):
        pass

    def handle_delay(self, userid, seconds):
        pass

    def handle_split(self):
        pass

    def handle_list(self, userid, items):
        pass

    def handle_ordered_list(self, userid, items):
        pass

    def handle_location(self, userid):
        pass
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

import urllib.parse

from programy.clients.renderer import RichMediaRenderer


class HtmlRenderer(RichMediaRenderer):

    def __init__(self, config):
        RichMediaRenderer.__init__(self, config)

    def create_postback_url(self, postback):
        host = self._config.host
        port = self._config.port
        api = self._config.api
        question = urllib.parse.quote_plus(postback)
        return "%s:%s%squestion=%s"%(host, port, api, question)

    def handle_text(self, userid, text):
        self._bot.send_message(userid, text)

    def handle_url_button(self, userid, text, url):
        return '<a href="%s">%s</a>'%(url, text)

    def handle_postback_button(self, userid, text, postback):
        url = self.create_postback_url(postback)
        return '<a href="%s">%s</a>'%(url, text)

    def handle_link(self, userid, text, url):
        return '<a href="%s">%s</a>'%(url, text)

    def handle_image(self, userid, url):
        return '<img src="%s" />'%url

    def handle_video(self, userid, url):
        return """
        <video src="%s">
        Sorry, your browser doesn't support embedded videos, 
        but don't worry, you can <a href="%s">download it</a>
        and watch it with your favorite video player!
        </video>
        """%(url, url)

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
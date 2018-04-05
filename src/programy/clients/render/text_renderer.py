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

import time

from programy.clients.render.renderer import RichMediaRenderer


class TextRenderer(RichMediaRenderer):

    def __init__(self, client):
        RichMediaRenderer.__init__(self, client)

    def handle_text(self, userid, text):
        return self._client.display_response(text)

    def handle_url_button(self, userid, text, url):
        str = "%s, click %s"%(text, url)
        self._client.display_response(str)

    def handle_postback_button(self, userid, text, postback):
        self._client.display_response(postback)

    def handle_link(self, userid, text, url):
        str = "Open in browser, click %s"%url
        self._client.display_response(str)

    def handle_image(self, userid, url):
        str = "To see the image, click %s"%url
        self._client.display_response(str)

    def handle_video(self, userid, url):
        str = "To see the video, click %s"%url
        self._client.display_response(str)

    def _format_card(self, userid, image, title, subtitle, buttons):
        str = "Image: %s\nTitle: %s\nSubtitle: %s\n"%(image, title, subtitle)
        for button in buttons:
            str += "---------------------------------------\n"
            text = button[0]
            url = button[1]
            postback = button[2]
            if url is not None:
                str += "%s : %s"%(text, url)
            else:
                str += "%s : %s" % (text, postback)
            str += "\n---------------------------------------\n"
        return str
    
    def handle_card(self, userid, image, title, subtitle, buttons):
        str = self._format_card(userid, image, title, subtitle, buttons)
        self._client.display_response(str)

    def handle_carousel(self, userid, cards):
        str = ""
        for card in cards:
            str += "=========================================\n"
            image = card[0]
            title = card[1]
            subtitle = card[2]
            buttons = card[3]
            str += self._format_card(userid, image, title, subtitle, buttons)
            str += "=========================================\n"
        self._client.display_response(str)

    def handle_reply(self, userid, text, postback):
        if postback is not None:
            self._client.display_response(postback)
        else:
            self._client.display_response(text)

    def handle_delay(self, userid, seconds):
        self._client.display_response("...")
        delay = int(seconds)
        time.sleep(delay)

    def handle_split(self, userid):
        return

    def handle_list(self, userid, items):
        str = ""
        for item in items:
            str += "> %s\n"%item
        self._client.display_response(str)

    def handle_ordered_list(self, userid, items):
        str = ""
        count = 1
        for item in items:
            str += "%d. %s\n"%(count, item)
            count += 1
        self._client.display_response(str)

    def handle_location(self, userid):
        str = ""
        self._client.display_response(str)

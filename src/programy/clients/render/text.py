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

    def __init__(self, callback):
        RichMediaRenderer.__init__(self, callback)

    def handle_text(self, client_context, text):
        if self._client:
            self._client.process_response(client_context, text)
        return text

    def handle_url_button(self, client_context, text, url):
        str = "%s, click %s"%(text, url)
        if self._client:
            self._client.process_response(client_context, str)
        return str

    def handle_postback_button(self, client_context, text, postback):
        if self._client:
            self._client.process_response(client_context, postback)
        return postback

    def handle_link(self, client_context, text, url):
        str = "Open in browser, click %s"%url
        if self._client:
            self._client.process_response(client_context, str)
        return str

    def handle_image(self, client_context, url):
        str = "To see the image, click %s"%url
        if self._client:
            self._client.process_response(client_context, str)
        return str

    def handle_video(self, client_context, url):
        str = "To see the video, click %s"%url
        if self._client:
            self._client.process_response(client_context, str)
        return str

    def _format_card(self, client_context, image, title, subtitle, buttons):
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
    
    def handle_card(self, client_context, image, title, subtitle, buttons):
        str = self._format_card(client_context, image, title, subtitle, buttons)
        if self._client:
            self._client.process_response(client_context, str)
        return str

    def handle_carousel(self, client_context, cards):
        str = ""
        for card in cards:
            str += "=========================================\n"
            image = card[0]
            title = card[1]
            subtitle = card[2]
            buttons = card[3]
            str += self._format_card(client_context, image, title, subtitle, buttons)
            str += "=========================================\n"
        self._client.process_response(client_context, str)

    def handle_reply(self, client_context, text, postback):
        if postback is not None:
            if self._client:
                self._client.process_response(client_context, postback)
                return postback
        else:
            if self._client:
                self._client.process_response(client_context, text)
            return text

    def handle_delay(self, client_context, seconds):
        str = "..."
        if self._client:
            self._client.process_response(client_context, str)
        delay = int(seconds)
        time.sleep(delay)
        return str

    def handle_split(self, client_context):
        return ""

    def handle_list(self, client_context, items):
        str = ""
        for item in items:
            str += "> %s\n"%item
        self._client.process_response(client_context, str)

    def handle_ordered_list(self, client_context, items):
        str = ""
        count = 1
        for item in items:
            str += "%d. %s\n"%(count, item)
            count += 1
        if self._client:
            self._client.process_response(client_context, str)
        return str

    def handle_location(self, client_context):
        str = ""
        if self._client:
            self._client.process_response(client_context, str)
        return str
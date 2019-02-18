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

import time

from programy.clients.render.renderer import RichMediaRenderer


class TextRenderer(RichMediaRenderer):

    def __init__(self, callback):
        RichMediaRenderer.__init__(self, callback)

    def handle_text(self, client_context, text):
        if self._client:
            self._client.process_response(client_context, text['text'])
        return text

    def handle_url_button(self, client_context, button):
        str = "%s, click %s"%(button['text'], button['url'])
        if self._client:
            self._client.process_response(client_context, str)
        return str

    def handle_postback_button(self, client_context, button):
        if self._client:
            self._client.process_response(client_context, button['postback'])
        return button['postback']

    def handle_link(self, client_context, link):
        str = "Open in browser, click %s"%link['url']
        if self._client:
            self._client.process_response(client_context, str)
        return str

    def handle_image(self, client_context, image):
        str = "To see the image, click %s"%image['url']
        if self._client:
            self._client.process_response(client_context, str)
        return str

    def handle_video(self, client_context, video):
        str = "To see the video, click %s"%video['url']
        if self._client:
            self._client.process_response(client_context, str)
        return str

    def _format_card(self, client_context, card):
        str = "Image: %s\nTitle: %s\nSubtitle: %s\n"%(card['image'], card['title'], card['subtitle'])
        for button in card['buttons']:
            str += "---------------------------------------\n"
            if button['url'] is not None:
                str += "%s : %s"%(button['text'], button['url'])
            else:
                str += "%s : %s" % (button['text'], button['postback'])
            str += "\n---------------------------------------\n"
        return str
    
    def handle_card(self, client_context, card):
        str = self._format_card(client_context, card)
        if self._client:
            self._client.process_response(client_context, str)
        return str

    def handle_carousel(self, client_context, carousel):
        str = ""
        for card in carousel['cards']:
            str += "=========================================\n"
            str += self._format_card(client_context, card)
            str += "=========================================\n"
        self._client.process_response(client_context, str)

    def handle_reply(self, client_context, reply):
        if reply['postback'] is not None:
            if self._client:
                self._client.process_response(client_context, reply['postback'])
                return reply['postback']
        else:
            if self._client:
                self._client.process_response(client_context, reply['text'])
            return reply['text']

    def handle_delay(self, client_context, delay):
        str = "..."
        if self._client:
            self._client.process_response(client_context, str)
        delay = int(delay['seconds'])
        time.sleep(delay)
        return str

    def handle_split(self, client_context, split):
        self._client.process_response(client_context, "\n")
        return "\n"

    def handle_list(self, client_context, list):
        str = ""
        for item in list['items']:
            str += "> %s\n"%item['text']
        self._client.process_response(client_context, str)

    def handle_ordered_list(self, client_context, list):
        str = ""
        count = 1
        for item in list['items']:
            str += "%d. %s\n"%(count, item['text'])
            count += 1
        if self._client:
            self._client.process_response(client_context, str)
        return str

    def handle_location(self, client_context, location):
        str = ""
        if self._client:
            self._client.process_response(client_context, str)
        return str
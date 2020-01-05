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
import time

from programy.clients.render.renderer import RichMediaRenderer


class TextRenderer(RichMediaRenderer):

    def __init__(self, callback):
        RichMediaRenderer.__init__(self, callback)

    def _default_output(self):
        return ""

    def _concat_result(self, first, second):
        return first + second

    def handle_text(self, client_context, text):
        if self._client:
            self._client.process_response(client_context, text['text'])
        return text['text']

    def handle_url_button(self, client_context, button):
        rendered = "%s, click %s" % (button['text'], button['url'])
        if self._client:
            self._client.process_response(client_context, rendered)
        return rendered

    def handle_postback_button(self, client_context, button):
        if self._client:
            self._client.process_response(client_context, button['postback'])
        return button['postback']

    def handle_link(self, client_context, link):
        rendered = "Open in browser, click %s" % link['url']
        if self._client:
            self._client.process_response(client_context, rendered)
        return rendered

    def handle_image(self, client_context, image):
        rendered = "To see the image, click %s" % image['url']
        if self._client:
            self._client.process_response(client_context, rendered)

        return rendered

    def handle_video(self, client_context, video):
        rendered = "To see the video, click %s" % video['url']
        if self._client:
            self._client.process_response(client_context, rendered)

        return rendered

    def _format_card(self, client_context, card):
        del client_context
        rendered = "Image: %s\nTitle: %s\nSubtitle: %s\n" % (card['image'], card['title'], card['subtitle'])
        for button in card['buttons']:
            rendered += "---------------------------------------\n"
            if button['url'] is not None:
                rendered += "%s : %s" % (button['text'], button['url'])
            else:
                rendered += "%s : %s" % (button['text'], button['postback'])
            rendered += "\n---------------------------------------\n"
        return rendered

    def handle_card(self, client_context, card):
        rendered = self._format_card(client_context, card)
        if self._client:
            self._client.process_response(client_context, rendered)
        return rendered

    def handle_carousel(self, client_context, carousel):
        rendered = ""
        for card in carousel['cards']:
            rendered += "=========================================\n"
            rendered += self._format_card(client_context, card)
            rendered += "=========================================\n"
        self._client.process_response(client_context, rendered)

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
        rendered = "..."
        if self._client:
            self._client.process_response(client_context, rendered)
        delay = int(delay['seconds'])
        time.sleep(delay)
        return rendered

    def handle_split(self, client_context, split):
        self._client.process_response(client_context, "\n")
        return "\n"

    def handle_list(self, client_context, lst):
        rendered = ""
        for item in lst.get('items', []):
            rendered += "> %s\n" % item['text']
        self._client.process_response(client_context, rendered)

    def handle_ordered_list(self, client_context, lst):
        rendered = ""
        count = 1
        for item in lst.get('items', []):
            rendered += "%d. %s\n" % (count, item['text'])
            count += 1
        if self._client:
            self._client.process_response(client_context, rendered)
        return rendered

    def handle_location(self, client_context, location):
        del location
        rendered = ""
        if self._client:
            self._client.process_response(client_context, rendered)

        return rendered

    def handle_tts(self, client_context, tts):
        del client_context
        del tts
        return ""

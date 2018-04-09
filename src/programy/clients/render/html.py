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
import urllib.parse

from programy.clients.render.text import TextRenderer


class HtmlRenderer(TextRenderer):

    def __init__(self, callback=None):
        TextRenderer.__init__(self, callback)

    def create_postback_url(self):
        return "#"

    def handle_text(self, client_context, text):
        str = "%s"%text
        if self._client:
            self._client.process_response(client_context, str)
        return str

    def handle_url_button(self, client_context, text, url):
        str = '<a href="%s">%s</a>'%(url, text)
        if self._client:
            self._client.process_response(client_context, str)
        return str

    def handle_postback_button(self, client_context, text, postback):
        url = self.create_postback_url()
        str = '<a class="postback" postback="%s" href="#">%s</a>' % (postback, text)
        if self._client:
            self._client.process_response(client_context, str)
        return str

    def handle_link(self, client_context, text, url):
        str = '<a href="%s">%s</a>'%(url, text)
        if self._client:
            self._client.process_response(client_context, str)
        return str

    def handle_image(self, client_context, url):
        str = '<img src="%s" />'%url
        if self._client:
            self._client.process_response(client_context, str)
        return str

    def handle_video(self, client_context, url):
        str = """<video src="%s">
Sorry, your browser doesn't support embedded videos, 
but don't worry, you can <a href="%s">download it</a>
and watch it with your favorite video player!
</video>"""%(url, url)
        if self._client:
            self._client.process_response(client_context, str)
        return str

    def _format_card(self, image, title, subtitle, buttons):
        str = '<div class="card" >'
        str += '<img src="%s" />' % image
        str += '<h1>%s</h1>' % title
        str += '<h2>%s</h2>' % subtitle
        for button in buttons:
            if button[1] is not None:
                str += '<a href="%s">%s</a>' % (button[1], button[0])
            else:
                postback = self.create_postback_url()
                str += '<a class="postback" href="%s">%s</a>' % (postback, button[0])
        str += '</div>'
        return str

    def handle_card(self, client_context, image, title, subtitle, buttons):
        str = self._format_card(image, title, subtitle, buttons)
        if self._client:
            self._client.process_response(client_context, str)
        return str

    def handle_carousel(self, client_context, cards):
        str = '<div class="carousel">'
        for card in cards:
            str += self._format_card(card[0], card[1], card[2], card[3])
        str += "</div>"
        if self._client:
            self._client.process_response(client_context, str)
        return str

    def handle_reply(self, client_context, text, postback):
        str = ''
        if postback is not None:
            str += '<a class="postback" postback="%s" href="#">%s</a>' % (postback, text)
        else:
            str += '<a class="postback" postback="%s" href="#">%s</a>' % (text, text)
        if self._client:
            self._client.process_response(client_context, str)
        return str

    def handle_delay(self, client_context, seconds):
        str = '<div class="delay">...</div>'
        if self._client:
            self._client.process_response(client_context, str)
        return str

    def handle_split(self, client_context):
        str = ""
        if self._client:
            self._client.process_response(client_context, str)
        return str

    def handle_list(self, client_context, items):
        str = "<ul>"
        for item in items:
            str += "<li>%s</li>"%item
        str += "</ul>"
        if self._client:
            self._client.process_response(client_context, str)
        return str

    def handle_ordered_list(self, client_context, items):
        str = "<ol>"
        for item in items:
            str += "<li>%s</li>" % item
        str += "</ol>"
        if self._client:
            self._client.process_response(client_context, str)
        return str

    def handle_location(self, client_context):
        str = ""
        if self._client:
            self._client.process_response(client_context, str)
        return str
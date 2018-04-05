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

from programy.clients.render.text_renderer import TextRenderer


class HtmlRenderer(TextRenderer):

    def __init__(self, client):
        TextRenderer.__init__(self, client)

    def create_postback_url(self, postback):
        host = self._client.configuration.host
        port = self._client.configuration.port
        api = self._client.configuration.api
        question = urllib.parse.quote_plus(postback)
        return "http://%s:%s%squestion=%s"%(host, port, api, question)

    def handle_text(self, userid, text):
        str = "<p>%s</p>"%text
        self._client.display_response(str)

    def handle_url_button(self, userid, text, url):
        str = '<a href="%s">%s</a>'%(url, text)
        self._client.display_response(str)

    def handle_postback_button(self, userid, text, postback):
        url = self.create_postback_url(postback)
        str = '<a href="%s">%s</a>'%(url, text)
        self._client.display_response(str)

    def handle_link(self, userid, text, url):
        str = '<a href="%s">%s</a>'%(url, text)
        self._client.display_response(str)

    def handle_image(self, userid, url):
        str = '<img src="%s" />'%url
        self._client.display_response(str)

    def handle_video(self, userid, url):
        str = """<video src="%s">
Sorry, your browser doesn't support embedded videos, 
but don't worry, you can <a href="%s">download it</a>
and watch it with your favorite video player!
</video>"""%(url, url)
        self._client.display_response(str)

    def _format_card(self, image, title, subtitle, buttons):
        str = '<div class="card" >'
        str += '<img src="%s" />' % image
        str += '<h1>%s</h1>' % title
        str += '<h2>%s</h2>' % subtitle
        for button in buttons:
            if button[1] is not None:
                str += '<a href="%s">%s</a>' % (button[1], button[0])
            else:
                postback = self.create_postback_url(button[2])
                str += '<a href="%s">%s</a>' % (postback, button[0])
        str += '</div>'
        return str

    def handle_card(self, userid, image, title, subtitle, buttons):
        str = self._format_card(image, title, subtitle, buttons)
        self._client.display_response(str)

    def handle_carousel(self, userid, cards):
        str = "<carousel>"
        for card in cards:
            str += self._format_card(card[0], card[1], card[2], card[3])
        str += "</carousel>"
        self._client.display_response(str)

    def handle_reply(self, userid, text, postback):
        str = '<div class="reply">'
        if postback is not None:
            url = self.create_postback_url(postback)
        else:
            url = self.create_postback_url(text)
        str += '<a href="%s">%s</a>'%(url, text)
        str += '</div>'
        self._client.display_response(str)

    def handle_delay(self, userid, seconds):
        self._client.display_response('<div class="delay">...</div>')
        delay = int(seconds)
        time.sleep(delay)

    def handle_split(self, userid):
        str = ""
        self._client.display_response(str)

    def handle_list(self, userid, items):
        str = "<ul>"
        for item in items:
            str += "<li>%s</li>"%item
        str += "</ul>"
        self._client.display_response(str)

    def handle_ordered_list(self, userid, items):
        str = "<ol>"
        for item in items:
            str += "<li>%s</li>" % item
        str += "</ol>"
        self._client.display_response(str)

    def handle_location(self, userid):
        str = ""
        self._client.display_response(str)

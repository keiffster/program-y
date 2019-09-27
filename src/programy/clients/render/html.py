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
from programy.clients.render.text import TextRenderer


class HtmlRenderer(TextRenderer):

    def __init__(self, callback=None):
        TextRenderer.__init__(self, callback)

    def create_postback_url(self):
        return "#"

    def handle_text(self, client_context, text):
        rendered = "%s" % text['text']
        if self._client:
            self._client.process_response(client_context, rendered)
        return rendered

    def handle_url_button(self, client_context, button):
        rendered = '<a href="%s">%s</a>' % (button['url'], button['text'])
        if self._client:
            self._client.process_response(client_context, rendered)
        return rendered

    def handle_postback_button(self, client_context, button):
        rendered = '<a class="postback" postback="%s" href="#">%s</a>' % (button['postback'], button['text'])
        if self._client:
            self._client.process_response(client_context, rendered)
        return rendered

    def handle_link(self, client_context, link):
        rendered = '<a href="%s">%s</a>' % (link['url'], link['text'])
        if self._client:
            self._client.process_response(client_context, rendered)
        return rendered

    def handle_image(self, client_context, image):
        rendered = '<img src="%s" />' % image['url']
        if self._client:
            self._client.process_response(client_context, rendered)
        return rendered

    def handle_video(self, client_context, video):
        rendered = """<video src="%s">
Sorry, your browser doesn't support embedded videos, 
but don't worry, you can <a href="%s">download it</a>
and watch it with your favorite video player!
</video>""" % (video['url'], video['url'])
        if self._client:
            self._client.process_response(client_context, rendered)
        return rendered

    def _format_card(self, client_context, card):
        rendered = '<div class="card" >'
        rendered += '<img src="%s" />' % card['image']
        rendered += '<h1>%s</h1>' % card['title']
        rendered += '<h2>%s</h2>' % card['subtitle']
        for button in card['buttons']:
            if button['url'] is not None:
                rendered += '<a href="%s">%s</a>' % (button['url'], button['text'])
            else:
                rendered += '<a class="postback" postback="%s" href="#">%s</a>' % (button['postback'], button['text'])
        rendered += '</div>'
        return rendered

    def handle_card(self, client_context, card):
        rendered = self._format_card(client_context, card)
        if self._client:
            self._client.process_response(client_context, rendered)
        return rendered

    def handle_carousel(self, client_context, carousel):
        rendered = '<div class="carousel">'
        for card in carousel['cards']:
            rendered += self._format_card(client_context, card)
        rendered += "</div>"
        if self._client:
            self._client.process_response(client_context, rendered)
        return rendered

    def handle_reply(self, client_context, reply):
        rendered = ''
        if reply['postback'] is not None:
            rendered += '<a class="postback" postback="%s" href="#">%s</a>' % (reply['postback'], reply['text'])
        else:
            rendered += '<a class="postback" postback="%s" href="#">%s</a>' % (reply['text'], reply['text'])
        if self._client:
            self._client.process_response(client_context, rendered)
        return rendered

    def handle_delay(self, client_context, delay):
        rendered = '<div class="delay">...</div>'
        if self._client:
            self._client.process_response(client_context, rendered)
        return rendered

    def handle_split(self, client_context, split):
        rendered = "<br />"
        if self._client:
            self._client.process_response(client_context, rendered)
        return rendered

    def handle_list(self, client_context, lst):
        rendered = "<ul>"
        for item in lst.get('items', []):
            rendered += "<li>%s</li>" % item['text']
        rendered += "</ul>"
        if self._client:
            self._client.process_response(client_context, rendered)
        return rendered

    def handle_ordered_list(self, client_context, lst):
        rendered = "<ol>"
        for item in lst.get('items', []):
            rendered += "<li>%s</li>" % item['text']
        rendered += "</ol>"
        if self._client:
            self._client.process_response(client_context, rendered)
        return rendered

    def handle_location(self, client_context, location):
        rendered = ""
        if self._client:
            self._client.process_response(client_context, rendered)
        return rendered

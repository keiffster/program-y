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
from programy.clients.render.text import TextRenderer


class HtmlRenderer(TextRenderer):

    def __init__(self, callback=None):
        TextRenderer.__init__(self, callback)

    def create_postback_url(self):
        return "#"

    def handle_text(self, client_context, text, response=True):
        rendered = "%s" % text['text']
        if self._client and response is True:
            self._client.process_response(client_context, rendered)
        return rendered

    def _add_class_and_id(self, data, rendered):
        toreturn = ""

        if 'class' in data:
            toreturn += ' class="%s programy"'%data['class']
        else:
            toreturn += ' class="programy"'

        if 'id' in data:
            toreturn += ' id="%s"'%data['id']

        return toreturn

    def handle_url_button(self, client_context, button, response=True):
        rendered = '<a'
        rendered += self._add_class_and_id(button, rendered)
        rendered += ' href="%s">%s</a>' % (button['url'], button['text'])
        if self._client and response is True:
            self._client.process_response(client_context, rendered)
        return rendered

    def handle_postback_button(self, client_context, button, response=True):
        rendered = '<a'
        rendered += self._add_class_and_id(button, rendered)
        rendered += ' postback="%s" href="#">%s</a>' % (button['postback'], button['text'])
        if self._client and response is True:
            self._client.process_response(client_context, rendered)
        return rendered

    def handle_link(self, client_context, link, response=True):
        rendered = '<a'
        rendered += self._add_class_and_id(link, rendered)
        rendered += ' href="%s">%s</a>' % (link['url'], link['text'])
        if self._client and response is True:
            self._client.process_response(client_context, rendered)
        return rendered

    def handle_image(self, client_context, image, response=True):
        rendered = '<img'
        rendered += self._add_class_and_id(image, rendered)
        rendered += ' src="%s" />' % image['url']
        if self._client and response is True:
            self._client.process_response(client_context, rendered)
        return rendered

    def handle_video(self, client_context, video, response=True):
        rendered = '<video'
        rendered += self._add_class_and_id(video, rendered)
        rendered += ' src="%s">'%video['url']
        rendered += """\nSorry, your browser doesn't support embedded videos, 
but don't worry, you can <a href="%s">download it</a>
and watch it with your favorite video player!
</video>""" %video['url']
        if self._client and response is True:
            self._client.process_response(client_context, rendered)
        return rendered

    def _format_card(self, client_context, card):
        rendered = '<div'
        rendered += self._add_class_and_id(card, rendered)
        rendered += '>'
        rendered += '<img src="%s" />' % card['image']
        rendered += '<h1>%s</h1>' % card['title']
        rendered += '<h2>%s</h2>' % card['subtitle']
        for button in card['buttons']:
            if button['url'] is not None:
                rendered += '<a href="%s">%s</a>' % (button['url'], button['text'])
            else:
                rendered += '<a postback="%s" href="#">%s</a>' % (button['postback'], button['text'])
        rendered += '</div>'
        return rendered

    def handle_card(self, client_context, card, response=True):
        rendered = self._format_card(client_context, card)
        if self._client and response is True:
            self._client.process_response(client_context, rendered)
        return rendered

    def handle_carousel(self, client_context, carousel, response=True):
        rendered = '<div'
        rendered += self._add_class_and_id(carousel, rendered)
        rendered += '>'
        for card in carousel['cards']:
            rendered += self._format_card(client_context, card)
        rendered += "</div>"
        if self._client and response is True:
            self._client.process_response(client_context, rendered)
        return rendered

    def handle_reply(self, client_context, reply, response=True):
        rendered = ''
        if reply['postback'] is not None:
            rendered += '<a'
            rendered += self._add_class_and_id(reply, rendered)
            rendered += ' postback="%s" href="#">%s</a>' % (reply['postback'], reply['text'])
        else:
            rendered += '<a'
            rendered += self._add_class_and_id(reply, rendered)
            rendered += ' postback="%s" href="#">%s</a>' % (reply['text'], reply['text'])
        if self._client and response is True:
            self._client.process_response(client_context, rendered)
        return rendered

    def handle_delay(self, client_context, delay, response=True):
        rendered = '<div'
        rendered += self._add_class_and_id(delay, rendered)
        rendered += '>...</div>'
        if self._client and response is True:
            self._client.process_response(client_context, rendered)
        return rendered

    def handle_split(self, client_context, split, response=True):
        rendered = "<br"
        rendered += self._add_class_and_id(split, rendered)
        rendered += " />"
        if self._client and response is True:
            self._client.process_response(client_context, rendered)
        return rendered

    def handle_list(self, client_context, lst, response=True):
        rendered = "<ul"
        rendered += self._add_class_and_id(lst, rendered)
        rendered += ">"
        for item in lst.get('items', []):
            rendered += "<li>%s</li>" % self._handle_children(client_context, item)
        rendered += "</ul>"
        if self._client and response is True:
            self._client.process_response(client_context, rendered)
        return rendered

    def handle_ordered_list(self, client_context, lst, response=True):
        rendered = "<ol"
        rendered += self._add_class_and_id(lst, rendered)
        rendered += ">"
        for item in lst.get('items', []):
            rendered += "<li>%s</li>" % self._handle_children(client_context, item)
        rendered += "</ol>"
        if self._client and response is True:
            self._client.process_response(client_context, rendered)
        return rendered

    def handle_location(self, client_context, location, response=True):
        rendered = ""
        if self._client and response is True:
            self._client.process_response(client_context, rendered)
        return rendered

    def handle_xml(self, client_context, item, response=True):
        rendered = item['text']
        if self._client and response is True:
            self._client.process_response(client_context, rendered)
        return rendered

    def _handle_children(self, client_context, item):

        if item['type'] == 'button':
            return self.handle_button(client_context, item, response=False)

        elif item['type'] == 'link':
            return self.handle_link(client_context, item, response=False)

        elif item['type'] == 'image':
            return self.handle_image(client_context, item, response=False)

        elif item['type'] == 'video':
            return self.handle_video(client_context, item, response=False)

        elif item['type'] == 'card':
            return self.handle_card(client_context, item, response=False)

        elif item['type'] == 'carousel':
            return self.handle_carousel(client_context, item, response=False)

        elif item['type'] == 'reply':
            return self.handle_reply(client_context, item, response=False)

        elif item['type'] == 'delay':
            return self.handle_delay(client_context, item, response=False)

        elif item['type'] == 'split':
            return self.handle_split(client_context, item, response=False)

        elif item['type'] == 'list':
            return self.handle_list(client_context, item, response=False)

        elif item['type'] == 'olist':
            return self.handle_ordered_list(client_context, item, response=False)

        elif item['type'] == 'location':
            return self.handle_location(client_context, item, response=False)

        elif item['type'] == 'tts':
            return self.handle_tts(client_context, item, response=False)

        elif item['type'] == 'text':
            return self.handle_text(client_context, item, response=False)

        return self.handle_xml(client_context, item, response=False)


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

from programy.clients.render.renderer import RichMediaRenderer


class JSONRenderer(RichMediaRenderer):

    def __init__(self, callback=None):
        RichMediaRenderer.__init__(self, callback)

    def handle_text(self, client_context, text):
        data = {"text": text}
        if self._client:
            return self._client.process_response(client_context, data)
        return data

    def handle_url_button(self, client_context, text, url):
        data = {"button": {"text": text, "url": url}}
        if self._client:
            self._client.process_response(client_context, data)
        return data

    def handle_postback_button(self, client_context, text, postback):
        data = {"button": {"text": text, "postback": postback}}
        if self._client:
            self._client.process_response(client_context, data)
        return data

    def handle_link(self, client_context, text, url):
        data = {"link": {"text": text, "url": url}}
        if self._client:
            self._client.process_response(client_context, data)
        return data

    def handle_image(self, client_context, url):
        data = {"image": {"url": url}}
        if self._client:
            self._client.process_response(client_context, data)
        return data

    def handle_video(self, client_context, url):
        data = {"video": {"url": url}}
        if self._client:
            self._client.process_response(client_context, data)
        return data

    def _format_card(self, client_context, image, title, subtitle, buttons):
        data = {"card": {
            "image": image, "title": title, "subtitle": subtitle, "buttons": []
        }}
        if buttons:
            for button in buttons:
                text = button[0]
                url = button[1]
                postback = button[2]
                if url is not None:
                    data['card']['buttons'].append({"button": {"text": text, "url": url}})
                else:
                    data['card']['buttons'].append({"button": {"text": text, "postback": postback}})
        return data
    
    def handle_card(self, client_context, image, title, subtitle, buttons):
        data = self._format_card(client_context, image, title, subtitle, buttons)
        if self._client:
            self._client.process_response(client_context, data)
        return data

    def handle_carousel(self, client_context, cards):
        data = {"carousel": { "cards": [] }}
        for card in cards:
            image = card[0]
            title = card[1]
            subtitle = card[2]
            buttons = card[3]
            data['carousel']['cards'].append(self._format_card(client_context, image, title, subtitle, buttons))
        if self._client:
            self._client.process_response(client_context, data)
        return data

    def handle_reply(self, client_context, text, postback):
        if postback is not None:
            data = {"reply": { "text": text}}
        else:
            data = {"reply": { "text": text, "postback": postback}}
        if self._client:
            self._client.process_response(client_context, data)
        return data

    def handle_delay(self, client_context, seconds):
        data = {"delay": { "seconds": seconds}}
        if self._client:
            self._client.process_response(client_context, data)
        return data

    def handle_split(self, client_context):
        data = {"split": {}}
        if self._client:
            self._client.process_response(client_context, data)
        return data

    def handle_list(self, client_context, items):
        data = {"list": { "items": []}}
        for item in items:
            data['list']['items'].append({"item": item})
        if self._client:
            self._client.process_response(client_context, data)
        return data

    def handle_ordered_list(self, client_context, items):
        count = 1
        data = {"olist": { "items": []}}
        for item in items:
            data['olist']['items'].append({"item": item, "pos": count})
            count += 1
        if self._client:
            self._client.process_response(client_context, data)
        return data

    def handle_location(self, client_context):
        data = {'location': {"xlat": "", "xlong": ""}}
        if self._client:
            self._client.process_response(client_context, data)
        return data

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


class FacebookRenderer(RichMediaRenderer):

    def __init__(self, client):
        RichMediaRenderer.__init__(self, client)

    def handle_text(self, client_context, text):
        payload = {
            'recipient': {
                'id': client_context.userid
            },
            'message': {
                'text': text
            }
        }
        return self._client.facebook_bot.send_raw(payload)

    def handle_url_button(self, client_context, text, url):
        payload = {
            "recipient": {
                "id": client_context.userid
            },
            "message": {
                "attachment": {
                    "type": "template",
                    "payload": {
                        "template_type": "button",
                        "text": text,
                        "buttons": [
                            {
                                "type": "web_url",
                                "url": url,
                                "title": text,
                                "webview_height_ratio": "full",
                                "messenger_extensions": "false"
                            }
                        ]
                    }
                }
            }

        }
        return self._client.facebook_bot.send_raw(payload)

    def handle_postback_button(self, client_context, text, postback):
        payload = {
            "recipient": {
                "id": client_context.userid
            },
            "message": {
                "attachment": {
                    "type": "template",
                    "payload": {
                        "template_type": "button",
                        "text": text,
                        "buttons": [
                            {
                                "type": "postback",
                                "title": text,
                                "payload": postback
                            }
                        ]
                    }
                }
            }
        }
        return self._client.facebook_bot.send_raw(payload)

    def handle_link(self, client_context, text, url):
        pass

    def handle_image(self, client_context, url):
        payload = {
            "recipient": {
                "id": client_context.userid
            },
            "message": {
                "attachment": {
                    "type": "template",
                    "payload": {
                        "template_type": "media",
                        "elements": [
                            {
                                "media_type": "image",
                                "url": url
                            }
                        ]
                    }
                }
            }
        }
        return self._client.facebook_bot.send_raw(payload)

    def handle_video(self, client_context, url):
        payload = {
            "recipient": {
                "id": client_context.userid
            },
            "message": {
                "attachment": {
                    "type": "template",
                    "payload": {
                        "template_type": "media",
                        "elements": [
                            {
                                "media_type": "video",
                                "url": url
                            }
                        ]
                    }
                }
            }
        }
        return self._client.facebook_bot.send_raw(payload)

    def handle_card(self, client_context, image, title, subtitle, buttons):

        if len(buttons) > 3:
            print("Warning more buttons than facebook allows for a card")

        payload = {
            'recipient': {
                'id': client_context.userid
            },
            'message': {
                "attachment": {
                    "type": "template",
                    "payload": {
                        "template_type": "generic",
                        "elements": []
                    }
                }
            }
        }

        payload['message']['attachment']['payload']['elements'].append({
            "title": "Welcome!",
            "image_url": "https://petersfancybrownhats.com/company_image.png",
            "subtitle": "We have the right hat for everyone.",

        })

        """
        for button in buttons:
            if button[1] is not None:
                payload['elements'][0]['buttons'].append({
                    "type": "url",
                    "title": button[0],
                    "url": button[1]
                })
            else:
                payload['elements'][0]['buttons'].append({
                    "type": "postback",
                    "title": button[0],
                    "payload": button[0]
                })
        """

        print(payload)

        return self._client.facebook_bot.send_raw(payload)

    def handle_carousel(self, client_context, cards):
        if len(cards) > 10:
            print("Warning more cards than facebook allows for a carousel")
        pass

    def handle_reply(self, client_context, text, postback):
        pass

    def handle_delay(self, client_context, seconds):
        pass

    def handle_split(self, client_context):
        pass

    def handle_list(self, client_context, items):
        pass

    def handle_ordered_list(self, client_context, items):
        pass

    def handle_location(self, client_context):
        pass
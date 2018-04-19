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
import json
import time

from programy.utils.logging.ylogger import YLogger

from programy.clients.render.renderer import RichMediaRenderer

class FacebookRenderer(RichMediaRenderer):

    def __init__(self, client):
        RichMediaRenderer.__init__(self, client)

    def print_payload(self, title, payload, indent=2, sort_keys=False):
        print(title, json.dumps(payload, indent=indent, sort_keys=sort_keys))

    def send_payload(self, payload):
        self.print_payload("Payload:", payload)
        result = self._client.facebook_bot.send_raw(payload)
        self.print_payload("Result:", result)
        return result

    def handle_text(self, client_context, text):
        print("Handling text...")
        payload = {
            'recipient': {
                'id': client_context.userid
            },
            'message': {
                'text': text
            }
        }
        return self.send_payload(payload)

    def handle_url_button(self, client_context, text, url):
        print("Handling url...")
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
                                "title": text
                            }
                        ]
                    }
                }
            }

        }
        return self.send_payload(payload)

    def handle_postback_button(self, client_context, text, postback):
        print("Handling postback button...")
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
        return self.send_payload(payload)

    def handle_link(self, client_context, text, url):
        print("Handling link...")
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
                                "title": text,
                                "url": url
                            }
                        ]
                    }
                }
            }
        }
        return self.send_payload(payload)

    def handle_image(self, client_context, url):
        print("Handling image...")
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
        return self.send_payload(payload)

    def handle_video(self, client_context, url):
        print("Handling video...")
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
        return self.send_payload(payload)

    def handle_card(self, client_context, image, title, subtitle, buttons):
        print("Handling card...")

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
                        "elements": [
                            {
                                "title": title,
                                "image_url": image,
                                "subtitle": subtitle,
                                "buttons": []
                            }
                        ]
                    }
                }
            }
        }

        for button in buttons:
            if button[1] is not None:
                payload['message']['attachment']['payload']['elements'][0]['buttons'].append({
                                "type": "web_url",
                                "title": button[0],
                                "url": button[1]
                            })
            else:
                payload['message']['attachment']['payload']['elements'][0]['buttons'].append({
                                "type": "web_url",
                                "title": button[0],
                                "url": button[2]
                            })

        return self.send_payload(payload)

    def handle_carousel(self, client_context, cards):
        print("Handling carousel...")
        if len(cards) > 10:
            print("Warning more cards than facebook allows for a carousel")

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

        for card in cards:
            image = card[0]
            title = card[1]
            subtitle = card[2]
            buttons = card[3]

            element = {
                "title": title,
                "image_url": image,
                "subtitle": subtitle,
                "buttons": []
            }

            for button in  buttons:
                if button[1] is not None:
                    element['buttons'].append({
                        "type": "web_url",
                        "title": button[0],
                        "url": button[1]
                    })
                else:
                    element['buttons'].append({
                        "type": "web_url",
                        "title": button[0],
                        "url": button[2]
                    })

            payload['message']['attachment']['payload']['elements'].append(element)

        return self.send_payload(payload)

    def handle_reply(self, client_context, text, postback):
        print("Handling reply...")
        if postback is None:
            return self.handle_postback_button(client_context, text, text)
        else:
            return self.handle_postback_button(client_context, text, postback)

    def handle_delay(self, client_context, seconds):
        print("Handling delay...")
        payload = {
            "recipient": {
                "id": client_context.userid
            },
            "sender_action": "typing_on"
        }
        result = self.send_payload(payload)
        time.sleep(int(seconds))
        payload = {
            "recipient": {
                "id": client_context.userid
            },
            "sender_action": "typing_off"
        }
        return self.send_payload(payload)

    def handle_split(self, client_context):
        print("Handling split...")

    def handle_list(self, client_context, items):
        print("Handling list...")
        payload = {
            "recipient": {
                "id": client_context.userid
            },
            "message": {
                "attachment": {
                    "type": "template",
                    "payload": {
                        "template_type": "list",
                        "top_element_style": "compact",
                        "elements": [
                        ]
                    }
                }
            }
        }

        for item in items:
            print(item)

        return self.send_payload(payload)

    def handle_ordered_list(self, client_context, items):
        print("Handling ordered...")
        payload = {
            "recipient": {
                "id": client_context.userid
            },
            "message": {
                "attachment": {
                    "type": "template",
                    "payload": {
                        "template_type": "list",
                        "top_element_style": "compact",
                        "elements": [
                        ]
                    }
                }
            }
        }

        for item in items:
            print(item)

        return self.send_payload(payload)

    def handle_location(self, client_context):
        print("Handling location...")
        payload = {
            'recipient': {
                'id': client_context.userid
            },
            "message": {
                "text": "Your location",
                "quick_replies": [
                    {
                        "content_type": "location"
                    }
                ]
            }
        }
        return self.send_payload(payload)

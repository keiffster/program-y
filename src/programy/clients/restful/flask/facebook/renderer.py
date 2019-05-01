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
        result = self._client.facebook_bot.send_raw(payload)
        return result

    def handle_text(self, client_context, text):
        YLogger.debug(client_context, "Handling text...")

        payload = {
            'recipient': {
                'id': client_context.userid
            },
            'message': {
                'text': text['text']
            }
        }
        return self.send_payload(payload)

    def handle_url_button(self, client_context, button):
        YLogger.debug(client_context, "Handling url...")

        payload = {
            "recipient": {
                "id": client_context.userid
            },
            "message": {
                "attachment": {
                    "type": "template",
                    "payload": {
                        "template_type": "button",
                        "text": button['text'],
                        "buttons": [
                            {
                                "type": "web_url",
                                "url": button['url'],
                                "title": button['text']
                            }
                        ]
                    }
                }
            }

        }
        return self.send_payload(payload)

    def create_postback_button(self, userid, text, postback):
        return {
            "recipient": {
                "id": userid
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

    def handle_postback_button(self, client_context, button):
        YLogger.debug(client_context, "Handling postback button...")

        payload = self.create_postback_button(client_context.userid, button['text'], button['postback'])
        return self.send_payload(payload)

    def handle_link(self, client_context, link):
        YLogger.debug(client_context, "Handling link...")

        payload = {
            "recipient": {
                "id": client_context.userid
            },
            "message": {
                "attachment": {
                    "type": "template",
                    "payload": {
                        "template_type": "button",
                        "text": link['text'],
                        "buttons": [
                            {
                                "type": "web_url",
                                "title": link['text'],
                                "url": link['url']
                            }
                        ]
                    }
                }
            }
        }
        return self.send_payload(payload)

    def handle_image(self, client_context, image):
        YLogger.debug(client_context, "Handling image...")

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
                                "url": image['url']
                            }
                        ]
                    }
                }
            }
        }
        return self.send_payload(payload)

    def handle_video(self, client_context, video):
        YLogger.debug(client_context, "Handling video...")

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
                                "url": video['url']
                            }
                        ]
                    }
                }
            }
        }
        return self.send_payload(payload)

    def create_card_payload(self, card):
        payload = {
                    "title": card['title'],
                    "image_url": card['image'],
                    "subtitle": card['subtitle'],
                    "buttons": []
                }

        for button in card['buttons']:
            if button['url'] is not None:
                payload['buttons'].append({
                                "type": "web_url",
                                "title": button['text'],
                                "url": button['url']
                            })
            else:
                payload['buttons'].append({
                                "type": "web_url",
                                "title": button['text'],
                                "postback": button['postback']
                            })

        return payload

    def handle_card(self, client_context, card):
        YLogger.debug(client_context, "Handling card...")

        if len(card['buttons']) > 3:
            YLogger.warning(client_context,"More buttons than facebook allows for a card")

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
                        ]
                    }
                }
            }
        }
        payload['message']['attachment']['payload']['elements'].append(self.create_card_payload(card))
        return self.send_payload(payload)

    def handle_carousel(self, client_context, carousel):
        YLogger.debug(client_context, "Handling carousel...")

        if len(carousel['cards']) > 10:
            YLogger.warning(client_context, "More cards than facebook allows for a carousel")

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

        for card in carousel['cards']:

            element = {
                "title": card['title'],
                "image_url": card['image'],
                "subtitle": card['subtitle'],
                "buttons": []
            }

            for button in card['buttons']:
                if button['url'] is not None:
                    element['buttons'].append({
                        "type": "web_url",
                        "title": button['text'],
                        "url": button['url']
                    })
                else:
                    element['buttons'].append({
                        "type": "web_url",
                        "title": button['text'],
                        "postback": button['postback']
                    })

            payload['message']['attachment']['payload']['elements'].append(element)

        return self.send_payload(payload)

    def handle_reply(self, client_context, reply):
        YLogger.debug(client_context, "Handling reply...")

        if reply['postback'] is None:
            payload = self.create_postback_button(client_context.userid, reply['text'], reply['text'])
        else:
            payload = self.create_postback_button(client_context.userid, reply['text'], reply['postback'])
        self.send_payload(payload)

    def handle_delay(self, client_context, delay):
        YLogger.debug(client_context, "Handling delay...")
        payload = {
            "recipient": {
                "id": client_context.userid
            },
            "sender_action": "typing_on"
        }
        result = self.send_payload(payload)
        time.sleep(int(delay['seconds']))
        payload = {
            "recipient": {
                "id": client_context.userid
            },
            "sender_action": "typing_off"
        }
        return self.send_payload(payload)

    def handle_split(self, client_context, split):
        YLogger.debug(client_context, "Handling split...")

    def convert_to_element(self, item):
        if item["type"] == 'card':
            return self.create_card_payload(item)
        return None

    def handle_list(self, client_context, list):
        YLogger.debug(client_context, "Handling list...")
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

        for item in list['items']:
            element = self.convert_to_element(item)
            if element is not None:
                payload["message"]["attachment"]["payload"]["elements"].append(element)

        return self.send_payload(payload)

    def handle_ordered_list(self, client_context, list):
        YLogger.debug(client_context, "Handling ordered...")

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

        for item in list['items']:
            element = self.convert_to_element(item)
            if element is not None:
                payload["message"]["attachment"]["payload"]["elements"].append(element)

        return self.send_payload(payload)

    def handle_location(self, client_context, location):
        YLogger.debug(client_context, "Handling location...")

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

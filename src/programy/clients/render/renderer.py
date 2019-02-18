"""
Copyright (c) 2016-2019 Keith Sterling http://www.keithsterling.com

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated
documentation files (the "Software"), to deal in the Software without restriction, including without limitation
the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software,
and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions
of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO
THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT,
TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
"""
from programy.utils.logging.ylogger import YLogger

from bs4 import BeautifulSoup as Soup
from bs4.element import Tag, NavigableString


class RichMediaRenderer(object):

    def __init__(self, callback):
        self._client = callback

    def render(self, client_context, message):
        if message:
            soup = Soup(message, "lxml-xml")
            parsed = False
            if soup.children:
                    for child in soup.children:
                        if isinstance(child, Tag):
                            return self.parse_tag(client_context, child)

                        elif isinstance(child, NavigableString):
                            return self.parse_text(client_context, child)

                        parsed = True

            if parsed is False:
                return self.parse_text(client_context, message)

        return None

    def parse_tag(self, client_context, tag):

        if tag.name == 'button':
            return self.parse_button(client_context, tag)

        elif tag.name == 'link':
            return self.parse_link(client_context, tag)

        elif tag.name == 'image':
            return self.parse_image(client_context, tag)

        elif tag.name == 'video':
            return self.parse_video(client_context, tag)

        elif tag.name == 'card':
            return self.parse_card(client_context, tag)

        elif tag.name == 'carousel':
            return self.parse_carousel(client_context, tag)

        elif tag.name == 'reply':
            return self.parse_reply(client_context, tag)

        elif tag.name == 'delay':
            return self.parse_delay(client_context, tag)

        elif tag.name == 'split':
            return self.parse_split(client_context, tag)

        elif tag.name == 'list':
            return self.parse_list(client_context, tag)

        elif tag.name == 'olist':
            return self.parse_olist(client_context, tag)

        elif tag.name == 'location':
            return self.parse_location(client_context, tag)

        else:
            return self.parse_xml(client_context, tag)

    def parse_text(self, client_context, text):
        return self.handle_text(client_context, {"type": "text", "text": text})

    def parse_xml(self, client_context, tag):
        text = str(tag)
        return self.handle_text(client_context, {"type": "text", "text": text})

    def extract_button_info(self, tag):
        text = None
        url = None
        postback = None
        for child in tag.children:

            if child.name is None:
                pass

            elif child.name == 'text':
                text = child.text

            elif child.name == 'url':
                url = child.text

            elif child.name == 'postback':
                postback = child.text

            else:
                print("Unknown button tag %s" % child.name)

        return {"type": "button", "text": text, "url": url, "postback": postback}

    def parse_button(self, client_context, tag):
        button = self.extract_button_info(tag)
        if button['url'] is not None:
            return self.handle_url_button(client_context, button)
        else:
            return self.handle_postback_button(client_context, button)

    def extract_link_info(self, tag):
        text = None
        url = None
        for child in tag.children:

            if child.name is None:
                pass

            elif child.name == 'text':
                text = child.text

            elif child.name == 'url':
                url = child.text

            else:
                print("Unknown link tag %s" % child.name)

        return {"type": "link", "text": text, "url": url}

    def parse_link(self, client_context, tag):
        link = self.extract_link_info(tag)
        return self.handle_link(client_context, link)

    def parse_image(self, client_context, tag):
        return self.handle_image(client_context, {"type": "image", "url": tag.text.strip()})

    def parse_video(self, client_context, tag):
        return self.handle_video(client_context, {"type": "video", "url": tag.text.strip()})

    def extract_card_info(self, tag):
        image = None
        title = None
        subtitle = None
        buttons = []

        for child in tag.children:

            if child.name is None:
                pass

            elif child.name == 'image':
                image = child.text

            elif child.name == 'title':
                title = child.text

            elif child.name == 'subtitle':
                subtitle = child.text

            elif child.name == 'button':
                button = self.extract_button_info(child)
                buttons.append(button)

            else:
                print("Unknown card tag [%s]" % child.name)

        return {"type": "card", "image": image, "title": title, "subtitle": subtitle, "buttons": buttons}

    def parse_card(self, client_context, tag):
        card = self.extract_card_info(tag)
        return self.handle_card(client_context, card)

    def extract_carousel_info(self, tag):
        cards = []
        for child in tag.children:

            if child.name is None:
                pass

            elif child.name == 'card':
                card = self.extract_card_info(child)
                cards.append(card)

            else:
                print("Unknown carousel tag %s" % child.name)

        return {"type": "carousel", "cards": cards}

    def parse_carousel(self, client_context, tag):
        carousel = self.extract_carousel_info(tag)
        return self.handle_carousel(client_context, carousel)

    def extract_reply_info(self, tag):
        text = None
        postback = None
        for child in tag.children:

            if child.name is None:
                pass

            elif child.name == 'text':
                text = child.text.strip()

            elif child.name == 'postback':
                postback = child.text.strip()

            else:
                print("Unknown reply tag %s" % child.name)

        return {"type": "reply", "text": text, "postback": postback}

    def parse_reply(self, client_context, tag):
        reply = self.extract_reply_info(tag)
        return self.handle_reply(client_context, reply)

    def extract_delay_info(self, tag):
        seconds = None
        for child in tag.children:

            if child.name is None:
                pass

            elif child.name == 'seconds':
                seconds = child.text.strip()
        return {"type": "delay", "seconds": seconds}

    def parse_delay(self, client_context, tag):
        delay = self.extract_delay_info(tag)
        return self.handle_delay(client_context, delay)

    def parse_split(self, client_context, tag):
        return self.handle_split(client_context, {"type": "split"})

    def extract_item_info(self, tag):

        if tag.name == 'button':
            return self.extract_reply_info(tag)

        elif tag.name == 'link':
            return self.extract_link_info(tag)

        elif tag.name == 'image':
            return {"type": "image", "url": tag.text}

        elif tag.name == 'video':
            return {"type": "video", "url": tag.text}

        elif tag.name == 'card':
            return self.extract_card_info(tag)

        elif tag.name == 'carousel':
            return self.extract_carousel_info(tag)

        elif tag.name == 'reply':
            return self.extract_reply_info(tag)

        elif tag.name == 'delay':
            return self.extract_delay_info(tag)

        elif tag.name == 'split':
            # Not allowed
            pass

        elif tag.name == 'list':
            return self.extract_list_info(tag)

        elif tag.name == 'olist':
            return self.extract_list_info(tag)

        elif tag.name == 'location':
            # Not allowed
            pass

        else:
            if isinstance(tag, Tag):
                text = tag.text

            elif isinstance(tag, NavigableString):
                text = tag

            return {"type": "text", "text": text}

    def extract_list_info(self, tag):
        items = []

        for child in tag.children:

            if child.name is None:
                pass

            elif child.name == 'item':

                for childs_child in child.children:

                    if isinstance(childs_child, Tag):
                        items.append(self.extract_item_info(childs_child))

                    elif isinstance(childs_child, NavigableString):
                        childs_child_text = childs_child.strip()
                        if childs_child_text:
                            items.append({'type': 'text', 'text': childs_child_text})

            else:
                print("Unknown list tag %s" % child.name)

        return {'type': 'list', 'items': items}

    def parse_list(self, client_context, tag):
        list = self.extract_list_info(tag)
        return self.handle_list(client_context, list)

    def parse_olist(self, client_context, tag):
        list = self.extract_list_info(tag)
        return self.handle_ordered_list(client_context, list)

    def parse_location(self, client_context, tag):
        return self.handle_location(client_context, {"type": "location"})

    ######################################################################################################
    # You need to implement all of these and decide how to display the various rich media elements
    # 
    def handle_text(self, client_context, text):
        return None

    def handle_url_button(self, client_context, button):
        return None

    def handle_postback_button(self, client_context, button):
        return None

    def handle_link(self, client_context, link):
        return None

    def handle_image(self, client_context, image):
        return None

    def handle_video(self, client_context, image):
        return None

    def handle_card(self, client_context, card):
        return None

    def handle_carousel(self, client_context, carousel):
        return None

    def handle_reply(self, client_context, reply):
        return None

    def handle_delay(self, client_context, delay):
        return None

    def handle_split(self, client_contex, split):
        return None

    def handle_list(self, client_context, list):
        return None

    def handle_ordered_list(self, client_context, list):
        return None

    def handle_location(self, client_context, location):
        return None

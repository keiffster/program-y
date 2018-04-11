"""
Copyright (c) 2016-2018 Keith Sterling http://www.keithsterling.com

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
        return self.handle_text(client_context, text)

    def parse_xml(self, client_context, tag):
        text = str(tag)
        return self.handle_text(client_context, text)

    def parse_button(self, client_context, tag):
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

        if url is not None:
            return self.handle_url_button(client_context, text, url)
        else:
            return self.handle_postback_button(client_context, text, postback)

    def parse_link(self, client_context, tag):
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

        return self.handle_link(client_context, text, url)

    def parse_image(self, client_context, tag):
        return self.handle_image(client_context, tag.text)

    def parse_video(self, client_context, tag):
        return self.handle_video(client_context, tag.text)

    def _parse_card_details(self, tag):
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
                text = None
                url = None
                postback = None
                for button_child in child:
                    if button_child.name is None:
                        pass

                    elif button_child.name == 'text':
                        text = button_child.text

                    elif button_child.name == 'url':
                        url = button_child.text

                    elif button_child.name == 'postback':
                        postback = button_child.text

                    else:
                        print("Unknown button child tag %s" % child.name)

                buttons.append((text, url, postback))
            else:
                print("Unknown card tag [%s]" % child.name)

        return (image, title, subtitle, buttons)

    def parse_card(self, client_context, tag):

        details = self._parse_card_details(tag)

        image = details[0]
        title = details[1]
        subtitle = details[2]
        buttons = details[3]

        return self.handle_card(client_context, image, title, subtitle, buttons)

    def parse_carousel(self, client_context, tag):

        cards = []
        for child in tag.children:

            if child.name is None:
                pass

            elif child.name == 'card':
                details = self._parse_card_details(child)
                cards.append(details)

            else:
                print("Unknown carousel tag %s" % child.name)

        return self.handle_carousel(client_context, cards)

    def parse_reply(self, client_context, tag):
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

        return self.handle_reply(client_context, text, postback)

    def parse_delay(self, client_context, tag):
        seconds = None
        for child in tag.children:

            if child.name is None:
                pass

            elif child.name == 'seconds':
                seconds = child.text.strip()

        return self.handle_delay(client_context, seconds)

    def parse_split(self, client_context, tag):
        return self.handle_split(client_context)

    def parse_list_items(self, client_context, tag):
        items = []

        for child in tag.children:

            if child.name is None:
                pass

            elif child.name == 'item':
                for child2 in child.children:

                    if isinstance(child2, Tag):
                        parsed = self.parse_tag(client_context, child2)
                        items.append(parsed)

                    elif isinstance(child2, NavigableString):
                        text = child2.strip()
                        if text:
                            parsed = self.parse_text(client_context, child2)
                            items.append(parsed.strip())

            else:
                print("Unknown list tag %s" % child.name)

        return items

    def parse_list(self, client_context, tag):
        items = self.parse_list_items(client_context, tag)
        return self.handle_list(client_context, items)

    def parse_olist(self, client_context, tag):
        items = self.parse_list_items(client_context, tag)
        return self.handle_ordered_list(client_context, items)

    def parse_location(self, client_context, tag):
        return self.handle_location(client_context)

    ######################################################################################################
    # You need to implement all of these and decide how to display the various rich media elements
    # 
    def handle_text(self, client_context, text):
        return None

    def handle_url_button(self, client_context, text, url):
        return None

    def handle_postback_button(self, client_context, text, postback):
        return None

    def handle_link(self, client_context, text, url):
        return None

    def handle_image(self, client_context, url):
        return None

    def handle_video(self, client_context, url):
        return None

    def handle_card(self, client_context, image, title, subtitle, buttons):
        return None

    def handle_carousel(self, client_context, cards):
        return None

    def handle_reply(self, client_context, text, postback):
        return None

    def handle_delay(self, client_context, seconds):
        return None

    def handle_split(self, client_context):
        return None

    def handle_list(self, client_context, items):
        return None

    def handle_ordered_list(self, client_context, items):
        return None

    def handle_location(self, client_context):
        return None

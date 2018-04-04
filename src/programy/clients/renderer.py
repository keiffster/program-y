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

    def __init__(self, config):
        self._config = config

    def send_message(self, userid, message):
        soup = Soup(message, "html.parser")
        for child in soup.children:

            if isinstance(child, Tag):
                self.parse_tag(userid, child)

            elif isinstance(child, NavigableString):
                self.parse_text(userid, child)

    def parse_tag(self, userid, tag):

        if tag.name == 'button':
            return self.parse_button(userid, tag)

        elif tag.name == 'link':
            return self.parse_link(userid, tag)

        elif tag.name == 'image':
            return self.parse_image(userid, tag)

        elif tag.name == 'video':
            return self.parse_video(userid, tag)

        elif tag.name == 'card':
            return self.parse_card(userid, tag)

        elif tag.name == 'carousel':
            return self.parse_carousel(userid, tag)

        elif tag.name == 'reply':
            return self.parse_reply(userid, tag)

        elif tag.name == 'delay':
            return self.parse_delay(userid, tag)

        elif tag.name == 'split':
            return self.parse_split(userid, tag)

        elif tag.name == 'list':
            return self.parse_list(userid, tag)

        elif tag.name == 'olist':
            return self.parse_olist(userid, tag)

        elif tag.name == 'location':
            return self.parse_location(userid, tag)

        else:
            print("Unknown tag %s".tag.name)
            return None

    def parse_text(self, userid, text):
        self.handle_text(userid, text)

    def parse_button(self, userid, tag):
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
            self.handle_url_button(userid, text, url)
        else:
            self.handle_postback_button(userid, text, postback)

    def parse_link(self, userid, tag):
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

        self.handle_link(userid, text, url)

    def parse_image(self, userid, tag):
        self.handle_image(userid, tag.text)

    def parse_video(self, userid, tag):
        self.handle_video(userid, tag.text)

    def parse_card(self, userid, tag):
        image = None
        title = None
        substitle = None
        buttons = []

        for child in tag.children:

            if child.name is None:
                pass

            elif child.name == 'image':
                image = self.parse_image(child)

            elif child.name == 'title':
                title = child.text

            elif child.name == 'subtitle':
                subtitle = child.text

            elif child.text == 'button':
                buttons.append(self.parse_button(child))

            else:
                print("Unknown card tag %s" % child.name)

        self.handle_card(userid, image, title, substitle, buttons)

    def parse_carousel(self, userid, tag):

        cards = []
        for child in tag.children:

            if child.name is None:
                pass

            elif child.name == 'card':
                cards.append(self.parse_card(child))

            else:
                print("Unknown carousel tag %s" % child.name)

        self.handle_carousel(userid, cards)

    def parse_reply(self, userid, tag):
        text = None
        postback = None
        for child in tag.children:

            if child.name is None:
                pass

            elif child.name == 'text':
                text = child.text

            elif child.name == 'postback':
                postback = child.text

            else:
                print("Unknown reply tag %s" % child.name)

        self.handle_reply(userid, text, postback)

    def parse_delay(self, userid, tag):
        seconds = None
        for child in tag.children:

            if child.name is None:
                pass

            elif child.name == 'seconds':
                seconds = child.text

        self.handle_delay(userid, seconds)

    def parse_split(self, userid, tag):
        self.handle_split()

    def parse_list(self, userid, tag):
        items = []
        for child in tag.children:

            if child.name is None:
                pass

            elif child.name == 'item':
                items.append(child.text)

            else:
                print("Unknown list tag %s" % child.name)

        self.handle_list(userid, items)

    def parse_olist(self, userid, tag):
        items = []
        for child in tag.children:

            if child.name is None:
                pass

            elif child.name == 'item':
                items.append(child.text)

            else:
                print("Unknown olist tag %s" % child.name)

        self.handle_ordered_list(items)

    def parse_location(self, userid, tag):
        self.handle_location(userid)

    ######################################################################################################
    # You need to implement all of these and decide how to display the various rich media elements
    # 
    def handle_text(self, userid, text):
        pass

    def handle_url_button(self, userid, text, url):
        pass

    def handle_postback_button(self, userid, text, postback):
        pass

    def handle_link(self, userid, text, url):
        pass

    def handle_image(self, userid, url):
        pass

    def handle_video(self, userid, url):
        pass

    def handle_card(self, userid, image, title, substitle, buttons):
        pass

    def handle_carousel(self, userid, cards):
        pass

    def handle_reply(self, userid, text, postback):
        pass

    def handle_delay(self, userid, seconds):
        pass

    def handle_split(self):
        pass

    def handle_list(self, userid, items):
        pass

    def handle_ordered_list(self, userid, items):
        pass

    def handle_location(self, userid):
        pass

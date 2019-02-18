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

import re
import os

class TextUtils:

    DEFAULT_TAB_SPACE = "  "

    RE_STRIP_ALL_WHITESPACE = re.compile('[\s+]')
    RE_STRIP_WHITESPACE = re.compile('[\n\t\r+]')
    RE_TERMIANTORS = re.compile('[:;,.?!]')
    RE_STRIP_NONE_TERMINATING = re.compile('[\'"\(\)\-"]')
    RE_STRIP_ALL_PUNCTUATION1 = re.compile('[:\'";,.?!\(\)\-"]')
    RE_STRIP_ALL_PUNCTUATION2 = re.compile('\s+')
    RE_STRIP_HTML = re.compile(r'<.*?>')
    RE_PATTERN_OF_TAG_AND_NAMESPACE_FROM_TEXT = re.compile("^{.*}.*$")
    RE_MATCH_OF_TAG_AND_NAMESPACE_FROM_TEXT = re.compile("^({.*})(.*)$")

    HTML_ESCAPE_TABLE = {
        "&": "&amp;",
        '"': "&quot;",
        "'": "&apos;",
        ">": "&gt;",
        "<": "&lt;",
    }

    @staticmethod
    def get_tabs(depth: int, tabs=DEFAULT_TAB_SPACE):
        return tabs * depth

    @staticmethod
    def strip_whitespace(string):
        first_pass = TextUtils.RE_STRIP_WHITESPACE.sub(' ', string)
        return ' '.join(first_pass.split())

    @staticmethod
    def strip_all_whitespace(string):
        first_pass = TextUtils.RE_STRIP_ALL_WHITESPACE.sub('', string)
        return ' '.join(first_pass.split())

    @staticmethod
    def strip_none_terminating_punctuation(string):
        first_pass = TextUtils.RE_STRIP_NONE_TERMINATING.sub(' ', string)
        second_pass = TextUtils.RE_STRIP_NONE_TERMINATING.sub(' ', first_pass)
        return second_pass.strip()

    @staticmethod
    def strip_all_punctuation(string):
        first_pass = TextUtils.RE_STRIP_ALL_PUNCTUATION1.sub(' ', string)
        second_pass = TextUtils.RE_STRIP_ALL_PUNCTUATION2.sub(' ', first_pass)
        return second_pass.strip()

    @staticmethod
    def urlify(string):
        return string.replace(" ", "%20")

    @staticmethod
    def strip_html(data, replace_with=''):
        return TextUtils.RE_STRIP_HTML.sub(replace_with, data)

    @staticmethod
    def replace_path_seperator(path, old="/", new=os.sep):
        if old in path:
            return path.replace(old, new)
        return path

    @staticmethod
    def tag_and_namespace_from_text(text):
        # If there is a namespace, then it looks something like
        # {http://alicebot.org/2001/AIML}aiml
        if TextUtils.RE_PATTERN_OF_TAG_AND_NAMESPACE_FROM_TEXT.match(text) is None:
            # If that pattern does not exist, assume that the text is the tag name
            return text, None

        # Otherwise, extract namespace and tag name
        groupings = TextUtils.RE_MATCH_OF_TAG_AND_NAMESPACE_FROM_TEXT.match(text)
        if groupings is not None:
            namespace = groupings.group(1).strip()
            tag_name = groupings.group(2).strip()
            return tag_name, namespace
        return None, None

    @staticmethod
    def tag_from_text(text):
        tag, _ = TextUtils.tag_and_namespace_from_text(text)
        return tag

    @staticmethod
    def html_escape(text):
        return "".join(TextUtils.HTML_ESCAPE_TABLE.get(c, c) for c in text)

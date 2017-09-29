"""
Copyright (c) 2016-17 Keith Sterling http://www.keithsterling.com

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

    STRIP_ALL_WHITESPACE = r'[\s+]'
    STRIP_WHITESPACE = r'[\n\t\r+]'
    STRIP_ALL_PUNCTUATION = r'[:\'";,.?!\(\)\-"]'

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
        first_pass = re.sub(TextUtils.STRIP_WHITESPACE, ' ', string)
        return ' '.join(first_pass.split())

    @staticmethod
    def strip_all_whitespace(string):
        first_pass = re.sub(TextUtils.STRIP_ALL_WHITESPACE, '', string)
        return ' '.join(first_pass.split())

    @staticmethod
    def strip_all_punctuation(string):
        first_pass = re.sub(TextUtils.STRIP_ALL_PUNCTUATION, ' ', string)
        second_pass = re.sub(r'\s+', ' ', first_pass)
        return second_pass.strip()

    @staticmethod
    def urlify(string):
        return string.replace(" ", "%20")

    @staticmethod
    def strip_html(data, replace_with=''):
        pattern = re.compile(r'<.*?>')
        return pattern.sub(replace_with, data)

    @staticmethod
    def replace_path_seperator(path, old="/", new=os.sep):
        if old in path:
            return path.replace(old, new)
        return path

    @staticmethod
    def tag_and_namespace_from_text(text):
        # If there is a namespace, then it looks something like
        # {http://alicebot.org/2001/AIML}aiml
        pattern = re.compile("^{.*}.*$")
        if pattern.match(text) is None:
            # If that pattern does not exist, assume that the text is the tag name
            return text, None

        # Otherwise, extract namespace and tag name
        match = re.compile("^({.*})(.*)$")
        groupings = match.match(text)
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

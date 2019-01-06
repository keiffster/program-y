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
from programy.dialog.tokenizer.tokenizer import Tokenizer


class CjkTokenizer(Tokenizer):

    def __init__(self, split_chars=' '):
        Tokenizer.__init__(self, split_chars)

    @staticmethod
    def _is_chinese_word(word):
        if word is None:
            return False
        else:
            for ch in word:
                if CjkTokenizer._is_chinese_char(ch):
                    return True
            return False

    @staticmethod
    def _is_chinese_char(c):
        r = [
            # 标准CJK文字
            (0x3400, 0x4DB5), (0x4E00, 0x9FA5), (0x9FA6, 0x9FBB), (0xF900, 0xFA2D),
            (0xFA30, 0xFA6A), (0xFA70, 0xFAD9), (0x20000, 0x2A6D6), (0x2F800, 0x2FA1D),
            # 全角ASCII、全角中英文标点、半宽片假名、半宽平假名、半宽韩文字母
            (0xFF00, 0xFFEF),
            # CJK部首补充
            (0x2E80, 0x2EFF),
            # CJK标点符号
            (0x3000, 0x303F),
            # CJK笔划
            (0x31C0, 0x31EF)]
        return any(s <= ord(c) <= e for s, e in r)

    def _is_wildchar(self, ch):
        MATCH_CHARS = ['^', '#', '', '*']
        return bool(ch in MATCH_CHARS)

    def texts_to_words(self, texts):
        if not texts:
            return []

        words = []
        last_word = ''
        for ch in texts:
            if CjkTokenizer._is_chinese_char(ch):
                if len(last_word) > 0:
                    words.append(last_word)
                    last_word = ''
                words.append(ch)
            elif ch == self.split_chars:
                if len(last_word) > 0:
                    words.append(last_word)
                    last_word = ''
            else:
                if self._is_wildchar(ch):
                    if len(last_word) > 0:
                        words.append(last_word)
                        last_word = ''
                    words.append(ch)
                else:
                    last_word += ch

        if len(last_word) > 0:
            words.append(last_word)

        return words

    def words_to_texts(self, words):
        texts = ''

        if words is None:
            words = ''

        for word in words:
            if CjkTokenizer._is_chinese_word(word):
                texts += word
            elif len(texts) > 0:
                texts += ' ' + word
            elif word is None:
                pass
            else:
                texts += word

        texts = re.sub(r'\s+', ' ', texts)
        stripped_text = texts.strip()
        return stripped_text

    def words_from_current_pos(self, words, current_pos):
        if words:
            return self.words_to_texts(words[current_pos:])
        raise Exception("Num word array violation !")

    def compare(self, value1, value2):
        cjk_value1 = self.words_to_texts(self.texts_to_words(value1.upper()))
        cjk_value2 = self.words_to_texts(self.texts_to_words(value2.upper()))
        return cjk_value1 == cjk_value2


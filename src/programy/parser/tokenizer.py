import re

class Tokenizer(object):
    def __init__(self, split_chars=' '):
        self.split_chars = split_chars

    def texts_to_words(self, texts):
        if not texts:
            return []
        return [word.strip() for word in texts.split(self.split_chars) if word]

    def words_to_texts(self, words):
        if not words:
            return ''
        to_join = [word.strip() for word in words if word]
        return self.split_chars.join(to_join)

    def words_from_current_pos(self, words, current_pos):
        if not words:
            return ''
        return self.split_chars.join(words[current_pos:])

    def compare(self, value1, value2):
        return value1 == value2

class CjkTokenizer(Tokenizer):
    def __init__(self, split_chars=' '):
        self.split_chars = split_chars

    def _is_chinese_word(self, word):
        for ch in word:
            if self._is_chinese_char(ch):
                return True
        return False

    def _is_chinese_char(self, c):
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

    def texts_to_words(self, texts):
        if not texts:
            return []

        words = []
        last_word = ''
        for ch in texts:
            if self._is_chinese_char(ch):
                if len(last_word) > 0:
                    words.append(last_word)
                    last_word = ch
                else:
                    words.append(ch)
            else:
                if ch == self.split_chars:
                    if len(last_word) > 0:
                        words.append(last_word)
                        last_word = ''
                else:
                    last_word += ch

        if len(last_word) > 0:
            words.append(last_word)

        return words
    
    def words_to_texts(self, words):
        texts = ''
        prev_is_cjk = True
        prev_is_num = False

        for word in words:
            if self._is_chinese_word(word):
                if prev_is_cjk == False:
                    if prev_is_num is False:
                        texts += ' '
                texts += word
                prev_is_cjk = True
            elif len(texts) > 0:
                texts += ' ' + word
                prev_is_cjk = False
            else:
                texts += word
                prev_is_cjk = False
            prev_is_num = word.isdigit()

        texts = re.sub(r'\s+', ' ', texts)
        return texts.strip()

    def words_from_current_pos(self, words, current_pos):
        if words:
            return self.words_to_texts(words[current_pos:])
        raise Exception("Num word array violation !")

    def compare(self, value1, value2):
        cjk_value1 = self.words_to_texts(self.texts_to_words(value1.upper()))
        cjk_value2 = self.words_to_texts(self.texts_to_words(value2.upper()))
        return cjk_value1 == cjk_value2

DEFAULT_TOKENIZER = Tokenizer()


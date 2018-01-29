
class Tokenizer(object):
    def __init__(self, split_chars=' '):
        self.split_chars = split_chars

    def texts_to_words(self, texts):
        if not texts:
            return []
        return texts.split(self.split_chars)

    def words_to_texts(self, words):
        if not words:
            return ''
        return self.split_chars.join(words)

    def words_from_current_pos(self, words, current_pos):
        if not words:
            return ''
        return self.split_chars.join(words[current_pos:])

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
            (0x3400, 0x4DB5), (0x4E00, 0x9FA5), (0x9FA6, 0x9FBB), (0xF900, 0xFA2D),
            (0xFA30, 0xFA6A), (0xFA70, 0xFAD9), (0x20000, 0x2A6D6), (0x2F800, 0x2FA1D),
            (0xFF00, 0xFFEF),
            (0x2E80, 0x2EFF),
            (0x3000, 0x303F),
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
                    last_word = ''
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
            last_word = ''

        return words
    
    def words_to_texts(self, words):
        texts = ''
        
        for word in words:
            if self._is_chinese_word(word):
                texts += word
            elif len(texts) > 0:
                texts += self.split_chars + word
            else:
                texts += word
        return texts

    def words_from_current_pos(self, words, current_pos):
        if words:
            return self.words_to_texts(words[current_pos:])
        raise Exception("Num word array violation !")

DEFAULT_TOKENIZER = Tokenizer()


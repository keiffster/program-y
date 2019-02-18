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

from programy.utils.logging.ylogger import YLogger
from programy.processors.processing import PostProcessor


class TranslatorPostProcessor(PostProcessor):

    def __init__(self):
        PostProcessor.__init__(self)

    def process(self, context, word_string):
        translator_config = context.bot.configuration.to_translator
        translator = context.bot.to_translator

        try:
            if translator is not None:
                trans_string = translator.translate(word_string,
                                            from_lang=translator_config.from_lang,
                                            to_lang=translator_config.to_lang)

                YLogger.debug(context, "Post translated [%s](%s) to [%s](%s)", word_string, translator_config.from_lang, trans_string, translator_config.to_lang)
                return trans_string

        except Exception as e:
            YLogger.exception(context, "Failed to translate [%s] from [%s] to [%s]", e, word_string,
                              translator_config.from_lang, translator_config.to_lang)

        return word_string

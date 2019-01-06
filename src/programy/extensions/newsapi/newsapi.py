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

from programy.utils.newsapi.newsapi import NewsAPI
from programy.extensions.base import Extension


class NewsAPIExtension(Extension):

    def get_news_api_api(self, context):
        return  NewsAPI(context.client.license_keys)

    def get_news(self, context, source, max_num, sort, reverse):

        newsapi = self.get_news_api_api(context)

        headlines = newsapi.get_headlines(source, max_num, sort, reverse)
        if headlines is None:
            YLogger.error(context, "NewsAPIExtension no headlines found!")
            return ""

        results = newsapi.to_program_y_text(headlines)
        if results is None:
            YLogger.error(context, "NewsAPIExtension no results returned!")
            return ""

        return results

    def parse_data(self, context, data):
        source = None
        max_num = 10
        sort = False
        reverse = False

        splits = data.split()
        count = 0
        while count < len(splits):
            if splits[count] == "SOURCE":
                count += 1
                source = splits[count]
            elif splits[count] == "MAX":
                count += 1
                max_num = int(splits[count])
            elif splits[count] == "SORT":
                count += 1
                if splits[count].upper() == 'TRUE':
                    sort = True
                elif splits[count].upper() == 'FALSE':
                    sort = False
                else:
                    YLogger.error(context, "Invalid value for NewAPI Data parameter sort [%s]", splits[count])
                    sort = False
            elif splits[count] == "REVERSE":
                count += 1
                if splits[count].upper() == 'TRUE':
                    reverse = True
                elif splits[count].upper() == 'FALSE':
                    reverse = False
                else:
                    YLogger.error(context, "Invalid value for NewAPI Data parameter reverse [%s]", splits[count])
                    reverse = False
            else:
                YLogger.error(context, "Unknown News API Command [%s]", splits[count])

            count += 1

        return source, max_num, sort, reverse

    # execute() is the interface that is called from the <extension> tag in the AIML
    def execute(self, context, data):

        source, max_num, sort, reverse = self.parse_data(context, data)

        if source is None:
            YLogger.error(context, "NewsAPIExtension no source passed in as data parameter!")
            return ""

        return self.get_news(context, source, max_num, sort, reverse)

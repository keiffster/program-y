import os

from programy.utils.license.keys import LicenseKeys
from programy.utils.newsapi.newsapi import NewsAPI

if __name__ == '__main__':

    # Running these tools drops test files into the newapi test folder

    app_license_keys = LicenseKeys()
    app_license_keys.load_license_key_file(os.path.dirname(__file__) + '/../../../../bots/y-bot/config/license.keys')

    news_api = NewsAPI(app_license_keys)

    results = news_api.get_headlines(NewsAPI.BBC_NEWS)

    json_data = NewsAPI.to_json(results)

    NewsAPI.json_to_file('../../../test/utils/newsapi/newsapi.json', json_data)

    # Running these tools drops test files into the geocode test folder

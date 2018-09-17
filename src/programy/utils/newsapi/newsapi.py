from programy.utils.logging.ylogger import YLogger
import json
import requests

class NewsApiApi(object):

    def get_news(self, url):
        return  requests.get(url)

class NewsArticle(object):

    def __init__(self):
        self.title = None
        self.description = None
        self.published_at = None
        self.author = None
        self.url = None
        self.url_to_image = None

    def _get_json_attribute(self, data, name, def_value=None):
        if name in data:
            return data[name]
        else:
            YLogger.debug(self, "Attribute [%s] missing from New API Article data", name)
            return def_value

    def parse_json(self, data):
        self.title = self._get_json_attribute(data, "title")
        self.description = self._get_json_attribute(data, "description")
        self.published_at = self._get_json_attribute(data, "publishedAt")
        self.author = self._get_json_attribute(data, "author")
        self.url = self._get_json_attribute(data, "url")
        self.url_to_image = self._get_json_attribute(data, "urlToImage")

    def to_json(self):
        data = {}
        data["title"] = self.title
        data["description"] = self.description
        data["publishedAt"] = self.published_at
        data["author"] = self.author
        data["url"] = self.url
        data["urlToImage"] = self.url_to_image
        return data

# https://newsapi.org/bbc-news-api

class NewsAPI(object):

    BASE_URL = "https://newsapi.org/v1/articles?source=%s&sortBy=%s&apiKey=%s"

    # Single news feeds
    ABC_NEWS_AU = "abc-news-au"
    AL_JAZEERA_ENGLISH = "al-jazeera-english"
    ARS_TECHNICA = "ars-technica"
    ASSOCIATED_PRESS = "associated-press"
    BBC_NEWS = "bbc-news"
    BBC_SPORT = "bbc-sport"
    BLOOMBERG = "bloomberg"
    BUSINESS_INSIDER = "business-insider"
    BUSINESS_INSIDER_UK = "business-insider-uk"
    BUZZFEED = "buzzfeed"
    CNBC = "cnbc"
    CNN = "cnn"
    DAILY_MAIL = "daily-mail"
    ENGADGET = "engadget"
    ENTERTAINMENT_WEEKLY = "entertainment-weekly"
    ESPN = "espn"
    ESPN_CRIC_INFO = "espn-cric-info"
    FINANCIAL_TIMES = "financial-times"
    FOOTBALL_ITALIA = "football-italia"
    FORTUNE = "fortune"
    FOUR_FOUR_TWO = "four-four-two"
    FOX_SPORTS = "fox-sports"
    GOOGLE_NEWS = "google-news"
    HACKER_NEWS = "hacker-news"
    IGN = "ign"
    INDEPENDENT = "independent"
    MASHABLE = "mashable"
    METRO = "metro"
    MIRROR = "mirror"
    MTV_NEWS = "mtv-news"
    MTV_NEWS_UK = "mtv-news-uk"
    NATIONAL_GEOGRAPHIC = "national-geographic"
    NEW_SCIENTIST = "new-scientist"
    NEWSWEEK = "newsweek"
    NEW_YORK_MAGAZINE = "new-york-magazine"
    NFL_NEWS = "nfl-news"
    POLYGON = "polygon"
    RECODE = "recode"
    REDDIT_R_ALL = "reddit-r-all"
    REUTERS = "reuters"
    TALKSPORT = "talksport"
    TECHCRUNCH = "techcrunch"
    TECHRADAR = "techradar"
    THE_ECONOMIST = "the-economist"
    THE_GUARDIAN_AU = "the-guardian-au"
    THE_GUARDIAN_UK = "the-guardian-uk"
    THE_HUFFINGTON_POST = "the-huffington-post"
    THE_NEW_YORK_TIMES = "the-new-york-times"
    THE_NEXT_WEB = "the-next-web"
    THE_SPORT_BIBLE = "the-sport-bible"
    THE_TELEGRAPH = "the-telegraph"
    THE_VERGE = "the-verge"
    THE_WALL_STREET_JOURNAL = "the-wall-street-journal"
    THE_WASHINGTON_POST = "the-washington-post"
    TIME = "time"
    USA_TODAY = "usa-today"

    # Collections
    BUSINESS = "business"
    ENTERTAINMENT = " entertainment"
    GAMING = "gaming"
    MUSIC = "music"
    SCIENCE_AND_NATURE = "science_and_nature"
    SPORT = "sport"
    TECHNOLOGY = "technology"
    UK_NEWS = "uk_news"
    UK_NEWSPAPERS = "uk_newspapers"

    def __init__(self, license_keys, news_api_api=None):

        if news_api_api is None:
            NewsAPI._news_api_api = NewsApiApi()
        else:
            NewsAPI._news_api_api = news_api_api

        self.function_mapping = {
            NewsAPI.ABC_NEWS_AU: NewsAPI.abc_news_au,
            NewsAPI.AL_JAZEERA_ENGLISH: NewsAPI.al_jazeera_english,
            NewsAPI.ARS_TECHNICA: NewsAPI.ars_technica,
            NewsAPI.ASSOCIATED_PRESS: NewsAPI.associated_press,
            NewsAPI.BBC_NEWS: NewsAPI.bbc_news,
            NewsAPI.BBC_SPORT: NewsAPI.bbc_sport,
            NewsAPI.BLOOMBERG: NewsAPI.bloomberg,
            NewsAPI.BUSINESS_INSIDER: NewsAPI.business_insider,
            NewsAPI.BUSINESS_INSIDER_UK: NewsAPI.business_insider_uk,
            NewsAPI.BUZZFEED: NewsAPI.buzzfeed,
            NewsAPI.CNBC: NewsAPI.cnbc,
            NewsAPI.CNN: NewsAPI.cnn,
            NewsAPI.DAILY_MAIL: NewsAPI.daily_mail,
            NewsAPI.ENGADGET: NewsAPI.engadget,
            NewsAPI.ENTERTAINMENT_WEEKLY: NewsAPI.entertainment_weekly,
            NewsAPI.ESPN: NewsAPI.espn,
            NewsAPI.ESPN_CRIC_INFO: NewsAPI.espn_cric_info,
            NewsAPI.FINANCIAL_TIMES: NewsAPI.financial_times,
            NewsAPI.FOOTBALL_ITALIA: NewsAPI.football_italia,
            NewsAPI.FORTUNE: NewsAPI.fortune,
            NewsAPI.FOUR_FOUR_TWO: NewsAPI.four_four_two,
            NewsAPI.FOX_SPORTS: NewsAPI.fox_sports,
            NewsAPI.GOOGLE_NEWS: NewsAPI.google_news,
            NewsAPI.HACKER_NEWS: NewsAPI.hacker_news,
            NewsAPI.IGN: NewsAPI.ign,
            NewsAPI.INDEPENDENT: NewsAPI.independent,
            NewsAPI.MASHABLE: NewsAPI.mashable,
            NewsAPI.METRO: NewsAPI.metro,
            NewsAPI.MIRROR: NewsAPI.mirror,
            NewsAPI.MTV_NEWS: NewsAPI.mtv_news,
            NewsAPI.MTV_NEWS_UK: NewsAPI.mtv_news_uk,
            NewsAPI.NATIONAL_GEOGRAPHIC: NewsAPI.national_geographic,
            NewsAPI.NEW_SCIENTIST: NewsAPI.new_scientist,
            NewsAPI.NEWSWEEK: NewsAPI.newsweek,
            NewsAPI.NEW_YORK_MAGAZINE: NewsAPI.new_york_magazine,
            NewsAPI.NFL_NEWS: NewsAPI.nfl_news,
            NewsAPI.POLYGON: NewsAPI.polygon,
            NewsAPI.RECODE: NewsAPI.recode,
            NewsAPI.REDDIT_R_ALL: NewsAPI.reddit,
            NewsAPI.REUTERS: NewsAPI.reuters,
            NewsAPI.TALKSPORT: NewsAPI.talksport,
            NewsAPI.TECHCRUNCH: NewsAPI.techcrunch,
            NewsAPI.TECHRADAR: NewsAPI.techradar,
            NewsAPI.THE_ECONOMIST: NewsAPI.the_economist,
            NewsAPI.THE_GUARDIAN_AU: NewsAPI.the_guardian_au,
            NewsAPI.THE_GUARDIAN_UK: NewsAPI.the_guardian_uk,
            NewsAPI.THE_HUFFINGTON_POST: NewsAPI.the_huffington_post,
            NewsAPI.THE_NEW_YORK_TIMES: NewsAPI.the_new_york_times,
            NewsAPI.THE_NEXT_WEB: NewsAPI.the_next_web,
            NewsAPI.THE_SPORT_BIBLE: NewsAPI.the_sport_bible,
            NewsAPI.THE_TELEGRAPH: NewsAPI.the_telegraph,
            NewsAPI.THE_VERGE: NewsAPI.the_verge,
            NewsAPI.THE_WALL_STREET_JOURNAL: NewsAPI.the_wall_street_journal,
            NewsAPI.THE_WASHINGTON_POST: NewsAPI.the_washington_post,
            NewsAPI.TIME: NewsAPI.time,
            NewsAPI.USA_TODAY: NewsAPI.usa_today,
            NewsAPI.BUSINESS: NewsAPI.business,
            NewsAPI.ENTERTAINMENT: NewsAPI. entertainment,
            NewsAPI.GAMING: NewsAPI.gaming,
            NewsAPI.MUSIC: NewsAPI.music,
            NewsAPI.SCIENCE_AND_NATURE: NewsAPI.science_and_nature,
            NewsAPI.SPORT: NewsAPI.sport,
            NewsAPI.TECHNOLOGY: NewsAPI.technology,
            NewsAPI.UK_NEWS: NewsAPI.uk_news,
            NewsAPI.UK_NEWSPAPERS: NewsAPI.uk_newspapers,
        }

        if license_keys is None:
            raise Exception("Missing license keys")

        if license_keys.has_key('NEWSAPI_API_KEY'):
            self.api_key = license_keys.get_key('NEWSAPI_API_KEY')
        else:
            raise Exception("No valid license key NEWSAPI_API_KEY found")

    @staticmethod
    def _format_url(service, api_key, sort_by="top"):
        return NewsAPI.BASE_URL%(service, sort_by, api_key)

    @staticmethod
    def _get_data(url_str, api_key, max_articles, sort, reverse):
        url = NewsAPI._format_url(url_str, api_key)
        return NewsAPI._get_news_feed_articles(url, max_articles, sort, reverse)

    @staticmethod
    def _get_news_feed_articles(url, max_articles, sort, reverse):
        YLogger.debug(None, "News API URL: [%s]", url)
        response = NewsAPI._news_api_api.get_news(url)
        articles = []
        if response.status_code == 200:
            header_splits = response.headers['content-type'].split(";")
            if header_splits[0] == 'application/json':
                json_data = response.json()
                if 'articles' in json_data:
                    for article_data in json_data['articles']:
                        article = NewsArticle()
                        article.parse_json(article_data)
                        articles.append(article)
                        YLogger.debug(None, article.description)

                    if sort is True:
                        YLogger.debug(None, "Sorting articles,, reverse=%s", str(reverse))
                        articles.sort(key=lambda article: article.published_at, reverse=reverse)

                    if max_articles != 0:
                        YLogger.debug(None, "Returning max_articles %d articles", max_articles)
                        articles = articles[:max_articles]
                    else:
                        YLogger.debug(None, "Returning all articles")
                else:
                    YLogger.error(None, "NewAPI payload contains no articles attribute")
            else:
                YLogger.error(None, "NewsAPI request none JSON object")

        else:
            YLogger.error(None, "NewsAPI request returned error code %d", response.status_code)

        return articles

    def get_headlines(self, source, max_articles=0, sort=False, reverse=False):

        if source in self.function_mapping:
            function = self.function_mapping[source]
            return function(self.api_key, max_articles, sort, reverse)
        else:
            YLogger.error(self, "No source available for %s", source)
            return []

    @staticmethod
    def to_json(articles):
        data = {}
        data['articles'] = []
        for article in articles:
            data['articles'].append(article.to_json())
        return data

    @staticmethod
    def json_to_file(filename, json_data):
        try:
            with open(filename, 'w+', encoding="utf-8") as json_file:
                json.dump(json_data, json_file)

        except Exception as e:
            YLogger.exception(None, "Failed to write to [%s]", e, filename)

    @staticmethod
    def json_from_file(filename):
        try:
            with open(filename, 'r+', encoding="utf-8") as json_file:
                return json.load(json_file)

        except Exception as e:
            YLogger.exception(None, "Failed to read from [%s]", e, filename)

    @staticmethod
    def to_program_y_text(articles, break_str=" <br /> "):
        return break_str.join("%s - %s" % (article.title, article.description) for article in articles)

    @staticmethod
    def abc_news_au(api_key, max_articles, sort, reverse):
        return NewsAPI._get_data(NewsAPI.ABC_NEWS_AU, api_key, max_articles, sort, reverse)

    @staticmethod
    def al_jazeera_english(api_key, max_articles, sort, reverse):
        return NewsAPI._get_data(NewsAPI.AL_JAZEERA_ENGLISH, api_key, max_articles, sort, reverse)

    @staticmethod
    def ars_technica(api_key, max_articles, sort, reverse):
        return NewsAPI._get_data(NewsAPI.ARS_TECHNICA, api_key, max_articles, sort, reverse)

    @staticmethod
    def associated_press(api_key, max_articles, sort, reverse):
        return NewsAPI._get_data(NewsAPI.ASSOCIATED_PRESS, api_key, max_articles, sort, reverse)

    @staticmethod
    def bbc_news(api_key, max_articles, sort, reverse):
        return NewsAPI._get_data(NewsAPI.BBC_NEWS, api_key, max_articles, sort, reverse)

    @staticmethod
    def bbc_sport(api_key, max_articles, sort, reverse):
        return NewsAPI._get_data(NewsAPI.BBC_SPORT, api_key, max_articles, sort, reverse)

    @staticmethod
    def bloomberg(api_key, max_articles, sort, reverse):
        return NewsAPI._get_data(NewsAPI.BLOOMBERG, api_key, max_articles, sort, reverse)

    @staticmethod
    def business_insider(api_key, max_articles, sort, reverse):
        return NewsAPI._get_data(NewsAPI.BUSINESS_INSIDER, api_key, max_articles, sort, reverse)

    @staticmethod
    def business_insider_uk(api_key, max_articles, sort, reverse):
        return NewsAPI._get_data(NewsAPI.BUSINESS_INSIDER_UK, api_key, max_articles, sort, reverse)

    @staticmethod
    def buzzfeed(api_key, max_articles, sort, reverse):
        return NewsAPI._get_data(NewsAPI.BUZZFEED, api_key, max_articles, sort, reverse)

    @staticmethod
    def cnbc(api_key, max_articles, sort, reverse):
        return NewsAPI._get_data(NewsAPI.CNBC, api_key, max_articles, sort, reverse)

    @staticmethod
    def cnn(api_key, max_articles, sort, reverse):
        return NewsAPI._get_data(NewsAPI.CNN, api_key, max_articles, sort, reverse)

    @staticmethod
    def daily_mail(api_key, max_articles, sort, reverse):
        return NewsAPI._get_data(NewsAPI.DAILY_MAIL, api_key, max_articles, sort, reverse)

    @staticmethod
    def engadget(api_key, max_articles, sort, reverse):
        return NewsAPI._get_data(NewsAPI.ENGADGET, api_key, max_articles, sort, reverse)

    @staticmethod
    def entertainment_weekly(api_key, max_articles, sort, reverse):
        return NewsAPI._get_data(NewsAPI.ENTERTAINMENT_WEEKLY, api_key, max_articles, sort, reverse)

    @staticmethod
    def espn(api_key, max_articles, sort, reverse):
        return NewsAPI._get_data(NewsAPI.ESPN, api_key, max_articles, sort, reverse)

    @staticmethod
    def espn_cric_info(api_key, max_articles, sort, reverse):
        return NewsAPI._get_data(NewsAPI.ESPN_CRIC_INFO, api_key, max_articles, sort, reverse)

    @staticmethod
    def financial_times(api_key, max_articles, sort, reverse):
        return NewsAPI._get_data(NewsAPI.FINANCIAL_TIMES, api_key, max_articles, sort, reverse)

    @staticmethod
    def football_italia(api_key, max_articles, sort, reverse):
        return NewsAPI._get_data(NewsAPI.FOOTBALL_ITALIA, api_key, max_articles, sort, reverse)

    @staticmethod
    def fortune(api_key, max_articles, sort, reverse):
        return NewsAPI._get_data(NewsAPI.FORTUNE, api_key, max_articles, sort, reverse)

    @staticmethod
    def four_four_two(api_key, max_articles, sort, reverse):
        return NewsAPI._get_data(NewsAPI.FOUR_FOUR_TWO, api_key, max_articles, sort, reverse)

    @staticmethod
    def fox_sports(api_key, max_articles, sort, reverse):
        return NewsAPI._get_data(NewsAPI.FOX_SPORTS, api_key, max_articles, sort, reverse)

    @staticmethod
    def google_news(api_key, max_articles, sort, reverse):
        return NewsAPI._get_data(NewsAPI.GOOGLE_NEWS, api_key, max_articles, sort, reverse)

    @staticmethod
    def hacker_news(api_key, max_articles, sort, reverse):
        return NewsAPI._get_data(NewsAPI.HACKER_NEWS, api_key, max_articles, sort, reverse)

    @staticmethod
    def ign(api_key, max_articles, sort, reverse):
        return NewsAPI._get_data(NewsAPI.IGN, api_key, max_articles, sort, reverse)

    @staticmethod
    def independent(api_key, max_articles, sort, reverse):
        return NewsAPI._get_data(NewsAPI.INDEPENDENT, api_key, max_articles, sort, reverse)

    @staticmethod
    def mashable(api_key, max_articles, sort, reverse):
        return NewsAPI._get_data(NewsAPI.MASHABLE, api_key, max_articles, sort, reverse)

    @staticmethod
    def metro(api_key, max_articles, sort, reverse):
        return NewsAPI._get_data(NewsAPI.METRO, api_key, max_articles, sort, reverse)

    @staticmethod
    def mirror(api_key, max_articles, sort, reverse):
        return NewsAPI._get_data(NewsAPI.MIRROR, api_key, max_articles, sort, reverse)

    @staticmethod
    def mtv_news(api_key, max_articles, sort, reverse):
        return NewsAPI._get_data(NewsAPI.MTV_NEWS, api_key, max_articles, sort, reverse)

    @staticmethod
    def mtv_news_uk(api_key, max_articles, sort, reverse):
        return NewsAPI._get_data(NewsAPI.MTV_NEWS_UK, api_key, max_articles, sort, reverse)

    @staticmethod
    def national_geographic(api_key, max_articles, sort, reverse):
        return NewsAPI._get_data(NewsAPI.NATIONAL_GEOGRAPHIC, api_key, max_articles, sort, reverse)

    @staticmethod
    def new_scientist(api_key, max_articles, sort, reverse):
        return NewsAPI._get_data(NewsAPI.NEW_SCIENTIST, api_key, max_articles, sort, reverse)

    @staticmethod
    def newsweek(api_key, max_articles, sort, reverse):
        return NewsAPI._get_data(NewsAPI.NEWSWEEK, api_key, max_articles, sort, reverse)

    @staticmethod
    def new_york_magazine(api_key, max_articles, sort, reverse):
        return NewsAPI._get_data(NewsAPI.NEW_YORK_MAGAZINE, api_key, max_articles, sort, reverse)

    @staticmethod
    def nfl_news(api_key, max_articles, sort, reverse):
        return NewsAPI._get_data(NewsAPI.NFL_NEWS, api_key, max_articles, sort, reverse)

    @staticmethod
    def polygon(api_key, max_articles, sort, reverse):
        return NewsAPI._get_data(NewsAPI.POLYGON, api_key, max_articles, sort, reverse)

    @staticmethod
    def recode(api_key, max_articles, sort, reverse):
        return NewsAPI._get_data(NewsAPI.RECODE, api_key, max_articles, sort, reverse)

    @staticmethod
    def reddit(api_key, max_articles, sort, reverse):
        return NewsAPI._get_data(NewsAPI.REDDIT_R_ALL, api_key, max_articles, sort, reverse)

    @staticmethod
    def reuters(api_key, max_articles, sort, reverse):
        return NewsAPI._get_data(NewsAPI.REUTERS, api_key, max_articles, sort, reverse)

    @staticmethod
    def talksport(api_key, max_articles, sort, reverse):
        return NewsAPI._get_data(NewsAPI.TALKSPORT, api_key, max_articles, sort, reverse)

    @staticmethod
    def techcrunch(api_key, max_articles, sort, reverse):
        return NewsAPI._get_data(NewsAPI.TECHCRUNCH, api_key, max_articles, sort, reverse)

    @staticmethod
    def techradar(api_key, max_articles, sort, reverse):
        return NewsAPI._get_data(NewsAPI.TECHRADAR, api_key, max_articles, sort, reverse)

    @staticmethod
    def the_economist(api_key, max_articles, sort, reverse):
        return NewsAPI._get_data(NewsAPI.THE_ECONOMIST, api_key, max_articles, sort, reverse)

    @staticmethod
    def the_guardian_au(api_key, max_articles, sort, reverse):
        return NewsAPI._get_data(NewsAPI.THE_GUARDIAN_AU, api_key, max_articles, sort, reverse)

    @staticmethod
    def the_guardian_uk(api_key, max_articles, sort, reverse):
        return NewsAPI._get_data(NewsAPI.THE_GUARDIAN_UK, api_key, max_articles, sort, reverse)

    @staticmethod
    def the_huffington_post(api_key, max_articles, sort, reverse):
        return NewsAPI._get_data(NewsAPI.THE_HUFFINGTON_POST, api_key, max_articles, sort, reverse)

    @staticmethod
    def the_new_york_times(api_key, max_articles, sort, reverse):
        return NewsAPI._get_data(NewsAPI.THE_NEW_YORK_TIMES, api_key, max_articles, sort, reverse)

    @staticmethod
    def the_next_web(api_key, max_articles, sort, reverse):
        return NewsAPI._get_data(NewsAPI.THE_NEXT_WEB, api_key, max_articles, sort, reverse)

    @staticmethod
    def the_sport_bible(api_key, max_articles, sort, reverse):
        return NewsAPI._get_data(NewsAPI.THE_SPORT_BIBLE, api_key, max_articles, sort, reverse)

    @staticmethod
    def the_telegraph(api_key, max_articles, sort, reverse):
        return NewsAPI._get_data(NewsAPI.THE_TELEGRAPH, api_key, max_articles, sort, reverse)

    @staticmethod
    def the_verge(api_key, max_articles, sort, reverse):
        return NewsAPI._get_data(NewsAPI.THE_VERGE, api_key, max_articles, sort, reverse)

    @staticmethod
    def the_wall_street_journal(api_key, max_articles, sort, reverse):
        return NewsAPI._get_data(NewsAPI.THE_WALL_STREET_JOURNAL, api_key, max_articles, sort, reverse)

    @staticmethod
    def the_washington_post(api_key, max_articles, sort, reverse):
        return NewsAPI._get_data(NewsAPI.THE_WASHINGTON_POST, api_key, max_articles, sort, reverse)

    @staticmethod
    def time(api_key, max_articles, sort, reverse):
        return NewsAPI._get_data(NewsAPI.TIME, api_key, max_articles, sort, reverse)

    @staticmethod
    def usa_today(api_key, max_articles, sort, reverse):
        return NewsAPI._get_data(NewsAPI.USA_TODAY, api_key, max_articles, sort, reverse)

    @staticmethod
    def business(api_key, max_articles, sort, reverse):
        articles = []
        articles.extend(NewsAPI.bloomberg(api_key, max_articles, sort, reverse))
        articles.extend(NewsAPI.business_insider(api_key, max_articles, sort, reverse))
        articles.extend(NewsAPI.business_insider_uk(api_key, max_articles, sort, reverse))
        articles.extend(NewsAPI.cnbc(api_key, max_articles, sort, reverse))
        articles.extend(NewsAPI.financial_times(api_key, max_articles, sort, reverse))
        articles.extend(NewsAPI.fortune(api_key, max_articles, sort, reverse))
        articles.extend(NewsAPI.the_economist(api_key, max_articles, sort, reverse))
        articles.extend(NewsAPI.the_wall_street_journal(api_key, max_articles, sort, reverse))
        return articles

    @staticmethod
    def entertainment(api_key, max_articles, sort, reverse):
        articles = []
        articles.extend(NewsAPI.buzzfeed(api_key, max_articles, sort, reverse))
        articles.extend(NewsAPI.daily_mail(api_key, max_articles, sort, reverse))
        articles.extend(NewsAPI.entertainment_weekly(api_key, max_articles, sort, reverse))
        articles.extend(NewsAPI.mashable(api_key, max_articles, sort, reverse))
        return articles

    @staticmethod
    def gaming(api_key, max_articles, sort, reverse):
        articles = []
        articles.extend(NewsAPI.ign(api_key, max_articles, sort, reverse))
        articles.extend(NewsAPI.polygon(api_key, max_articles, sort, reverse))
        return articles

    @staticmethod
    def music(api_key, max_articles, sort, reverse):
        articles = []
        articles.extend(NewsAPI.mtv_news(api_key, max_articles, sort, reverse))
        articles.extend(NewsAPI.mtv_news_uk(api_key, max_articles, sort, reverse))
        return articles

    @staticmethod
    def science_and_nature(api_key, max_articles, sort, reverse):
        articles = []
        articles.extend(NewsAPI.national_geographic(api_key, max_articles, sort, reverse))
        articles.extend(NewsAPI.new_scientist(api_key, max_articles, sort, reverse))
        return articles

    @staticmethod
    def sport(api_key, max_articles, sort, reverse):
        articles = []
        articles.extend(NewsAPI.bbc_sport(api_key, max_articles, sort, reverse))
        articles.extend(NewsAPI.espn(api_key, max_articles, sort, reverse))
        articles.extend(NewsAPI.espn_cric_info(api_key, max_articles, sort, reverse))
        articles.extend(NewsAPI.football_italia(api_key, max_articles, sort, reverse))
        articles.extend(NewsAPI.four_four_two(api_key, max_articles, sort, reverse))
        articles.extend(NewsAPI.fox_sports(api_key, max_articles, sort, reverse))
        articles.extend(NewsAPI.talksport(api_key, max_articles, sort, reverse))
        articles.extend(NewsAPI.the_sport_bible(api_key, max_articles, sort, reverse))
        return articles

    @staticmethod
    def technology(api_key, max_articles, sort, reverse):
        articles = []
        articles.extend(NewsAPI.ars_technica(api_key, max_articles, sort, reverse))
        articles.extend(NewsAPI.engadget(api_key, max_articles, sort, reverse))
        articles.extend(NewsAPI.hacker_news(api_key, max_articles, sort, reverse))
        articles.extend(NewsAPI.recode(api_key, max_articles, sort, reverse))
        articles.extend(NewsAPI.techcrunch(api_key, max_articles, sort, reverse))
        articles.extend(NewsAPI.techradar(api_key, max_articles, sort, reverse))
        articles.extend(NewsAPI.the_verge(api_key, max_articles, sort, reverse))
        return articles

    @staticmethod
    def uk_news(api_key, max_articles, sort, reverse):
        articles = []
        articles.extend(NewsAPI.bbc_news(api_key, max_articles, sort, reverse))
        articles.extend(NewsAPI.uk_newspapers(api_key, max_articles, sort, reverse))
        return articles

    @staticmethod
    def uk_newspapers(api_key, max_articles, sort, reverse):
        articles = []
        articles.extend(NewsAPI.the_guardian_uk(api_key, max_articles, sort, reverse))
        articles.extend(NewsAPI.mirror(api_key, max_articles, sort, reverse))
        articles.extend(NewsAPI.the_telegraph(api_key, max_articles, sort, reverse))
        articles.extend(NewsAPI.daily_mail(api_key, max_articles, sort, reverse))
        articles.extend(NewsAPI.financial_times(api_key, max_articles, sort, reverse))
        articles.extend(NewsAPI.independent(api_key, max_articles, sort, reverse))
        articles.extend(NewsAPI.metro(api_key, max_articles, sort, reverse))
        return articles

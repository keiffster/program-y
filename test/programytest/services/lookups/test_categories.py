import unittest
from programy.services.lookups.categories import ServiceCategories


class ServiceCategoriesTests(unittest.TestCase):

    def test_init(self):
        self.assertEqual(ServiceCategories.BOOKS, "books")
        self.assertEqual(ServiceCategories.DRINK, "drinks")
        self.assertEqual(ServiceCategories.FOOD, "food")
        self.assertEqual(ServiceCategories.FACTS, "facts")
        self.assertEqual(ServiceCategories.GENERAL, "general")
        self.assertEqual(ServiceCategories.JOKES, "jokes")
        self.assertEqual(ServiceCategories.MEDICAL, "medical")
        self.assertEqual(ServiceCategories.MOVIES, "movies")
        self.assertEqual(ServiceCategories.NEWS, "news")
        self.assertEqual(ServiceCategories.QUOTES, "quotes")
        self.assertEqual(ServiceCategories.SEARCH, "search")
        self.assertEqual(ServiceCategories.SPORT, "sport")
        self.assertEqual(ServiceCategories.STATS, "stats")
        self.assertEqual(ServiceCategories.STOCKS, "stocks")
        self.assertEqual(ServiceCategories.WEATHER, "weather")

"""
Copyright (c) 2016-2020 Keith Sterling http://www.keithsterling.com

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
import urllib.parse
import os
from programy.utils.logging.ylogger import YLogger
from programy.services.base import ServiceQuery
from programy.services.rest.base import RESTService
from programy.services.rest.base import RESTServiceException


class CocktailDBSearchByNameServiceQuery(ServiceQuery):

    @staticmethod
    def create(service):
        return CocktailDBSearchByNameServiceQuery(service)

    def parse_matched(self, matched):
        self._name = ServiceQuery._get_matched_var(matched, 0, "name")

    def __init__(self, service):
        ServiceQuery.__init__(self, service)
        self._name = None

    def execute(self):
        return self._service.search_by_name(self._name)

    def aiml_response(self, response):
        payload = response['response']['payload']
        drinks = payload['drinks']
        drink = drinks[0]

        name = drink['strDrink']
        instructions = drink['strInstructions']
        glass = drink['strGlass']

        ingredients = self._get_ingredients(drink)
        formatted = self._format_ingredients(ingredients)

        result= "NAME {0} INGREDIENTS {1} INSTRUCTIONS {2}".format(name, formatted, instructions)
        YLogger.debug(self, result)
        return result

    @staticmethod
    def _get_ingredients(drink):
        more = True
        count = 1
        ingredients = []
        while more is True and count < 16:
            ingredient_num = 'strIngredient{0}'.format(count)
            measure_num = 'strMeasure{0}'.format(count)

            ingredient = drink.get(ingredient_num, None)
            measure = drink.get(measure_num, None)

            if ingredient is not None:
                ingredients.append((measure, ingredient))
                count += 1
            else:
                more = False

        return ingredients

    @staticmethod
    def _format_ingredients(ingredients):
        return " and ".join("{0} {1}".format(x[0], x[1]) for x in ingredients)


class CocktailDBSearchByIngredientServiceQuery(ServiceQuery):

    @staticmethod
    def create(service):
        return CocktailDBSearchByIngredientServiceQuery(service)

    def parse_matched(self, matched):
        self._ingredient = ServiceQuery._get_matched_var(matched, 0, "ingredient")

    def __init__(self, service):
        ServiceQuery.__init__(self, service)
        self._ingredient = None

    def execute(self):
        return self._service.search_by_ingredient(self._ingredient)

    def aiml_response(self, response):
        payload = response['response']['payload']
        drinks = payload['ingredients']
        drink = drinks[0]

        name = drink['strIngredient']
        description = drink['strDescription']

        result = "NAME {0} DESCRIPTION {1}".format(name, description)
        YLogger.debug(self, result)
        return result


class CocktailDBServiceException(RESTServiceException):

    def __init__(self, msg):
        RESTServiceException.__init__(self, msg)


class CocktailDBService(RESTService):
    """
    """
    PATTERNS = [
        [r"SEARCH\sNAME\s(.+)", CocktailDBSearchByNameServiceQuery],
        [r"SEARCH\sINGREDIENT\s(.+)", CocktailDBSearchByIngredientServiceQuery]
    ]

    SEARCH_BY_NAME_URL="https://www.thecocktaildb.com/api/json/v1/{0}/search.php?s={1}"
    SEARCH_BY_INGREDIENT_URL="https://www.thecocktaildb.com/api/json/v1/{0}/search.php?i={1}"

    def __init__(self, configuration):
        RESTService.__init__(self, configuration)
        self._api_key = None

    def patterns(self) -> list:
        return CocktailDBService.PATTERNS

    def initialise(self, client):
        self._api_key = client.license_keys.get_key('THECOCKTAILDB_APIKEY')
        if self._api_key is None:
            YLogger.error(self, "THECOCKTAILDB_APIKEY missing from license.keys, service will not function correctly!")

    def get_default_aiml_file(self):
        return os.path.dirname(__file__) + os.sep + "cocktaildb.aiml"

    @staticmethod
    def get_default_conf_file():
        return os.path.dirname(__file__) + os.sep + "cocktaildb.conf"

    def _build_search_by_name_url(self, name):
        url = CocktailDBService.SEARCH_BY_NAME_URL.format(self._api_key, name)
        return url

    def search_by_name(self, name):
        url = self._build_search_by_name_url(name)
        response = self.query('search_by_name', url)
        return response

    def _build_search_by_ingredient_url(self, ingredient):
        url = CocktailDBService.SEARCH_BY_INGREDIENT_URL.format(self._api_key, ingredient)
        return url

    def search_by_ingredient(self, ingredient):
        url = self._build_search_by_ingredient_url(ingredient)
        response = self.query('search_by_ingredient', url)
        return response

    def _response_to_json(self, api, response):
        return response.json()

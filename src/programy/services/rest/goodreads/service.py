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
import os
import json
from urllib.parse import quote
from xmljson import abdera
from xml.etree.ElementTree import fromstring
from programy.utils.logging.ylogger import YLogger
from programy.services.base import ServiceQuery
from programy.services.rest.base import RESTService
from programy.services.rest.base import RESTServiceException


class GoodReadsSearchAuthorServiceQuery(ServiceQuery):

    @staticmethod
    def create(service):
        return GoodReadsSearchAuthorServiceQuery(service)

    def parse_matched(self, matched):
        self._name = ServiceQuery._get_matched_var(matched, 0, "name")

    def __init__(self, service):
        ServiceQuery.__init__(self, service)
        self._name = None

    def execute(self):
        return self._service.search_for_author(self._name)

    def aiml_response(self, response):
        payload = response['response']['payload']
        goodreads = payload['GoodreadsResponse']
        children = goodreads['children'][1]
        author = children['author']
        attributes = author['attributes']
        id = attributes['id']
        result = "AUTHOR SEARCH {0}".foramt(str(id))
        YLogger.debug(self, result)
        return result


class GoodReadsListBooksServiceQuery(ServiceQuery):

    @staticmethod
    def create(service):
        return GoodReadsListBooksServiceQuery(service)

    def parse_matched(self, matched):
        self._authorid = ServiceQuery._get_matched_var(matched, 0, "authorid")

    def __init__(self, service):
        ServiceQuery.__init__(self, service)
        self._authorid = None

    def execute(self):
        return self._service.list_books(self._authorid)

    def aiml_response(self, response):
        payload = response['response']['payload']
        goodReadsResponse = payload['GoodreadsResponse']
        children = goodReadsResponse['children']
        author = children[1]['author']
        books = author['children'][3]['books']
        titles = []
        for child in books['children']:
            book = child['book']
            for item in book['children']:
                if 'title_without_series' in item:
                    titles.append(item['title_without_series'])
                    break

        result = "BOOK LIST <ul>{0}</ul>".format("".join("<li>{0}</li>".format(x) for x in titles))
        YLogger.debug(self, result)
        return result


class GoodReadsServiceException(RESTServiceException):

    def __init__(self, msg):
        RESTServiceException.__init__(self, msg)


class GoodReadsService(RESTService):
    """
    """
    PATTERNS = [
        [r"SEARCH\sAUTHOR\s(.+)", GoodReadsSearchAuthorServiceQuery],
        [r"LIST\sBOOKS\s(.+)", GoodReadsListBooksServiceQuery]
    ]

    SEARCH_AUTHOR_URL="https://www.goodreads.com/api/author_url/{0}?key={1}"
    BOOKS_LIST_URL="https://www.goodreads.com/author/list/{0}?format=xml&key={1}"

    def __init__(self, configuration):
        RESTService.__init__(self, configuration)
        self._api_key = None
        self._api_secret = None

    def patterns(self) -> list:
        return GoodReadsService.PATTERNS

    def initialise(self, client):
        self._api_key = client.license_keys.get_key('GOODREADS_KEY')
        if self._api_key is None:
            YLogger.error(self, "GOODREADS_KEY missing from license.keys, service will not function correctly!")

        self._api_secret = client.license_keys.get_key('GOODREAD_SECRET')
        if self._api_secret is None:
            YLogger.error(self, "GOODREAD_SECRET missing from license.keys, service will not function correctly!")

    def get_default_aiml_file(self):
        return os.path.dirname(__file__) + os.sep + "goodreads.aiml"

    @staticmethod
    def get_default_conf_file():
        return os.path.dirname(__file__) + os.sep + "goodreads.conf"

    def _build_author_search_url(self, name):
        url = GoodReadsService.SEARCH_AUTHOR_URL.format(quote(name), self._api_key)
        return url

    def search_for_author(self, name):
        url = self._build_author_search_url(name)
        response = self.query('search_for_author', url)
        return response

    def _build_list_books_url(self, authorid):
        url = GoodReadsService.BOOKS_LIST_URL.format(authorid, self._api_key)
        return url

    def list_books(self, authorid):
        url = self._build_list_books_url(authorid)
        response = self.query('list_books', url)
        return response

    def _response_to_json(self, api, response):
        jsondata = abdera.data(fromstring(response.content.decode('UTF-8')))
        return json.loads(json.dumps(jsondata))

    @staticmethod
    def get_author_id(payload):
        response = payload.get("response", None)
        if response is not None:
            payload = response.get("payload", None)
            if payload is not None:
                goodreadsResponse = payload.get("GoodreadsResponse", None)
                if goodreadsResponse is not None:
                    children = goodreadsResponse.get('children', [])
                    for child in children:
                        if child.get('author', None) is not None:
                            author = child['author']
                            attributes = author.get("attributes", {})
                            return attributes.get('id', None)
        return None

    @staticmethod
    def get_books(payload):
        book_list = []
        response = payload.get("response", None)
        if response is not None:
            payload = response.get("payload", None)
            if payload is not None:
                goodreadsResponse = payload.get("GoodreadsResponse", None)
                if goodreadsResponse is not None:
                    children = goodreadsResponse.get('children', [])
                    for child in children:
                        if child.get('author', None) is not None:
                            author = child['author']
                            author_children = author.get('children', [])
                            for author_child in author_children:
                                books = author_child.get('books', {})
                                book_children = books.get('children', [])
                                for book_child in book_children:
                                    book = book_child.get('book', {})
                                    book_subchildren = book.get('children', [])
                                    book_id = book_title = None
                                    for book_subchild in book_subchildren:
                                        if 'id' in book_subchild:
                                            id_dict = book_subchild.get('id', {})
                                            if id_dict:
                                                id_dict_childs = id_dict.get('children', [])
                                                if id_dict_childs:
                                                    book_id = id_dict_childs[0]

                                        if 'title' in book_subchild:
                                            book_title = book_subchild.get('title', None)

                                        if book_id and book_title:
                                            book_list.append((book_id, book_title))
                                            break

        return tuple(book_list)


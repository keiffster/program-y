from programy.services.requestsapi import RequestsAPI

class MockRequestsResponse(object):

    def __init__(self, data):
        self._data = data

    def json(self):
        return self._data

    @property
    def content(self):
        return self._data

class MockRequestsAPI(RequestsAPI):

    def __init__(self, response=None):
        self._response = response

    def get(self, url, params):
        if self._response is None:
            return None
        else:
            return MockRequestsResponse(self._response)


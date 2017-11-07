import drest
from pprint import pprint
import json

class RequestHandler(drest.request.RequestHandler):
    class Meta:
        debug = False

    def add_header(self, key, value):
        super(RequestHandler, self).add_header(key, value)

    def add_param(self, key, value):
        super(RequestHandler, self).add_param(key, value)

    def add_url_param(self, key, value):
        super(RequestHandler, self).add_url_param(key, value)

    # Returns the response data of a request in an dictionary
    # Parameters: response - a drest response object
    # Returns: a dictionary of the response data
    def handle_response(self, response):
        data = json.loads(json.dumps(response.data))
        if len(data) == 1:
            data = dict(data[0])
        assert not 'error' in data.keys() ,"Incorrect arguments"
        return data

    # Makes the request
    # Parameters: method - one of 'GET', 'POST', 'PUT', 'DELETE'
    #             url - the URL of the request (the base URL is prepended)
    #             params - optional dictionary of parameters of the request
    #             headers - optional dictionary of headers of the request
    # Returns: a dictionary of the response data
    def make_request(self, method, url, params = None, headers = None):
        url = url.replace(' ', '/')
        response = super(RequestHandler, self).make_request(method, url, params, headers)
        return response

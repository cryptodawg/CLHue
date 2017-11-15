import drest
from RequestHandler import RequestHandler

class HueAPI(drest.API):
    class Meta:
        request_handler = RequestHandler

    def __init__(self, hueURL, username):
        self.Meta.baseurl = 'http://' + hueURL + '/api/' + username
        super(HueAPI, self).__init__(self.Meta.baseurl)

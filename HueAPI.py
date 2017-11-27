import requests
import json

class HueAPI():
    """
    Handles the GET/PUT requests to a Philips Hue bridge.

    Constructor parameters:
        hueURL -- the URL of the Hue bridge (often in the form of an IP address)
        username -- the bridge-generated username to use for the requests
    """

    def __init__(self, hueURL, username):
        self.url = 'http://' + hueURL + '/api/' + username
        self.session = requests.Session()

    def getFullURL(self, apiObject):

        """
        Returns the base URL with added parameters.

        Parameters:
            apiObject -- a string in the form of <lights/groups> <id>
        """
        return self.url + '/' + apiObject.replace(' ', '/')

    def get(self, apiObject):
        """
        Performs a GET request on the Hue bridge. Returns the API response in JSON format.

        Parameters:
            apiObject -- a string in the form of <lights/groups> <id>
        """
        fullURL = self.getFullURL(apiObject)
        response = self.session.get(fullURL)
        return response.json()

    def put(self, apiObject, params):
        """
        Performs a PUT request on the Hue bridge. Returns the API response in JSON format.

        Parameters:
            apiObject -- a string in the form of <lights/groups> <id>
        """
        fullURL = self.getFullURL(apiObject)
        params = json.dumps(params)
        response = self.session.put(fullURL, params)
        return response.json()

import requests
import json

class HueAPI():

    def __init__(self, hueURL, username):
        self.url = 'http://' + hueURL + '/api/' + username
        self.session = requests.Session()
        # self.session.hooks['response'].append(self.handleResponse) # Add response hook

    # # Hook to handle the response object
    # def handleResponse(self, response, *args, **kwargs): # What are *args, **kwargs?
    #     data = response.json()
    #     if len(data) == 1:
    #         data = dict(data[0])
    #     assert not 'error' in data.keys() ,"Incorrect arguments"
    #     return data

    # Returns the base URL with added parameters
    # Parameters: apiObject - arguments separated by a space
    # Returns: string of the base URL with parameters added on the end
    def getFullURL(self, apiObject):
        return self.url + '/' + apiObject.replace(' ', '/')

    # Performs a GET request on the Hue bridge
    # Parameters: apiObject - space-separated arguments
    # Returns: A JSON object representing the response back from the Hue bridge
    def get(self, apiObject):
        fullURL = self.getFullURL(apiObject)
        response = self.session.get(fullURL)
        return response.json()

    # Performs a GET request on the Hue bridge
    # Parameters: apiObject - space-separated arguments
    #             params - a dictionary representing the body of the message to put
    # Returns: A JSON object representing the response back from the Hue bridge
    def put(self, apiObject, params):
        fullURL = self.getFullURL(apiObject)
        params = json.dumps(params)
        response = self.session.put(fullURL, params)
        return response.json()

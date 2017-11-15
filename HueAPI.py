import requests

class HueAPI():

    def __init__(self, hueURL, username):
        self.url = 'http://' + hueURL + '/api/' + username
        self.session = requests.Session()
        # self.session.hooks['response'].append(self.handleResponse) # Add response hook

    # Hook to handle the response object - currently not in use
    def handleResponse(self, response, *args, **kwargs): # What are *args, **kwargs?
        data = response.json()
        # if len(data) == 1:
        #     data = dict(data[0])
        assert not 'error' in data.keys() ,"Incorrect arguments"
        return data

    # Returns the base URL with added parameters
    # Parameters: args - arguments separated by a space
    # Returns: string of the base URL with parameters added on the end
    def getFullURL(self, args):
        return self.url + '/' + args.replace(' ', '/')

    # Performs a GET request on the Hue bridge
    # Parameters: args - space-separated arguments
    # Returns: A JSON object representing the response back from the Hue bridge
    def get(self, args):
        fullURL = self.getFullURL(args)
        response = self.session.get(fullURL)
        return response.json()

from HueAPI import HueAPI
from ConfigHandler import ConfigHandler

class HueInteract():
    """ A Python API to interact with the Philips Hue bridge API in a user-friendly way. """

    def __init__(self):
        conf = ConfigHandler().load()
        username = '8zBIONh42t4l1LbxOymAit7LYY9UHj338dW0jjc0' # TODO: Programatically get this - will be done in ConfigHandler
        self.api = HueAPI(conf['bridgeIP'], username) # TODO: Change this once we can programatically get the username

    def get(self, arg):
        """ Returns items from the bridge API in JSON format.

        Parameters:
			arg -- a string in the form of <lights/groups> <id>
        """
        return self.api.get(arg)

    def bridgeName(self):
        """ Returns the friendly name of the bridge.

        Parameters:
            arg -- a string in the form of <lights/groups> <id>
        """
        configData = self.api.get('config')
        return configData['name']

    def putState(self, arg, newState):
        """ Changes the state of an object on the bridge. Returns the API response in JSON format.

        Parameters:
			arg -- a string in the form of <lights/groups> <id>
        """
        if arg[:6] == 'groups':
            return self.api.put(arg + ' action', newState)
        else:
            return self.api.put(arg + ' state', newState)

    # TODO: Error handling if we specify this for a bulb that can only handle white
    def rainbow(self, arg, bri=-1, sat=-1):
        """ Cycles an item through all hues. Returns the API response in JSON format.

        Parameters:
			arg -- a string in the form of <lights/groups> <id>
            bri -- optional, specifies brightness from 1 (dim) to 254 (most bright)
            sat -- optional, specifies saturation from 0 (white) to 254 (most saturated)
        """
        stateDict = {'on': True, 'effect': 'colorloop'}
        if (sat != -1): # Saturation is defined
            stateDict['sat'] = sat
        if (bri != -1): # Brightness is defined
            stateDict['bri'] = bri
        return self.putState(arg, stateDict)

    def power(self, arg, on):
        """ Powers an object on or off. Returns the API response in JSON format.

        Parameters:
			arg -- a string in the form of <lights/groups> <id>
            on -- a boolean, True if we want to turn the object on and False if we want to turn it off
        """
        return self.putState(arg, {'on': on})

    def status(self, arg):
        response = self.get(arg)
        try:
            objectStatus = response['state']['on']
            return objectStatus
        except TypeError: # When there's an error on the bridge, there will only be one index ('error') in response
            return response

    def toggle(self, arg):
        """ Toggles the power of an object on the bridge from off to on and vice-versa. Returns the API response in JSON format.

        Parameters:
			arg -- a string in the form of <lights/groups> <id>
        """
        currState = status(arg)
        return self.power(arg, not currState)

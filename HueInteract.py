from HueAPI import HueAPI
from ConfigHandler import ConfigHandler

# TODO: Create a hook for error handling

class HueInteract():

    def __init__(self):
        conf = ConfigHandler().load()
        username = '8zBIONh42t4l1LbxOymAit7LYY9UHj338dW0jjc0' # TODO: Programatically get this - will be done in ConfigHandler
        self.api = HueAPI(conf['bridgeIP'], username) # TODO: Change this once we can programatically get the username

    # Statuses an object
    # Parameters: arg - arguments separated by a space
    # Returns: True if object is turned on; False otherwise.
    def getState(self, arg):
        return self.api.make_request('GET', arg)['state']['on']

    # Get items on the bridge
    # arg: Follows pattern defined in Hue API
    # Returns: A dict of the item
    def get(self, arg):
        return self.api.make_request('GET', arg)

    # Toggles items on the bridge
    # arg: Follows pattern defined in Hue API
    def toggle(self, arg):
        currState = self.api.make_request('GET', arg)['state']['on']
        if currState:
        	print('Light is on, turning off.')
        else:
        	print('Light is off, turning on.')

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
        return self.api.get(arg)['state']['on']

    # Get items on the bridge
    # Parameters: arg - arguments separated by a space
    # Returns: A dict of the item
    def get(self, arg):
        return self.api.get(arg)

    # Changes the state of an item
    # Parameters: arg - arguments separated by a space
    #             newState - dictionary containing the new state of the item
    def putState(self, arg, newState):
        pass
        # return self.api.make_request('PUT', arg + ' state', newState)

    # Powers an item on or off
    # Parameters: arg - arguments separated by a space
    #             on - boolean indicating if we want to turn the item on
    def power(self, arg, on):
        pass
        # powerDict = {'on': on}
        # return self.putState(arg, powerDict)

    # Toggles items on the bridge
    # Parameters: arg - arguments separated by a space
    def toggle(self, arg):
        currState = self.getState(arg)
        if currState:
        	print('Light is on, turning off.')
        else:
        	print('Light is off, turning on.')

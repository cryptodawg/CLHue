from HueAPI import HueAPI
from ConfigHandler import ConfigHandler

# TODO: Create a hook for error handling

class HueInteract():

    def __init__(self):
        conf = ConfigHandler().load()
        username = '8zBIONh42t4l1LbxOymAit7LYY9UHj338dW0jjc0' # TODO: Programatically get this - will be done in ConfigHandler
        self.api = HueAPI(conf['bridgeIP'], username) # TODO: Change this once we can programatically get the username
        self.appGroups = dict()

    # Get items on the bridge
    # Parameters: arg - the object to get information on, separated by a space
    # Returns: API response in JSON format
    def get(self, arg):
        return self.api.get(arg)

    # Changes the state of an item
    # Parameters: arg - the object to change state of, separated by a space
    #             newState - dictionary containing the new state of the item
    # Returns: API response in JSON format
    def putState(self, arg, newState):
        if arg == 'all':
            arg = 'groups 0'
        if arg[:5] == 'groups':
            return self.api.put(arg + ' action', newState)
        else:
            return self.api.put(arg + ' state', newState)

    # Powers an item on and off
    # Parameters: arg - the object to change the power state of, separated by a space
    #             on - True if we want to turn the object on, False if we want to turn it off
    # Returns: API response in JSON format
    def power(self, arg, on):
        return self.putState(arg, {'on': on})

    # Toggles the power of items on the bridge
    # Parameters: arg - the object to toggle the power on, separated by a space
    # Returns: API response in JSON format
    def toggle(self, arg):
        currState = self.get(arg)['state']['on']
        if currState:
            response = self.power(arg, False)
        else:
            response = self.power(arg, True)
        return response

from HueInteract import HueInteract

class LightGroup:
    """ Enables a user to define app-specific groups of lights instead of storing them all on the bridge

    Constructor parameters:
        api --- a HueInteract object
        lights --- a list of lights on the bridge to be in the group
        name --- optional, the name of the group
    """

    def __init__(self, api, lights, name = None):
        self.name = name
        self.api = api
        if lights == 'all':
            allLights = dict(self.api.get('lights')).keys()
            self.lights = list(allLights)
        else:
            self.lights = lights
        self.lightsStr = ['lights ' + str(i) for i in self.lights]

    def __str__(self):
        """ Returns a string representation of the LightGroup """
        return str(self.name) + ": " + str(self.lights)

    def status(self):
        """ Returns True if all lights in the group are on, False otherwise """
        for i in self.lightsStr:
            if not self.api.status(i):
                return False
        return True

    def rename(self, newName):
        """ Renames the group.

        Parameters:
            newName --- the name you wish to rename the group to
        """

        self.name = newName

    def get(self):
        """ Returns the API response of the status of all lights in the group """
        response = []
        for i in self.lightsStr:
            response.append(self.api.get(i))
        return response

    def addLight(self, newLight):
        """ Add a light to the group.

        Parameters:
            newLight --- the light you wish to add to the group.
        """
        newLight = str(newLight)
        try:
            testExistence = self.api.get('lights ' + newLight)['state']
            self.lights.add(newLight)
            self.lightsStr.append('lights ' + newLight)
        except TypeError:
            print("Light " + newLight + " not found on the bridge.")

    def removeLight(self, toRemove):
        """ Remove a light from the group.

        Parameters:
            toRemove --- the light you wish to remove from the group. Returns the API response in JSON format.
        """
        toRemove = str(toRemove)
        try:
            self.lights.remove(toRemove)
            self.lightsStr.remove('lights ' + toRemove)
        except KeyError:
            print("Light " + toRemove + " doesn't exist in group " + self.name)

    def rainbow(self, bri = -1, sat = -1):
        """ Cycles all lights in the group through all hues.

        Parameters:
            bri -- optional, specifies brightness from 1 (dim) to 254 (most bright)
            sat -- optional, specifies saturation from 0 (white) to 254 (most saturated)
        """
        response = []
        for i in self.lightsStr:
            response.append(self.api.rainbow(i, bri, sat))
        return response

from LightGroup import LightGroup

class LightGroupManager:
    """ A manager for a collection of LightGroup objects.

    Constructor parameters:
        api --- a HueInteract object
    """

    def __init__(self, api):
        self.noNames = 0
        self.groups = dict()
        self.api = api
        self.add('all', name = 'all')

    def __str__(self):
        """ Returns a string representation of the LightGroupManager in the format of 'Group name': [lights in the group] """
        string = dict()
        for group in self.groups.keys():
            string[group] = self.groups[group].lights
        return str(string)

    def __getitem__(self, key):
        """ Makes LightGroupManager subscriptable. """
        return self.get(key)

    def get(self, key):
        """ Returns the LightGroup with name of key.

        Parameters:
            key --- the name of the LightGroup to return.
        """
        return self.groups[key]

    def getAllLights(self):
        """ Returns the LightGroup containing all lights """
        return self.groups['All Lights']

    def add(self, lights, name = None):
        """ Add a LightGroup. Returns the LightGroup that was added.

        Parameters:
            lights --- a list of lights to be in the new group
            name --- optional, the name of the new group. Will be an integer if name is omitted.
        """
        if name is None:
            name = str(self.noNames)
            self.noNames += 1
        newGroup = LightGroup(self.api, lights, name)
        self.groups[name] = newGroup
        return newGroup

    def remove(self, name):
        """ Remove a LightGroup """
        if name == str(self.noNames):
            self.noNames -= 1
        try:
            self.groups.pop(name, None)
        except KeyError:
            print("Group does not exist.")

    def status(self, key):
        lights = self.groups[key]
        results = []
        for i in lights:
            results.append(self.api.get('lights ' + str(i)))
        return results

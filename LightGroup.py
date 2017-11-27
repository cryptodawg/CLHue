from HueInteract import HueInteract

class LightGroup(HueInteract):
    """ Enables a user to define app-specific groups of lights instead of storing them all on the bridge """

    def __init__(self, api, lights, name = None):
        self.name = name
        self.api = api
        if lights == 'all':
            allLights = dict(self.api.get('lights')).keys()
            self.lights = set(allLights)
        else:
            self.lights = lights
        self.lightsStr = ['lights ' + str(i) for i in self.lights]

    def __str__(self):
        return str(self.name) + ": " + str(self.lights)

    def status(self):
        for i in self.lightsStr:
            if not self.api.status(i):
                return False
        return True

    def rename(self, newName):
        self.name = newName

    def get(self):
        response = []
        for i in self.lightsStr:
            response.append(self.api.get(i))
        return response

    def add(self, newLight):
        newLight = str(newLight)
        try:
            testExistence = self.api.get('lights ' + newLight)['state']
            self.lights.add(newLight)
            self.lightsStr.append('lights ' + newLight)
        except TypeError:
            print("Light " + newLight + " not found on the bridge.")

    def remove(self, toRemove):
        toRemove = str(toRemove)
        try:
            self.lights.remove(toRemove)
            self.lightsStr.remove('lights ' + toRemove)
        except KeyError:
            print("Light " + toRemove + " doesn't exist in group " + self.name)

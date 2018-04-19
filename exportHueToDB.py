import json
from HueInteract import HueInteract
from ConfigHandler import ConfigHandler
from LightGroupManager import LightGroupManager

name = 'CryptoHue'
confHandler = ConfigHandler()
conf = confHandler.load(name)
bridgeIP = conf['bridgeIP']
api = HueInteract(bridgeIP)
groups = LightGroupManager(api)
allStatus = groups.status('all')
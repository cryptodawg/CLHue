import json
import socket

class ConfigHandler():
    """ Handler for clHue configuration. """

    def __init__(self):
        self.conf = dict()

    def load(self, name = "default"):
        """ Load the configuration file (clConfig.conf) and returns the loaded configuration in a dictionary. """
        # Attempt to load the file
        try:
            with open('clConfig.conf', 'r') as confFile:
                parsedConf = json.load(confFile)
        except (FileNotFoundError, json.decoder.JSONDecodeError):
            open('clConfig.conf', 'a').close()
            parsedConf = dict()

        # See if name exists
        try:
            self.conf = parsedConf[name]
        except KeyError:
            self.conf = dict()
        self.name = name  

        # See if there is a bridge IP listed
        try:
            bridgeIP = self.conf["bridgeIP"]
        except KeyError:
            self.setIP()

        return self.conf

    def findBridgeIP(self):
        """ Returns the IP address of a Philips Hue bridge on the network """
        msg = \
            'M-SEARCH * HTTP/1.1\r\n' \
            'ST:upnp:rootdevice\r\n' \
            'MX:2\r\n' \
            'MAN:"ssdp:discover"\r\n' \
            '\r\n'
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
        s.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        s.settimeout(5)
        s.sendto(msg.encode(), ('192.168.50.255', 1900))
        bridgeIP = None
        try:
            while True:
                data, addr = s.recvfrom(65507)
                if 'IpBridge'.encode() in data: # TODO: Make this work if there are multiple bridges on the network
                    bridgeIP = addr[0]
                    return bridgeIP
        except socket.timeout:
            pass
        s.close()
        if bridgeIP is None:
            raise ValueError("No bridge found")

    def setIP(self, ipAddress = None):
        if ipAddress is None:
            ipAddress = self.findBridgeIP()
        self.conf["bridgeIP"] = ipAddress

    def writeConfig(self, name = None, newConf = None):
        """ Writes the currently loaded configuration to the configuration file. Doesn't return anything. """
        with open('clConfig.conf', 'r') as confFile:
            try:
                parsedConf = json.load(confFile)
            except json.decoder.JSONDecodeError:
                parsedConf = dict()
            if name is None:
                    name = self.name
            if newConf is None:
                parsedConf[name] = self.conf
            else:
                parsedConf[name] = newConf
        with open('clConfig.conf', 'w') as confFile:
                json.dump(parsedConf, confFile)
                confFile.flush()

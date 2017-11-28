import json
import socket

class ConfigHandler():
    """ Handler for clHue configuration. """

    def __init__(self):
        self.conf = dict()

    def load(self):
        """ Load the configuration file (clConfig.conf) and returns the loaded configuration in a dictionary. """
        # Attempt to load the file
        try:
            print("Loading configuration file.")
            with open('clConfig.conf', 'r') as confFile:
                self.conf = json.load(confFile)
        except (FileNotFoundError, json.decoder.JSONDecodeError):
            print("Configuration file missing or empty.")

        # See if there is a bridge IP listed
        try:
            bridgeIP = self.conf["bridgeIP"]
            print("Found bridge in configuration file: ", bridgeIP)
        except (KeyError):
            print("No bridge IP found in configuration file. Searching the network...")
            bridgeIP = self.getBridgeIP()
            self.conf["bridgeIP"] = bridgeIP
            self.writeConfig()
        return self.conf

    def getBridgeIP(self):
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
                    print('Bridge found at', bridgeIP)
                    return bridgeIP
        except socket.timeout:
            pass
        s.close()
        if bridgeIP is None:
            print("No bridge found. Exiting.")
            exit()

    def writeConfig(self):
        """ Writes the currently loaded configuration to the configuration file. Doesn't return anything. """
        with open('clConfig.conf', 'w') as confFile:
            json.dump(self.conf, confFile)
            confFile.flush()
            print('Written to configuration file.')

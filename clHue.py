import drest
import cmd
import socket
import json

class clHue(cmd.Cmd):
	intro = 'Welcome to clHue!'
	prompt = 'hue> '
	bridgeIP = None

	def __init__(self):
		super(clHue, self).__init__()
		try:
			confFile = open('clConfig.conf', 'r+')
			conf = json.load(confFile)
		except FileNotFoundError:
			print("Configuration file not found. Creating new configuration file.")
			confFile = open('clConfig.conf', 'w+')
			confFile.write('{}')
			conf = None
		confFile.close()
		try:
			bridgeIP = conf["bridgeIP"]
		except (KeyError, TypeError):
			print("Could not find a bridge IP. Searching the network...")
			self.bridgeIP = self.getBridgeIP()
			if self.bridgeIP is None:
				print("No bridge found. Exiting.")
				do_exit()

	# Gets the bridge's IP address
	def getBridgeIP(self):
		msg = \
		    'M-SEARCH * HTTP/1.1\r\n' \
		    'ST:upnp:rootdevice\r\n' \
		    'MX:2\r\n' \
		    'MAN:"ssdp:discover"\r\n' \
		    '\r\n'

		s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
		s.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
		s.settimeout(5)
		s.sendto(msg.encode(), ('192.168.50.255', 1900)) # TODO: Make this find the broadcast address

		try:
			while True:
				data, addr = s.recvfrom(65507)
				if 'IpBridge'.encode() in data: # TODO: Make this work if there are multiple bridges on the network
					print('Bridge found at', addr[0])
					return addr[0]
					break
		except socket.timeout:
			return None
			pass
		s.close()

	def do_exit():
		exit()

if __name__ == '__main__':
	clHue().cmdloop()

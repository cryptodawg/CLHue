import drest
import cmd
import socket
import json
import pprint

class clHue(cmd.Cmd):
	intro = 'Welcome to clHue!'
	prompt = 'hue> '
	bridgeIP = None
	api = None
	username = '8zBIONh42t4l1LbxOymAit7LYY9UHj338dW0jjc0'
	conf = dict()
	troubleshooting = True

	def __init__(self):
		super(clHue, self).__init__()
		try:
			print("Loading configuration file.")
			with open('clConfig.conf', 'r') as confFile:
				self.conf = json.load(confFile)
				print("Found bridge in configuration file: ", self.conf["bridgeIP"])
		except (FileNotFoundError, json.decoder.JSONDecodeError):
			print("Configuration file missing or empty.")

		try:
			self.bridgeIP = self.conf["bridgeIP"]
		except (KeyError):
			print("No bridge IP found in configuration file. Searching the network...")
			# TODO: Prompt the user if this is the bridge we wish to connect to - if yes, have them push the button then go through connection steps to authenticate
			self.bridgeIP = self.getBridgeIP()
			if self.bridgeIP is None:
				print("No bridge found. Exiting.")
				self.do_exit()
			else:
				self.conf["bridgeIP"] = self.bridgeIP

				self.writeConfig() # TODO: Ask if we want to write to configuration
		self.api = drest.API('http://' + self.bridgeIP + '/api/' + self.username)
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

	# Returns the response data of a request in an dictionary
	def responseData(self, arg, mode):
		arg = arg.replace(' ', '/')
		response = self.api.make_request(mode, arg)
		data = json.loads(json.dumps(response.data))
		if self.troubleshooting:
			pprint.pprint(data)
		if len(data) == 1:
			data = dict(data[0])
		assert not 'error' in data.keys() ,"Incorrect arguments"
		return data



	# Writes the currently loaded configuration to the configuration file
	def writeConfig(self):
		with open('clConfig.conf', 'w') as confFile:
			json.dump(self.conf, confFile)
			confFile.flush()
			print('Written to configuration file.')

	# Statuses an object
	# Parameters: arg - arguments separated by a space
	# Returns: True if object is turned on; False otherwise.
	def getState(self, arg):
		return self.responseData(arg, 'GET')['state']['on']

	### THE FOLLOWING ARE THE METHODS THAT ARE RAN IN THE PROMPT ###

	# Exit the program
	# arg: None
	def do_exit(self, arg):
		print("Bye!")
		exit()

	# Get items on the bridge
	# arg: Follows pattern defined in Hue API
	def do_get(self, arg):
		try:
			data = self.responseData(arg, 'GET')
			if not self.troubleshooting:
				pprint.pprint(data) # If troubleshooting mode is not enabled, this will not print to the console, which defeats the whole purpose of this method
		except AssertionError:
				print("Please specify an item to get. Enter 'help get' for more information.")

	# Toggles items on the bridge
	# arg: Follows pattern defined in Hue API
	def do_toggle(self, arg):
		try:
			if self.getState(arg):
				print('Light is on, turning off.')
			else:
				print('Light is off, turning on.')
		except AssertionError:
			print("Please specify an item to toggle. Enter 'help toggle' for more information.")

if __name__ == '__main__':
	clHue().cmdloop()

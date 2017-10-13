import socket
import ctypes

# Finds the Hue bridge
def findBridge():
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
		pass

findBridge()

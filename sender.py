# chat server using multicast
# python fork of the original ruby implementation
# http://tx.pignata.com/2012/11/multicast-in-ruby-building-a-peer-to-peer-chat-system.html
# send.py
# usage : $ python send.py message

import socket
import struct
import sys

#message = sys.argv[1] if len(sys.argv) > 1 else 'message via multicast'.encode()
message = 'message via multicast'.encode()
multicast_addr = '10.151.32.60'
port = 3000

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
ttl = struct.pack('b', 1)
sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, ttl)
sock.sendto(message, (multicast_addr, port))
sock.close()
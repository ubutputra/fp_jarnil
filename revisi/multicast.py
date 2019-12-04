import socket
import struct
import sys
import time
import threading

def multicast_recv():
	groupip='224.3.29.73'
	groupport=10000
	multicast_group = groupip
	server_address = ('', groupport)
	sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

	sock.bind(server_address)

	group = socket.inet_aton(multicast_group)
	mreq = struct.pack('4sL', group, socket.INADDR_ANY)
	sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)
	while True:
		sock.settimeout(None)
		data, address = sock.recvfrom(1024)
		print('received %s bytes from %s' % (len(data), address))
		print(data.decode())
		pesan=data.decode().split(";")
		if int(pesan[1])<5:
			kirim=str(pesan[0])+";"+str(int(pesan[1])+1)
			send_only = threading.Thread(target=multicast_send_only, args=(1,kirim))
			send_only.start()
			pass
		# print('sending acknowledgement to', address)
		# sock.sendto('theack'.encode(), address)

def multicast_send_only(a,pesan):
	time.sleep(1)
	message = pesan
	multicast_group = ('224.3.29.73', 10000)

	sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

	sock.settimeout(60)

	ttl = struct.pack('b', 1)
	sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, ttl)
	sent = sock.sendto(message.encode(), multicast_group)

def multicast_send(a,pesan):
	message = pesan
	multicast_group = ('224.3.29.73', 10000)

	sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

	sock.settimeout(60)

	ttl = struct.pack('b', 1)
	sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, ttl)
	try:

	    print ('sending "%s"' % message)
	    sent = sock.sendto(message.encode(), multicast_group)

	    while True:
	        print ('waiting to receive')
	        try:
	            data, server = sock.recvfrom(16)
	        except socket.timeout:
	            print ('timed out, no more responses')
	            break
	        else:
	            print ('received "%s" from %s' % (data, server))
	            break

	finally:
	    print ('closing socket')
	    sock.close()

if __name__ == "__main__":
	recv = threading.Thread(target=multicast_recv, args=())
	recv.start()
	while True:
		command=input("enter 1 to send: ")
		if command=='1':
			send = threading.Thread(target=multicast_send, args=(1,"Pesan penting untukmu;0"))
			send.start()
			# multicast_send('Pesan penting untukmu;0')
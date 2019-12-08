import socket
import struct
import sys
import time
import threading
import hashlib

def multicast_recv(a,iam):
	hashbuffer = []
	msgbuffer = []
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
		print('\nreceived %s bytes from %s' % (len(data), address))
		print(data.decode())
		pesan=data.decode().split(";")1
		if str(pesan[2])==iam:
			continue
		elif str(pesan[3] == iam):
			print("ada pesan!")
			print(str(pesan[0]))
		#kalo belum melebihi hop
		elif int(pesan[1])<5:
			#kalo pesannya belum ada di buffer
			print("buffer: " + str(msgbuffer))
			if str(pesan[4]) not in msgbuffer:
				kirim = str(pesan[0]) + ";" + str(int(pesan[1]) + 1) + ";" + str(pesan[2]) + str(pesan[3]) + str(pesan[4])
				hashbuffer.append(str(pesan[4]))
				msgbuffer.append(kirim)
				while True:
					send_only = threading.Thread(target=multicast_send_only, args=(1,i))
					send_only.start()
			#drop kalo udah punya messagenya di buffer
			else:
				print("message already exists on the buffer, dropping message..")
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
	print(sent)

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
		print(sent)
		
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
	iam=input("who are you? ")
	recv = threading.Thread(target=multicast_recv, args=(1,iam))
	recv.start()
	while True:
		command=input("inputkan 1 untuk mengirim >> ")
		if command=='1':
			pesanku = "Pesan penting untukmu~~"
			receiver = input("untuk siapa? >> ")
			#hash buat bedain jenis pesan
			thehash = hashlib.md5((pesanku + str(iam) + str(receiver)).encode())
			hashhex = thehash.hexdigest()
			
			pesan = pesanku + ";0;" + str(iam) + ";" + str(receiver) + ";" + str(hashhex)
			send = threading.Thread(target=multicast_send_only, args=(1,pesan))
			send.start()
			# multicast_send('Pesan penting untukmu;0')
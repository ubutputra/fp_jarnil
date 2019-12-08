import socket
import struct
import sys
import time
import threading
import hashlib

max_hop = 5
hashbuffer = []
msgbuffer = []
groupip='224.3.29.73'
groupport=10000

def multicast_recv(a,iam):
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
		# print(data.decode())
		pesan=data.decode().split(";")
		if str(pesan[3]) == iam:
			print("ada pesan!")
			print(str(pesan[0]))
		#kalo belum melebihi hop
		elif int(pesan[1]) < max_hop:
			#kalo pesannya belum ada di buffer
			if str(pesan[4]) not in hashbuffer:
				kirim = data.decode()
				hashbuffer.append(str(pesan[4]))
				msgbuffer.append(kirim)
			#drop kalo udah punya messagenya di buffer
			else:
				print("message already exists on the buffer, dropping message..")
		else:
			print("dropping packets due to maximum amount of hop.")
		# print('sending acknowledgement to', address)
		# sock.sendto('theack'.encode(), address)

def multicast_send_only(pesan):
	message = pesan
	multicast_group = (groupip, groupport)

	sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

	ttl = struct.pack('b', 1)
	sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, ttl)
	sent = sock.sendto(message.encode(), multicast_group)
	# print(sent)

def multicast_buffering():
	while True:
		time.sleep(5)
		lala = 0
		for x in msgbuffer:
			msg=x.split(";")
			if int(msg[1])<max_hop:
				hopnya = int(msg[1]) + 1
				kirim = str(msg[0]) + ";" + str(hopnya) + ";" + str(msg[2]) + ";" + str(msg[3]) + ";" + str(msg[4])
				multicast_send_only(kirim)
				msgbuffer[int(lala)]=kirim
			lala = int(lala)+1

		po = 0
		for i in msgbuffer:
			psn=i.split(";")
			if int(psn[1])>=max_hop:
				del msgbuffer[po]
				del hashbuffer[po]
			po = int(po)+1

if __name__ == "__main__":
	iam=input("who are you? ")
	recv = threading.Thread(target=multicast_recv, args=(1,iam))
	recv.start()
	buff = threading.Thread(target=multicast_buffering, args=())
	buff.start()
	while True:
		command=input("inputkan 1 untuk mengirim >> ")
		if command=='1':
			pesanku = "Pesan penting untukmu~~"
			receiver = input("untuk siapa? >> ")
			#hash buat bedain jenis pesan
			thehash = hashlib.md5((pesanku + str(iam) + str(receiver)).encode())
			hashhex = thehash.hexdigest()
			
			pesan = pesanku + ";0;" + str(iam) + ";" + str(receiver) + ";" + str(hashhex)
			multicast_send_only(pesan)
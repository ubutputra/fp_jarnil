import socket
import struct
import sys

groupip=str(sys.argv[1])
groupport=int(sys.argv[2])
multicast_group = groupip
server_address = ('', groupport)
iam=input('who are you? ')
connectedip=input("connect to ip? ")
connectedport=input("connect to port? ")


# multicast_group = '224.3.29.73'
# server_address = ('', 10002)


# Create the socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Bind to the server address
sock.bind(server_address)

# Tell the operating system to add the socket to the multicast group
# on all interfaces.
group = socket.inet_aton(multicast_group)
mreq = struct.pack('4sL', group, socket.INADDR_ANY)
sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)
nodearray=dict()
# Receive/respond loop
while True:
    print('\nwaiting to receive message')
    data, address = sock.recvfrom(1024)
    
    print('received %s bytes from %s' % (len(data), address))
    print(data.decode())
    pesan = data.decode().split(" ")
    print(pesan[-1])
    if pesan[0]=="ack":
    	theack='ack '+str(pesan[1])
    	alamat=nodearray[str(pesan[1])].split(" ")
    	print(alamat)
    	address1=(alamat[0],int(alamat[1]))

    	print('sending acknowledgement to', address1)
    	sock.sendto(theack.encode(), address1)

    elif str(pesan[-1])==str(iam):
    	theack0='ack '+str(pesan[0])
    	print('sending acknowledgement to', address)
    	sock.sendto(theack0.encode(), address)
    else:
    	nodearray[str(pesan[0])]=str(address[0])+" "+str(address[1])
    	print(nodearray)
    	connected_group = (str(connectedip), int(connectedport))
    	sent = sock.sendto(data, connected_group)

    
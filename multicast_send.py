import socket
import struct
import sys

groupip=str(sys.argv[1])
groupport=int(sys.argv[2])
destination=input('destination: ')
iam=input("who am i? ")
message = str(iam)+' TO '+str(destination)
multicast_group = (groupip, groupport)

# Create the datagram socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Set a timeout so the socket does not block indefinitely when trying
# to receive data.
sock.settimeout(60)

ttl = struct.pack('b', 1)
sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, ttl)

try:

    # Send data to the multicast group
    print ('sending "%s"' % message)
    sent = sock.sendto(message.encode(), multicast_group)

    # Look for responses from all recipients
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
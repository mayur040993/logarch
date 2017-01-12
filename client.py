import socket
import sys
import sh
def getconnection(data):
	sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	server_address = ('localhost', 10000)
	print >>sys.stderr, 'connecting to %s port %s' % server_address
	sock.connect(server_address)
	try:
           sock.sendall(data)
           data = sock.recv(1024)
           print >>sys.stderr, 'received "%s"' % data
	finally:
    	   sock.close()

getconnection("some data")

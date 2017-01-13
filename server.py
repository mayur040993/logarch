import socket
import sys
import thread
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_address = ('localhost', 10000)
print >>sys.stderr, 'starting up on %s port %s' % server_address
sock.bind(server_address)
sock.listen(5)
##code

def processingdata(data):
    return data.split(' ')

def multipleclients(connection):
    try:
        print >>sys.stderr, 'client connected:', client_address
        while True:
            data = connection.recv(1024)
            print >>sys.stderr, '"%s"' % data
            if data:
               pass
            else:
                break
    finally:
        connection.close()


while True:
    print >>sys.stderr, 'waiting for a connection'
    connection, client_address = sock.accept()
    thread.start_new_thread(multipleclients,(connection,))

sock.close()
